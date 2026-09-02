#!/usr/bin/env python3
"""Ivy dispatch runner — executes queued contracts on the Mac (D2).

Runs from launchd every 30 min inside the 09:15-21:00 window (see
config.yml dispatch.runner_window). Operates on its OWN clone of ivy under
~/.ivy-dispatch/ so the human checkout is never mutated. One contract per
tick, oldest first. State changes are bot-authored commits; the repo is the
message bus and the cloud failsafe does verification — this script never
stamps `verified:`.

Flags: --once (ignore the window; single pass)  --dry-run (plan only,
print the exact harness argv, change nothing).

Harness notes: `claude -p` flags are stable; `codex exec` flags are
confirmed during the D2 smoke test — if the argv printed by --dry-run is
wrong for your codex version, fix HARNESS_ARGV below.

The attribution gate tests membership in config.yml `connected_emails`
(2026-09-01: equality against `commit_email` alone failed three build
contracts on a clone correctly configured with the second connected
address). A contract with `blocked_by: [id, ...]` is skipped until every id
sits in dispatch/done/. Pure parts are covered by dispatch-runner-test.py.

The runner execs the copy inside IVY once the sync has run: the launchd entry
point is a dev checkout that only moves when a human pulls, so without this a
pushed runner change lands in IVY while the old code keeps executing.
"""
import fcntl, os, re, shlex, signal, subprocess, sys
from datetime import datetime, timedelta
from pathlib import Path

WORKROOT = Path.home() / ".ivy-dispatch"
IVY = WORKROOT / "ivy"
WORK = WORKROOT / "work"
IVY_REMOTE = "https://github.com/tompulsarlabs/ivy.git"
BOT = ["-c", "user.name=ivy-bot", "-c", "user.email=bot@ivy.invalid"]
WINDOW = ((9, 15), (21, 0))
MARK_BEGIN, MARK_END = "BEGIN_REPORT", "END_REPORT"

def log(msg):
    print(f"[{datetime.now().astimezone().isoformat(timespec='seconds')}] {msg}", flush=True)

def run(args, cwd=None, check=True, capture=True):
    r = subprocess.run(args, cwd=cwd, text=True,
                       capture_output=capture)
    if check and r.returncode != 0:
        raise RuntimeError(f"{' '.join(map(str, args))} -> {r.returncode}: {(r.stderr or '')[:400]}")
    return r

def in_window(now):
    t = (now.hour, now.minute)
    return WINDOW[0] <= t <= WINDOW[1]

def ensure_clone(path, remote):
    if not (path / ".git").exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--quiet", remote, str(path)])
    run(["git", "fetch", "--quiet", "origin"], cwd=path)
    head = run(["git", "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD"], cwd=path,
               check=False).stdout.strip().rsplit("/", 1)[-1] or "main"
    run(["git", "checkout", "--quiet", head], cwd=path)
    run(["git", "reset", "--hard", "--quiet", f"origin/{head}"], cwd=path)
    return head

def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None, ""
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    b = re.search(r"wall_minutes:\s*(\d+)", m.group(1))
    fm["wall_minutes"] = int(b.group(1)) if b else 30
    raw = fm.get("blocked_by", "").strip().strip("[]")
    fm["blocked_by"] = [x.strip() for x in raw.split(",") if x.strip()]
    return fm, m.group(2)

def load_config():
    cfg = (IVY / "config.yml").read_text()
    commit_email = re.search(r"^commit_email:\s*(\S+)", cfg, re.M).group(1)
    block = re.search(r"^connected_emails:[^\n]*\n((?:[ \t]+-[^\n]*\n?)*)", cfg, re.M)
    connected = re.findall(r"-\s*(\S+)", block.group(1)) if block else []
    connected = connected or [commit_email]
    lanes = {}
    lane_block = re.search(r"^lanes:[^\n]*\n((?:[ \t]+.*\n?)*)", cfg, re.M).group(1)
    current = None
    for line in lane_block.splitlines():
        m = re.match(r"^  ([a-z-]+):\s*$", line)
        if m:
            current = m.group(1); lanes[current] = {}
        m = re.match(r"^    ([a-z]+):\s*\{(.*)\}", line)
        if m and current:
            pool, inner = m.group(1), m.group(2)
            entry = dict(re.findall(r"([a-z_-]+):\s*([^,}\s]+)", inner))
            lanes[current][pool] = entry
    return commit_email, connected, lanes

def author_connected(ident, connected):
    """True if `git var GIT_AUTHOR_IDENT` names any verified address — the
    author field is what GitHub counts, and more than one address is verified."""
    return any(f"<{e}>" in ident for e in connected)

def open_blockers(fm, done_ids):
    """Ids in blocked_by that are not yet in dispatch/done/ (order kept)."""
    return [b for b in fm.get("blocked_by", []) if b not in done_ids]

def synced_runner(current, synced):
    """The synced runner to exec into, or None to carry on with this one.

    The entry point (launchd points at a dev checkout) and the checkout the
    runner syncs are different working copies, so a pushed runner change does
    not reach the running code: on 2026-09-02 a fixed attribution gate sat in
    IVY while the pre-fix gate executed from ~/Build/ivy and refused four
    contracts. Exec the synced copy, never argv[0] — argv[0] is the stale file.
    """
    try:
        if synced.resolve() == current.resolve() or not synced.is_file():
            return None
        return synced if synced.read_bytes() != current.read_bytes() else None
    except OSError:
        return None

def bot_commit_push(msg, paths):
    run(["git", "add", "--"] + [str(p) for p in paths], cwd=IVY)
    run(["git"] + BOT + ["commit", "--quiet", "-m", msg], cwd=IVY)
    for attempt in range(3):
        p = run(["git", "push", "--quiet", "origin", "HEAD"], cwd=IVY, check=False)
        if p.returncode == 0:
            return True
        run(["git", "pull", "--rebase", "--quiet", "origin"], cwd=IVY, check=False)
    return False

def set_state(path, new_state, extra_fm=None):
    text = path.read_text()
    text = re.sub(r"^state: .*$", f"state: {new_state}", text, count=1, flags=re.M)
    if extra_fm:
        text = re.sub(r"^(state: .*)$", r"\1\n" + extra_fm, text, count=1, flags=re.M)
    path.write_text(text)

def harness_argv(entry, prompt, ctype):
    h, model = entry.get("harness"), entry.get("model")
    if h == "claude-code":
        argv = ["claude", "-p", prompt, "--model", model]
        if ctype in ("build", "chore"):
            # acceptEdits alone denies git push / gh pr create in -p mode
            # (verified 2026-08-28); the worker needs the shell for its DoD.
            argv += ["--permission-mode", "acceptEdits", "--allowedTools", "Bash"]
        return argv
    if h == "codex":
        argv = ["codex", "exec", "--model", model]
        if ctype in ("build", "chore"):
            argv += ["-s", "workspace-write"]  # exec defaults to read-only sandbox
        return argv + [prompt]
    raise RuntimeError(f"unknown harness {h}")

def build_prompt(cid, repo, ctype, body):
    head = (f"You are an Ivy dispatch worker executing contract {cid}. "
            f"Your working directory is a fresh checkout of {repo}.\n")
    if ctype == "review":
        tail = ("\nSkills: if a `code-review` skill is installed in this harness, drive the review "
                "with it (the Task above is the spec axis); if it is not, review without it.\n"
                "\nRules: read-only — do not commit, push, or modify anything. "
                f"Produce your complete findings as markdown and print them between two lines "
                f"containing exactly {MARK_BEGIN} and {MARK_END}. Print nothing after {MARK_END}.")
    else:
        tail = ("\nSkills: if `tdd` and `code-review` skills are installed in this harness, build "
                "test-first at the seams the Task names and review the diff against the Task before "
                "opening the PR; if they are not installed, proceed without them.\n"
                "\nRules: do the work on a new branch named dispatch/" + cid + ", commit with the "
                "repository's connected git identity, push the branch, and open a DRAFT pull "
                "request. Never push to the default branch. When finished, print a short summary "
                f"of what you did between two lines containing exactly {MARK_BEGIN} and {MARK_END}.")
    return head + body.strip() + tail

def finalize(qpath, cid, dest, state, outcome_lines, msg, extra_paths=()):
    set_state(qpath, state)
    with qpath.open("a") as f:
        f.write("\noutcome:\n" + "".join(f"  {l}\n" for l in outcome_lines))
    target = IVY / "dispatch" / dest / qpath.name
    run(["git", "mv", str(qpath), str(target)], cwd=IVY)
    lint = run(["bash", "scripts/dispatch-lint.sh"], cwd=IVY, check=False)
    if lint.returncode != 0:
        log(f"LINT FAILED after finalize: {lint.stderr or lint.stdout}")
    bot_commit_push(msg, [target] + list(extra_paths))
    log(f"{cid}: {state} -> dispatch/{dest}/")

def main():
    once = "--once" in sys.argv
    dry = "--dry-run" in sys.argv
    now = datetime.now().astimezone()
    if not once and not in_window(now):
        return 0
    WORKROOT.mkdir(exist_ok=True)
    lockf = open(WORKROOT / "lock", "w")
    try:
        fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        log("another runner instance holds the lock; exiting"); return 0

    ensure_clone(IVY, IVY_REMOTE)
    fresh = synced_runner(Path(__file__), IVY / "scripts" / "dispatch-runner.py")
    if fresh and not os.environ.get("IVY_RUNNER_REEXEC"):
        log(f"runner differs from {IVY} — exec'ing the synced copy")
        os.environ["IVY_RUNNER_REEXEC"] = "1"
        lockf.close()          # flock released; the exec'd process re-acquires
        os.execv(sys.executable, [sys.executable, str(fresh), *sys.argv[1:]])

    lint = run(["bash", "scripts/dispatch-lint.sh"], cwd=IVY, check=False)
    if lint.returncode != 0:
        log(f"queue not lint-clean, refusing to run: {lint.stderr or lint.stdout}"); return 1
    commit_email, connected, lanes = load_config()
    done_ids = {p.stem for p in (IVY / "dispatch" / "done").glob("*.md")}

    for qpath in sorted((IVY / "dispatch" / "queue").glob("*.md")):
        fm, body = parse_frontmatter(qpath.read_text())
        if not fm or fm.get("state") != "open":
            continue
        cid, repo, ctype = fm["id"], fm["repo"], fm["type"]
        if datetime.fromisoformat(fm["expires"]) <= now:
            log(f"{cid}: past expiry, leaving for the failsafe to expire"); continue
        blockers = open_blockers(fm, done_ids)
        if blockers:
            log(f"{cid}: blocked by {', '.join(blockers)} (not in dispatch/done/) — skipping"); continue
        entry = lanes.get(fm["lane"], {}).get(fm.get("pool") or "anthropic")
        if not entry or entry.get("model") == "VERIFY":
            log(f"{cid}: lane {fm['lane']}/{fm.get('pool') or 'anthropic'} unresolved (VERIFY) — skipping"); continue

        clone = WORK / repo.split("/")[-1]
        ensure_clone(clone, f"https://github.com/{repo}.git")
        if ctype == "build":
            ident = run(["git", "var", "GIT_AUTHOR_IDENT"], cwd=clone).stdout
            if not author_connected(ident, connected):
                finalize(qpath, cid, "failed", "failed",
                         [f"claimed_at: {now.isoformat(timespec='seconds')}",
                          "exit: attribution",
                          f"note: next commit would author '{ident.split('>')[0].strip()}>' — not a connected address (config.yml connected_emails)"],
                         f"dispatch: failed {cid} — attribution gate")
                continue

        prompt = build_prompt(cid, repo, ctype, body.split("outcome:")[0])
        argv = harness_argv(entry, prompt, ctype)
        if dry:
            log(f"{cid}: DRY RUN — would claim, then exec in {clone}:")
            log("  " + " ".join(shlex.quote(a if len(a) < 120 else a[:117] + "...") for a in argv))
            return 0

        set_state(qpath, "claimed", f"claimed_at: {now.isoformat(timespec='seconds')}")
        if not bot_commit_push(f"dispatch: claim {cid}", [qpath]):
            log(f"{cid}: claim push lost a race; next tick retries"); return 0

        log(f"{cid}: executing via {entry['harness']} ({entry['model']}), budget {fm['wall_minutes']}m")
        start = datetime.now()
        proc = subprocess.Popen(argv, cwd=clone, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, start_new_session=True)
        try:
            out, _ = proc.communicate(timeout=fm["wall_minutes"] * 60)
            code = proc.returncode
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            out, code = (proc.communicate()[0] or ""), "timeout"
        wall = round((datetime.now() - start).total_seconds() / 60, 1)

        m = re.search(re.escape(MARK_BEGIN) + r"\n(.*?)\n" + re.escape(MARK_END), out or "", re.S)
        report_rel = f"dispatch/reports/{cid}.md"
        base = [f"claimed_at: {now.isoformat(timespec='seconds')}",
                f"finished_at: {datetime.now().astimezone().isoformat(timespec='seconds')}",
                f"harness: {entry['harness']} (dispatch-runner)",
                f"model: {entry['model']}", f"wall_minutes: {wall}", f"exit: {code}"]
        if code == 0 and m:
            (IVY / report_rel).write_text(
                f"# Report — {cid}\n\nProduced by the {fm['lane']}/{fm.get('pool') or 'anthropic'} "
                f"lane, {wall} wall-minutes.\n\n{m.group(1).strip()}\n")
            finalize(qpath, cid, "done", "done",
                     base + ["artifacts:", f"  - {report_rel}"],
                     f"dispatch: done {cid} — awaiting failsafe verification",
                     extra_paths=[IVY / report_rel])
        else:
            reason = "timeout" if code == "timeout" else ("no_report" if code == 0 else "harness_error")
            tail = (out or "")[-1500:]
            (IVY / "dispatch" / "failed").mkdir(exist_ok=True)
            finalize(qpath, cid, "failed", "failed",
                     base + [f"note: {reason}; last output lines follow", "output_tail: |",
                             *("    " + l for l in tail.splitlines()[-12:])],
                     f"dispatch: failed {cid} — {reason}")
        return 0
    log("no executable contract in queue")
    return 0

if __name__ == "__main__":
    sys.exit(main())
