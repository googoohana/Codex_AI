import io
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tools.check_comfy_cloud_connection import check_connection, write_report


class FakeResponse:
    def __init__(self, payload: dict, status: int = 200) -> None:
        self.payload = payload
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *args) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


class CheckComfyCloudConnectionTests(unittest.TestCase):
    def test_missing_api_key_is_blocked_without_network_call(self) -> None:
        called = False

        def opener(request, timeout):
            nonlocal called
            called = True
            return FakeResponse({})

        result = check_connection("", opener=opener)

        self.assertEqual(result.status, "blocked")
        self.assertFalse(called)
        self.assertIn("환경 변수", result.message)

    def test_readonly_check_uses_system_stats_and_api_key_header(self) -> None:
        captured = {}

        def opener(request, timeout):
            captured["url"] = request.full_url
            captured["key"] = request.get_header("X-api-key")
            captured["timeout"] = timeout
            return FakeResponse({"system": {"os": "cloud"}})

        result = check_connection("private-test-key", opener=opener)

        self.assertEqual(result.status, "connected")
        self.assertEqual(captured["url"], "https://cloud.comfy.org/api/system_stats")
        self.assertEqual(captured["key"], "private-test-key")
        self.assertEqual(captured["timeout"], 10)
        self.assertNotIn("private-test-key", result.message)

    def test_report_does_not_contain_api_key(self) -> None:
        with TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "REPORT.md"

            result = check_connection(
                "private-test-key",
                opener=lambda request, timeout: FakeResponse({"ok": True}),
            )
            write_report(result, report_path)
            report = report_path.read_text(encoding="utf-8-sig")

        self.assertNotIn("private-test-key", report)
        self.assertIn("실제 생성 작업 제출: 하지 않음", report)


if __name__ == "__main__":
    unittest.main()
