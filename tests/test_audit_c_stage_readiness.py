import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.audit_c_stage_readiness import audit_readiness


class AuditCStageReadinessTests(unittest.TestCase):
    def write_config(self, directory: Path, config: dict) -> Path:
        config_path = directory / "C_STAGE_READINESS.json"
        config_path.write_text(
            json.dumps(config, ensure_ascii=False),
            encoding="utf-8",
        )
        return config_path

    def test_default_config_is_blocked_and_writes_korean_report(self) -> None:
        with TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            config_path = self.write_config(
                directory,
                {
                    "external_calls_allowed": False,
                    "dry_run_required": True,
                    "max_test_cuts": 1,
                    "max_budget_krw": 0,
                    "rights_policy": "fictional_only",
                    "seedance": {"enabled": False},
                    "kling": {"enabled": False},
                },
            )
            report_path = directory / "REPORT.md"

            result = audit_readiness(config_path, report_path)
            report = report_path.read_text(encoding="utf-8-sig")

        self.assertEqual(result.status, "blocked")
        self.assertIn("외부 호출 승인이 필요합니다.", result.issues)
        self.assertIn("최소 한 개의 영상 서비스", "\n".join(result.issues))
        self.assertIn("# C단계 진입 준비 점검 보고서", report)
        self.assertIn("- 최종 상태: 진입 차단", report)

    def test_safe_seedance_config_is_ready_without_literal_secret(self) -> None:
        with TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            config_path = self.write_config(
                directory,
                {
                    "external_calls_allowed": True,
                    "dry_run_required": True,
                    "max_test_cuts": 1,
                    "max_budget_krw": 10000,
                    "rights_policy": "fictional_only",
                    "seedance": {
                        "enabled": True,
                        "account_ready": True,
                        "api_key_env": "ARK_API_KEY",
                        "model_activated": True,
                        "prepaid_resource_pack_confirmed": True,
                        "selected_model": "seedance-2.0",
                        "selected_mode": "multimodal_reference",
                        "real_face_assets_allowed": False,
                    },
                    "kling": {"enabled": False},
                },
            )

            result = audit_readiness(config_path, directory / "REPORT.md")

        self.assertEqual(result.status, "ready")
        self.assertEqual(result.issues, ())

    def test_literal_secret_is_rejected(self) -> None:
        with TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            config_path = self.write_config(
                directory,
                {
                    "external_calls_allowed": True,
                    "dry_run_required": True,
                    "max_test_cuts": 1,
                    "max_budget_krw": 10000,
                    "rights_policy": "fictional_only",
                    "api_key": "secret-value-must-not-be-here",
                    "seedance": {"enabled": False},
                    "kling": {"enabled": False},
                },
            )

            result = audit_readiness(config_path, directory / "REPORT.md")

        self.assertEqual(result.status, "blocked")
        self.assertIn("비밀값으로 보이는 항목", "\n".join(result.issues))

    def test_kling_api_mode_requires_confirmed_official_api_access(self) -> None:
        with TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            config_path = self.write_config(
                directory,
                {
                    "external_calls_allowed": True,
                    "dry_run_required": True,
                    "max_test_cuts": 1,
                    "max_budget_krw": 10000,
                    "rights_policy": "fictional_only",
                    "seedance": {"enabled": False},
                    "kling": {
                        "enabled": True,
                        "access_mode": "api",
                        "account_ready": True,
                        "credits_budget_approved": True,
                        "official_api_access_confirmed": False,
                    },
                },
            )

            result = audit_readiness(config_path, directory / "REPORT.md")

        self.assertEqual(result.status, "blocked")
        self.assertIn("Kling 공식 API 접근 확인", "\n".join(result.issues))

    def test_safe_comfy_cloud_config_is_ready(self) -> None:
        with TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            config_path = self.write_config(
                directory,
                {
                    "external_calls_allowed": True,
                    "dry_run_required": True,
                    "max_test_cuts": 1,
                    "max_budget_krw": 10000,
                    "rights_policy": "fictional_only",
                    "seedance": {"enabled": False},
                    "kling": {"enabled": False},
                    "comfy_cloud": {
                        "enabled": True,
                        "subscription_ready": True,
                        "api_key_env": "COMFY_CLOUD_API_KEY",
                        "readonly_connection_verified": True,
                        "workflow_api_json_ready": True,
                        "estimated_credits_per_run": 20,
                        "max_credits_per_run": 20,
                    },
                },
            )

            result = audit_readiness(config_path, directory / "REPORT.md")

        self.assertEqual(result.status, "ready")
        self.assertEqual(result.issues, ())


if __name__ == "__main__":
    unittest.main()
