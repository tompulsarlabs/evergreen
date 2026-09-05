"""Independent source-boundary controls; no Docker or model execution."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from ivy_acceptance.budget import BudgetBlocked, Limits
from ivy_acceptance.canonical import InvalidManifest
from ivy_acceptance.docker_probe import DockerProbeAdapter
from ivy_acceptance.ports import WorkerRequest, WorkloadHandle
from ivy_acceptance.storage import AttemptStore, read_record


class PreparationBoundaryTests(unittest.TestCase):
    binding = {"plan_sha256": "a" * 64, "fixture_sha256": "b" * 64,
               "agent_version_sha256": "c" * 64}

    def adapter(self, store):
        return DockerProbeAdapter(store, {}, self.binding,
                                  "python@sha256:" + "d" * 64, "synthetic")

    def request(self):
        return WorkerRequest("attempt", "probe", "a" * 64, "b" * 64, "c" * 64, 10)

    def test_inherited_build_hooks_and_volumes_fail_before_build(self):
        for config in ({"OnBuild": ["RUN untrusted"]}, {"Volumes": {"/data": {}}}):
            with self.subTest(config=config), tempfile.TemporaryDirectory() as tmp:
                with AttemptStore(tmp, self.binding, Limits(32, 90, 3600)) as store:
                    adapter = self.adapter(store)
                    response = SimpleNamespace(stdout=json.dumps(
                        [{"Id": "sha256:" + "e" * 64, "Config": config}]).encode())
                    with patch.object(adapter, "_cmd", return_value=response) as command:
                        with self.assertRaisesRegex(InvalidManifest, "build hooks or volumes"):
                            adapter.prepare(self.request())
                        self.assertEqual(command.call_count, 1)
                        self.assertEqual(command.call_args.args[0][:2], ["image", "inspect"])
                    self.assertFalse(store.state["attempts"][0]["termination_confirmed"])

    def test_preparation_timeout_survives_restart_and_blocks_next_launch(self):
        with tempfile.TemporaryDirectory() as tmp:
            with AttemptStore(tmp, self.binding, Limits(32, 90, 3600)) as store:
                adapter = self.adapter(store)
                with patch.object(adapter, "_cmd", side_effect=subprocess.TimeoutExpired("docker", 10)):
                    with self.assertRaises(subprocess.TimeoutExpired):
                        adapter.prepare(self.request())
            self.assertEqual(read_record(Path(tmp) / "attempt" / "preparation.json")
                             ["deadline_scope"], "preparation_and_run")
            with AttemptStore(tmp, self.binding, Limits(32, 90, 3600)) as store:
                self.assertEqual(len(store.state["attempts"]), 1)
                with self.assertRaises(BudgetBlocked):
                    store.reserve("next", "next-container", 10)

    def test_unreachable_container_cannot_close_reservation(self):
        with tempfile.TemporaryDirectory() as tmp:
            with AttemptStore(tmp, self.binding, Limits(32, 90, 3600)) as store:
                store.reserve("attempt", "owned", 10)
                (Path(tmp) / "attempt").mkdir()
                adapter = self.adapter(store)
                failure = subprocess.CalledProcessError(1, "docker", stderr=b"unreachable")
                with patch.object(adapter, "_cmd", side_effect=failure):
                    result = adapter.cancel(WorkloadHandle("attempt", "owned"))
                self.assertFalse(result.terminated)
                store.finish("attempt", "owned", "execution_error", terminated=result.terminated)
                with self.assertRaises(BudgetBlocked):
                    store.reserve("next", "next-container", 10)
