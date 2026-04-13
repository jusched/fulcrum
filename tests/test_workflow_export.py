import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW_PATH = REPO_ROOT / "workflows" / "meeting_to_deck.json"


class WorkflowExportTests(unittest.TestCase):
    def test_export_surfaces_review_outputs_and_errors(self):
        workflow = json.loads(WORKFLOW_PATH.read_text(encoding="utf-8"))
        node_names = {node["name"] for node in workflow["nodes"]}

        self.assertIn("Expose Intermediate Outputs", node_names)
        self.assertIn("Human Review Gate", node_names)
        self.assertIn("Approved For Distribution?", node_names)
        self.assertIn("Manual Revision Required", node_names)
        self.assertIn("Schema Validation Error", node_names)
        self.assertIn("Render Failure Error", node_names)

    def test_export_contains_human_review_and_error_notes(self):
        workflow = json.loads(WORKFLOW_PATH.read_text(encoding="utf-8"))
        sticky_notes = [node for node in workflow["nodes"] if node["type"] == "n8n-nodes-base.stickyNote"]
        note_text = "\n".join(node["parameters"].get("content", "") for node in sticky_notes)

        self.assertIn("Human review", note_text)
        self.assertIn("Error handling", note_text)
        self.assertIn("Intermediate outputs", note_text)


if __name__ == "__main__":
    unittest.main()
