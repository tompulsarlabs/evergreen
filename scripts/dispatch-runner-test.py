#!/usr/bin/env python3
"""Unit checks for the pure parts of dispatch-runner.py — the parts that cost
contracts when wrong and that only ever run on the Mac.

Red on 2026-09-01: the attribution gate compared `git var GIT_AUTHOR_IDENT`
against `commit_email` alone, so a clone correctly configured with the
second connected address (`tom@pulsarlabsai.com`) failed three build
contracts with `exit: attribution`. This file locks the fix down.

Run: python3 scripts/dispatch-runner-test.py   (exit 0 = green)
"""
import importlib.util, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("runner", HERE / "dispatch-runner.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

CONFIG = """\
commit_email: 249609836+tompulsarlabs@users.noreply.github.com
commit_name: tompulsarlabs
connected_emails:
  - 249609836+tompulsarlabs@users.noreply.github.com
  - tom@pulsarlabsai.com
lanes:
  frontier:
    anthropic: { harness: claude-code, model: claude-opus-5, effort: xhigh }
    openai:    { harness: codex, model: gpt-5.6-sol }
  workhorse:
    anthropic: { harness: claude-code, model: claude-opus-5, effort: medium }
pools:
  anthropic: { auth: mac-local }
"""

CONTRACT = """\
---
id: 2026-09-02-example-01
type: build
state: open
repo: tompulsarlabs/example
lane: workhorse
created: 2026-09-02T09:00:00+02:00
created_by: tom
expires: 2026-09-04T09:00:00+02:00
budget: { wall_minutes: 25 }
blocked_by: [2026-09-02-example-00, 2026-09-01-other-03]
---

## Task
x
"""

failures = []
def check(name, cond):
    print(("ok   " if cond else "FAIL ") + name)
    if not cond:
        failures.append(name)

with tempfile.TemporaryDirectory() as tmp:
    runner.IVY = Path(tmp)
    (runner.IVY / "config.yml").write_text(CONFIG)
    commit_email, connected, lanes = runner.load_config()
    check("commit_email parsed", commit_email.endswith("@users.noreply.github.com"))
    check("connected_emails parsed as a list of two", connected == [
        "249609836+tompulsarlabs@users.noreply.github.com", "tom@pulsarlabsai.com"])
    check("lanes parsed", lanes["frontier"]["openai"]["model"] == "gpt-5.6-sol")

    # The 2026-09-01 failure: a clone using the second connected address.
    ident_ok = "tompulsarlabs <tom@pulsarlabsai.com> 1756738878 +0200"
    ident_bad = "Tom Green <tom@C2-LAP32-TomGreen.local> 1756738878 +0200"
    check("gate passes the second connected address", runner.author_connected(ident_ok, connected))
    check("gate refuses an invented hostname identity", not runner.author_connected(ident_bad, connected))

    fm, body = runner.parse_frontmatter(CONTRACT)
    check("blocked_by parsed as a list", fm.get("blocked_by") == ["2026-09-02-example-00", "2026-09-01-other-03"])
    check("wall_minutes parsed", fm["wall_minutes"] == 25)
    check("no blocked_by -> empty list", runner.parse_frontmatter(
        CONTRACT.replace("blocked_by: [2026-09-02-example-00, 2026-09-01-other-03]\n", ""))[0].get("blocked_by") == [])
    check("blocked while a blocker is not done",
          runner.open_blockers(fm, {"2026-09-02-example-00"}) == ["2026-09-01-other-03"])
    check("unblocked once every blocker is done",
          runner.open_blockers(fm, {"2026-09-02-example-00", "2026-09-01-other-03"}) == [])

    # Red on 2026-09-02: the launchd entry point (~/Build/ivy) and the synced
    # checkout (~/.ivy-dispatch/ivy) are different working copies, so a pushed
    # gate fix sat unexecuted while the old gate refused four contracts.
    a, b = Path(tmp) / "a.py", Path(tmp) / "b.py"
    a.write_text("old\n")
    b.write_text("new\n")
    check("differing synced copy is exec'd", runner.synced_runner(a, b) == b)
    b.write_text("old\n")
    check("identical synced copy is not exec'd", runner.synced_runner(a, b) is None)
    check("same path is never exec'd (no loop)", runner.synced_runner(a, a) is None)
    check("missing synced copy is tolerated", runner.synced_runner(a, Path(tmp) / "nope.py") is None)

    # Red on 2026-09-02: `claude` is in ~/.local/bin, absent from launchd's PATH.
    # Popen raised FileNotFoundError after the claim was pushed, stranding two
    # contracts in `claimed`. Resolve before claiming; exec an absolute path.
    argv = ["claude", "-p", "prompt", "--model", "claude-opus-5"]
    check("harness resolved to an absolute path",
          runner.resolve_harness(argv, which=lambda b: "/Users/x/.local/bin/" + b)
          == ["/Users/x/.local/bin/claude", "-p", "prompt", "--model", "claude-opus-5"])
    check("missing harness resolves to None (contract stays open)",
          runner.resolve_harness(argv, which=lambda b: None) is None)
    check("resolution keeps every argument after argv[0]",
          len(runner.resolve_harness(argv, which=lambda b: "/bin/" + b)) == len(argv))
    check("empty argv is tolerated", runner.resolve_harness([], which=lambda b: "/bin/x") is None)

    review = runner.build_prompt("c1", "o/r", "review", "## Task\nx\n")
    build = runner.build_prompt("c2", "o/r", "build", "## Task\nx\n")
    check("review prompt names the code-review skill", "code-review" in review)
    check("build prompt names tdd and code-review", "tdd" in build and "code-review" in build)
    check("review prompt stays read-only", "read-only" in review)

print()
print("dispatch-runner-test: " + ("ok" if not failures else f"{len(failures)} failing"))
sys.exit(1 if failures else 0)
