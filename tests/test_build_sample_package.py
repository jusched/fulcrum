import json
import tempfile
import unittest
from pathlib import Path

from execution.build_sample_package import build_package
from tests.support import make_metadata, write_temp_transcript


class BuildSamplePackageTests(unittest.TestCase):
    def test_builds_summary_package_from_transcript(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            transcript_path = write_temp_transcript(temp_path)
            metadata_path = temp_path / "meeting_metadata.json"
            metadata_path.write_text(json.dumps(make_metadata()), encoding="utf-8")
            output_dir = temp_path / "artifacts"

            result = build_package(transcript_path, metadata_path, output_dir, mode="sample")

            self.assertTrue(result["validation"]["valid"])
            self.assertTrue((output_dir / "deck_content.json").exists())
            self.assertTrue((output_dir / "validation_report.json").exists())
            self.assertTrue((output_dir / "executive_summary.md").exists())
            self.assertTrue((output_dir / "meeting_deck.pptx").exists())

    def test_sanitizes_control_characters_from_transcript_evidence(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            transcript_path = temp_path / "meeting_transcript.txt"
            transcript_path.write_text(
                "Sarah said: I\u0019d also want some very basic cost estimate before we commit.",
                encoding="utf-8",
            )
            metadata_path = temp_path / "meeting_metadata.json"
            metadata_path.write_text(json.dumps(make_metadata()), encoding="utf-8")
            output_dir = temp_path / "artifacts"

            build_package(transcript_path, metadata_path, output_dir, mode="sample")

            payload = json.loads((output_dir / "deck_content.json").read_text(encoding="utf-8"))
            quotes = [item["quote"] for item in payload["evidence"]]
            self.assertTrue(any("I'd also want some very basic cost estimate" in quote for quote in quotes))
            self.assertFalse(any("\u0019" in quote for quote in quotes))


if __name__ == "__main__":
    unittest.main()
