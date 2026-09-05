"""Supervisor-owned local records. Checksums detect corruption, not hostile operators."""
import fcntl
import hashlib
import json
import os
import re
import tempfile
import time
from dataclasses import asdict
from pathlib import Path

from .budget import BudgetBlocked, Limits
from .canonical import InvalidManifest, canonical_bytes, digest, read_json


def write_record(path, value):
    """Replace a record atomically and sync both its data and parent directory."""
    path = Path(path)
    body = canonical_bytes({"record": value, "sha256": digest(value)}) + b"\n"
    fd, tmp = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(body)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def read_record(path):
    envelope = read_json(path)
    if (type(envelope) is not dict or set(envelope) != {"record", "sha256"}
            or digest(envelope["record"]) != envelope["sha256"]):
        raise InvalidManifest("record integrity mismatch")
    return envelope["record"]


def safe_id(value):
    if type(value) is not str or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,100}", value):
        raise InvalidManifest("invalid local artifact identifier")
    return value


class AttemptStore:
    """One sequential supervisor; the OS lock survives neither exit nor a crash.

    Reservations DO survive crashes. An unresolved container blocks new launches.
    Time is conservatively reserved at its full limit, never refunded. Wall-clock
    rollback blocks work; this local ledger is not a trusted metering service.
    """
    def __init__(self, directory, binding, limits: Limits, clock=time.time):
        self.directory = Path(directory)
        self.binding, self.limits, self.clock = binding, limits, clock
        self.lock = None

    def __enter__(self):
        self.directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        if self.directory.is_symlink():
            raise InvalidManifest("store cannot be a symlink")
        self.lock = open(self.directory / ".lock", "a+b")
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            path = self.directory / "ledger.json"
            if path.exists():
                self.state = read_record(path)
                self._validate()
            else:
                now = self._now()
                self.state = {"schema_version": 1, "binding": self.binding,
                              "limits": asdict(self.limits), "started_at": now,
                              "last_time": now, "attempts": []}
                self._save()
        except BaseException:
            self.lock.close()
            self.lock = None
            raise
        return self

    def __exit__(self, *exc):
        self.lock.close()
        self.lock = None

    def _now(self):
        now = self.clock()
        if type(now) not in (int, float) or not (0 <= now < float("inf")):
            raise BudgetBlocked("invalid supervisor clock")
        return now

    def _validate(self):
        s = self.state
        keys = {"schema_version", "binding", "limits", "started_at", "last_time", "attempts"}
        if (type(s) is not dict or set(s) != keys or type(s["schema_version"]) is not int
                or s["schema_version"] != 1 or s["binding"] != self.binding
                or s["limits"] != asdict(self.limits) or type(s["attempts"]) is not list):
            raise InvalidManifest("ledger schema, comparison or limits changed")
        for key in ("started_at", "last_time"):
            if type(s[key]) not in (int, float) or not (0 <= s[key] < float("inf")):
                raise InvalidManifest("invalid ledger clock")
        if s["last_time"] < s["started_at"]:
            raise InvalidManifest("ledger clock order invalid")
        ids, unresolved = set(), 0
        for row in s["attempts"]:
            if type(row) is not dict or set(row) != {"id", "runtime_id", "seconds", "termination_confirmed", "outcome"}:
                raise InvalidManifest("invalid attempt record")
            safe_id(row["id"])
            safe_id(row["runtime_id"])
            if row["id"] in ids or type(row["seconds"]) is not int or not 0 < row["seconds"] <= self.limits.per_attempt_seconds:
                raise InvalidManifest("invalid attempt identity/time")
            if type(row["termination_confirmed"]) is not bool:
                raise InvalidManifest("invalid termination state")
            if row["outcome"] not in (None, "completed", "execution_error", "timed_out", "canceled"):
                raise InvalidManifest("invalid outcome")
            if row["termination_confirmed"] and row["outcome"] is None:
                raise InvalidManifest("closed reservation lacks outcome")
            ids.add(row["id"])
            unresolved += not row["termination_confirmed"]
        if (unresolved > 1 or len(ids) > self.limits.max_attempts
                or sum(r["seconds"] for r in s["attempts"]) > self.limits.total_seconds):
            raise InvalidManifest("ledger exceeds limits")

    def _save(self):
        self._validate()
        write_record(self.directory / "ledger.json", self.state)

    def reserve(self, attempt_id, runtime_id, seconds):
        safe_id(attempt_id)
        safe_id(runtime_id)
        now = self._now()
        rows = self.state["attempts"]
        if now < self.state["last_time"]:
            raise BudgetBlocked("clock moved backwards; no launch")
        if any(not row["termination_confirmed"] for row in rows):
            raise BudgetBlocked("previous workload termination is unconfirmed; recover it first")
        if any(row["id"] == attempt_id for row in rows):
            raise BudgetBlocked("attempt id already consumed")
        if type(seconds) is not int or not 0 < seconds <= self.limits.per_attempt_seconds:
            raise BudgetBlocked("invalid deadline")
        if (len(rows) >= self.limits.max_attempts
                or sum(row["seconds"] for row in rows) + seconds > self.limits.total_seconds
                or now - self.state["started_at"] + seconds > self.limits.total_seconds):
            raise BudgetBlocked("attempt or execution time budget exhausted")
        self.state["last_time"] = now
        rows.append({"id": attempt_id, "runtime_id": runtime_id, "seconds": seconds,
                     "termination_confirmed": False, "outcome": None})
        self._save()  # Must succeed before Docker create/start.

    def finish(self, attempt_id, runtime_id, outcome, *, terminated):
        if type(terminated) is not bool:
            raise BudgetBlocked("explicit termination confirmation required")
        row = next((r for r in self.state["attempts"] if r["id"] == attempt_id), None)
        if row is None or row["runtime_id"] != runtime_id or row["termination_confirmed"]:
            raise BudgetBlocked("attempt does not own the active reservation")
        if outcome not in ("completed", "execution_error", "timed_out", "canceled"):
            raise BudgetBlocked("invalid execution outcome")
        row.update(outcome=outcome, termination_confirmed=terminated)
        self._save()


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
