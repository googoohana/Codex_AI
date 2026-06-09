from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from tools.run_local_pipeline import run_local_pipeline


class RunLocalPipelineTests(unittest.TestCase):
    def test_ready_episode_completes_all_steps(self) -> None:
        with TemporaryDirectory() as temp_dir:
            episode_dir = Path(temp_dir) / "EP01_sample"
            shutil.copytree(Path("episodes/EP01_sample"), episode_dir)

            result = run_local_pipeline(episode_dir, refresh_generated=True)
            report = (
                episode_dir / "story_sync_audit" / "PIPELINE_RUN_REPORT.md"
            ).read_text(encoding="utf-8-sig")

        self.assertEqual(result.status, "completed")
        self.assertEqual(
            result.completed_steps,
            ("cut_list", "validation", "shot_sync_map"),
        )
        self.assertIsNone(result.stopped_step)
        self.assertIn("- 최종 상태: 완료", report)
        self.assertIn("- shot_sync_map: 생성 완료", report)
        self.assertIn("외부 AI는 아직 호출하지 않았습니다", report)

    def test_episode_with_manual_cut_split_stops_at_cut_list(self) -> None:
        with TemporaryDirectory() as temp_dir:
            episode_dir = Path(temp_dir) / "EP02"
            shutil.copytree(Path("episodes/EP02"), episode_dir)
            sync_map_path = episode_dir / "story_sync_audit" / "shot_sync_map.json"

            result = run_local_pipeline(episode_dir, refresh_generated=True)
            report = (
                episode_dir / "story_sync_audit" / "PIPELINE_RUN_REPORT.md"
            ).read_text(encoding="utf-8-sig")

        self.assertEqual(result.status, "blocked")
        self.assertEqual(result.completed_steps, ("cut_list",))
        self.assertEqual(result.stopped_step, "cut_list")
        self.assertFalse(sync_map_path.exists())
        self.assertIn("- 최종 상태: 중간 차단", report)
        self.assertIn("수동 분할 필요", report)

    def test_existing_generated_files_are_protected_without_refresh(self) -> None:
        with TemporaryDirectory() as temp_dir:
            episode_dir = Path(temp_dir) / "EP01_sample"
            shutil.copytree(Path("episodes/EP01_sample"), episode_dir)

            result = run_local_pipeline(episode_dir)

        self.assertEqual(result.status, "blocked")
        self.assertEqual(result.completed_steps, ())
        self.assertEqual(result.stopped_step, "cut_list")
        self.assertIn("이미 존재합니다", result.message)

    def test_validation_failure_warns_that_existing_sync_map_is_stale(self) -> None:
        with TemporaryDirectory() as temp_dir:
            episode_dir = Path(temp_dir) / "EP01_sample"
            shutil.copytree(Path("episodes/EP01_sample"), episode_dir)
            shot_plan_path = episode_dir / "EP01_SHOT_PLAN.md"
            shot_plan = shot_plan_path.read_text(encoding="utf-8-sig")
            shot_plan_path.write_text(
                shot_plan.replace(
                    "- review_status: ready_for_image_prompt",
                    "- review_status: draft",
                    1,
                ),
                encoding="utf-8-sig",
            )

            result = run_local_pipeline(episode_dir, refresh_generated=True)
            report = (
                episode_dir / "story_sync_audit" / "PIPELINE_RUN_REPORT.md"
            ).read_text(encoding="utf-8-sig")

        self.assertEqual(result.status, "blocked")
        self.assertEqual(result.stopped_step, "validation")
        self.assertIn("기존 shot_sync_map", report)
        self.assertIn("갱신되지 않았습니다", report)


if __name__ == "__main__":
    unittest.main()
