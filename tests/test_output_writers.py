import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from wow import output as output_module


class OutputWriterTests(unittest.TestCase):
    def test_write_timeline_output_creates_asset_json_in_cwd(self):
        original_cwd = os.getcwd()
        temp_dir = tempfile.TemporaryDirectory()

        try:
            os.chdir(temp_dir.name)

            payload = [{"character_name": "SmokeTest", "type": "item"}]
            output_module.write_timeline_output(payload)

            timeline_path = Path("asset/timeline.json")
            self.assertTrue(timeline_path.exists())
            self.assertTrue(Path("asset").is_dir())

            with timeline_path.open("r", encoding="utf-8") as handle:
                written = json.load(handle)

            self.assertEqual(written, payload)
            self.assertIn("asset/timeline.json", str(timeline_path).replace("\\", "/"))
        finally:
            os.chdir(original_cwd)
            temp_dir.cleanup()

    def test_write_api_status_output_writes_asset_json_next_to_module(self):
        temp_dir = tempfile.TemporaryDirectory()
        original_module_file = output_module.__file__

        try:
            fake_module_file = str(Path(temp_dir.name) / "wow" / "output.py")
            Path(fake_module_file).parent.mkdir(parents=True, exist_ok=True)

            with mock.patch.object(output_module, "__file__", fake_module_file), mock.patch(
                "builtins.print"
            ):
                output_module.write_api_status_output(
                    ok=True,
                    code=200,
                    message="All good",
                    source="unit_test",
                )

            api_status_path = Path(temp_dir.name) / "asset" / "api_status.json"
            self.assertTrue(api_status_path.exists())

            with api_status_path.open("r", encoding="utf-8") as handle:
                written = json.load(handle)

            self.assertEqual(written["ok"], True)
            self.assertEqual(written["code"], 200)
            self.assertEqual(written["source"], "unit_test")
            self.assertEqual(written["message"], "All good")
            self.assertIn("updated_at", written)
        finally:
            output_module.__file__ = original_module_file
            temp_dir.cleanup()


if __name__ == "__main__":
    unittest.main()
