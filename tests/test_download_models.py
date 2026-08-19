from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from huggingface_hub._local_folder import get_local_download_paths

from download_models import (
    GIB,
    SAFETY_MARGIN_BYTES,
    DownloadPlan,
    ModelFile,
    build_download_plan,
    ensure_disk_space,
    is_required_path,
)


class DownloadPlanTests(unittest.TestCase):
    def test_required_path_filter(self) -> None:
        self.assertTrue(is_required_path("v0Q.ckpt"))
        self.assertTrue(is_required_path("llava-v1.5-7b/config.json"))
        self.assertFalse(is_required_path("checkpoints/optional.safetensors"))

    def test_fresh_download_requires_remaining_bytes_plus_margin(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            files = [
                ModelFile("one.bin", 10 * GIB, "etag-one"),
                ModelFile("two.bin", 5 * GIB, "etag-two"),
            ]
            plan = build_download_plan(Path(directory), files)

        self.assertEqual(plan.remaining_bytes, 15 * GIB)
        self.assertEqual(plan.partial_bytes, 0)
        self.assertEqual(plan.required_free_bytes, 15 * GIB + SAFETY_MARGIN_BYTES)

    def test_completed_and_partial_files_reduce_remaining_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            completed = ModelFile("complete.bin", 10, "etag-complete")
            partial = ModelFile("nested/partial.bin", 1_000, "etag-partial")
            (target / completed.path).write_bytes(b"x" * completed.size)
            paths = get_local_download_paths(target, partial.path)
            incomplete = paths.incomplete_path(partial.etag)
            incomplete.parent.mkdir(parents=True, exist_ok=True)
            incomplete.write_bytes(b"x" * 600)

            plan = build_download_plan(target, [completed, partial])

        self.assertEqual(plan.completed_files, 1)
        self.assertEqual(plan.pending_files, 1)
        self.assertEqual(plan.partial_bytes, 600)
        self.assertEqual(plan.remaining_bytes, 400)
        self.assertEqual(plan.required_free_bytes, 1_000 + SAFETY_MARGIN_BYTES)

    def test_all_complete_requires_no_free_space_reserve(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            file = ModelFile("complete.bin", 4, "etag")
            (target / file.path).write_bytes(b"done")
            plan = build_download_plan(target, [file])

        self.assertEqual(plan.pending_files, 0)
        self.assertEqual(plan.required_free_bytes, 0)

    def test_wrong_final_size_stops_before_download(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            file = ModelFile("broken.bin", 10, "etag")
            (target / file.path).write_bytes(b"bad")
            with self.assertRaisesRegex(SystemExit, "unexpected size"):
                build_download_plan(target, [file])

    def test_insufficient_space_reports_current_requirement(self) -> None:
        plan = DownloadPlan(10, 10, 0, 8 * GIB, 0, 1)
        with self.assertRaisesRegex(SystemExit, "8.0 GiB currently required"):
            ensure_disk_space(Path("."), plan, free_bytes=7 * GIB)


if __name__ == "__main__":
    unittest.main()
