from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.create_episode import create_episode, normalize_episode_id


TEMPLATE_NAMES = (
    "EP##_DESIGN.md",
    "EP##_SCRIPT.md",
    "EP##_CHARACTER_BIBLE.md",
    "EP##_SHOT_PLAN.md",
    "EP##_IMAGE_PROMPTS.md",
)


class CreateEpisodeTests(unittest.TestCase):
    def test_episode_id_is_normalized(self) -> None:
        self.assertEqual(normalize_episode_id("2"), "EP02")
        self.assertEqual(normalize_episode_id("ep2"), "EP02")
        self.assertEqual(normalize_episode_id("EP02"), "EP02")

    def test_episode_workspace_is_created_from_templates(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            templates_dir = project_root / "templates"
            templates_dir.mkdir()
            for template_name in TEMPLATE_NAMES:
                (templates_dir / template_name).write_text(
                    f"# {template_name}\nEP## placeholder\n",
                    encoding="utf-8-sig",
                )

            episode_dir = create_episode(project_root, "ep2")

            self.assertEqual(episode_dir, project_root / "episodes" / "EP02")
            for template_name in TEMPLATE_NAMES:
                output_name = template_name.replace("EP##", "EP02")
                output_path = episode_dir / output_name
                self.assertTrue(output_path.exists())
                self.assertNotIn(
                    "EP##",
                    output_path.read_text(encoding="utf-8-sig"),
                )

            expected_leaf_dirs = (
                "reference_assets/characters",
                "reference_assets/locations",
                "images_gpt",
                "video_generations/kling",
                "video_generations/seedance",
                "video_generations/grok",
                "videos_grok_480p_6s",
                "final_tts_subtitles",
                "story_sync_audit",
                "DOWNLOAD_READY",
            )
            for relative_dir in expected_leaf_dirs:
                self.assertTrue((episode_dir / relative_dir / ".gitkeep").exists())

            reference_guide = episode_dir / "reference_assets" / "README.md"
            video_guide = episode_dir / "video_generations" / "README.md"
            self.assertTrue(reference_guide.exists())
            self.assertTrue(video_guide.exists())
            self.assertIn("EP02", reference_guide.read_text(encoding="utf-8-sig"))
            self.assertIn("EP02", video_guide.read_text(encoding="utf-8-sig"))

    def test_existing_episode_is_not_overwritten(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            existing_dir = project_root / "episodes" / "EP02"
            existing_dir.mkdir(parents=True)

            with self.assertRaisesRegex(FileExistsError, "이미 존재합니다"):
                create_episode(project_root, "EP02")

    def test_invalid_episode_id_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "에피소드 번호"):
            normalize_episode_id("episode-two")
        with self.assertRaisesRegex(ValueError, "1 이상"):
            normalize_episode_id("0")


if __name__ == "__main__":
    unittest.main()
