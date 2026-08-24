#!/usr/bin/env python3
"""Scan local project roots for git repos and publish their WIP state to
local-wip.json so the cloud scout sees local truth (dirty trees, unpushed
commits, repos with no remote at all).

Privacy: the published file identifies repos by directory basename and
remote slug only — no hostname, no filesystem paths. Those are public
identifiers already (or at worst a folder name); the machine itself stays
out of the public repo.

Robustness (replaces the original shell version):
- JSON is generated with the json module, never string interpolation.
- The output is written atomically (temp file + os.replace) under a lock,
  so overlapping runs can't interleave.
- Push flow: an earlier run's unpushed commit is retried even when the new
  scan changes nothing, and `pull --rebase --autostash` tolerates unrelated
  dirty files in the Ivy checkout.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

IVY = Path(os.environ.get("IVY_DIR", Path.home() / "Build" / "ivy"))
OUT = IVY / "local-wip.json"
LOCK = IVY / ".local-wip.lock"
LOCK_STALE_SECONDS = 15 * 60


def git(repo, *args, check=False):
    """Run git in `repo`; return stdout or None on failure."""
    try:
        r = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if r.returncode != 0:
        return None if not check else None
    return r.stdout.strip()


def read_roots(config_path):
    """Read local_wip.roots from config.yml.

    Deliberately parses only the one documented shape (a nested list under
    `local_wip:` / `roots:`) and fails loudly on anything else, rather than
    half-implementing YAML. If the config grows past this shape, install a
    real YAML parser and replace this function.
    """
    try:
        text = config_path.read_text()
    except OSError:
        return [Path.home() / "Build"]
    roots, in_block, in_roots = [], False, False
    for line in text.splitlines():
        if re.match(r"^local_wip:", line):
            in_block, in_roots = True, False
            continue
        if in_block and re.match(r"^\S", line):
            break
        if in_block and re.match(r"^\s+roots:", line):
            in_roots = True
            continue
        if in_roots:
            m = re.match(r"^\s+-\s+(\S+)", line)
            if m:
                roots.append(Path(os.path.expanduser(m.group(1))))
            elif line.strip():
                in_roots = False
    if in_block and not roots:
        print("local-wip: local_wip block present but no roots parsed — "
              "config.yml shape changed?", file=sys.stderr)
        sys.exit(1)
    return roots or [Path.home() / "Build"]


def scan_repo(repo):
    branch = git(repo, "branch", "--show-current") or "(detached)"
    status = git(repo, "status", "--porcelain")
    dirty = len(status.splitlines()) if status else 0
    remotes = git(repo, "remote") or ""
    if not remotes:
        remote = "none"
        unpushed = int(git(repo, "rev-list", "--count", "HEAD") or 0)
    else:
        url = git(repo, "remote", "get-url", "origin") or ""
        m = re.search(r"github\.com[:/]+(.+?)(?:\.git)?$", url)
        remote = m.group(1) if m else "other"
        unpushed = int(
            git(repo, "rev-list", "--count", "--branches", "--not", "--remotes") or 0
        )
    return {
        "name": repo.name,
        "remote": remote,
        "branch": branch,
        "dirty_files": dirty,
        "unpushed_commits": unpushed,
        "last_commit": git(repo, "log", "-1", "--format=%cs") or "",
    }


def acquire_lock():
    try:
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        return True
    except FileExistsError:
        try:
            if LOCK.stat().st_mtime < datetime.now().timestamp() - LOCK_STALE_SECONDS:
                LOCK.unlink()
                return acquire_lock()
        except OSError:
            pass
        return False


def unpushed_in_ivy():
    out = git(IVY, "rev-list", "--count", "@{u}..HEAD")
    return int(out) if out and out.isdigit() else 0


def sync_ivy():
    """Rebase onto upstream (stashing unrelated dirt) and push."""
    if git(IVY, "pull", "--rebase", "--autostash", "--quiet") is None:
        git(IVY, "rebase", "--abort")
        return False
    return git(IVY, "push", "--quiet") is not None


def main():
    if not acquire_lock():
        return 0
    try:
        repos = []
        for root in read_roots(IVY / "config.yml"):
            if not root.is_dir():
                continue
            for gitdir in sorted(root.glob("*/.git")) + sorted(root.glob("*/*/.git")):
                if gitdir.is_dir():
                    repos.append(scan_repo(gitdir.parent))

        payload = {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "repos": repos,
        }

        try:
            previous = json.loads(OUT.read_text())
        except (OSError, ValueError):
            previous = None
        changed = previous is None or previous.get("repos") != repos

        if changed:
            fd, tmp = tempfile.mkstemp(dir=IVY, prefix=".local-wip.")
            with os.fdopen(fd, "w") as f:
                json.dump(payload, f, indent=2)
                f.write("\n")
            os.replace(tmp, OUT)
            git(IVY, "add", "local-wip.json")
            git(
                IVY, "-c", "user.name=ivy-bot", "-c", "user.email=bot@ivy.invalid",
                "commit", "--quiet", "-m", f"wip: local scan — {len(repos)} repos",
            )

        # Push whenever anything is unpushed — including a stranded commit
        # from an earlier run whose push failed.
        if unpushed_in_ivy() > 0:
            sync_ivy()
        return 0
    finally:
        LOCK.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
