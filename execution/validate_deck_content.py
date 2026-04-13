from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "deck_content.schema.json"


def load_schema() -> dict[str, Any]:
    with SCHEMA_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def _build_validator() -> Draft202012Validator:
    return Draft202012Validator(load_schema())


def _collect_schema_errors(payload: dict[str, Any]) -> list[str]:
    validator = _build_validator()
    errors = []
    for error in sorted(validator.iter_errors(payload), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{location}: {error.message}")
    return errors


def _collect_evidence_errors(payload: dict[str, Any]) -> list[str]:
    evidence_ids = {item["id"] for item in payload.get("evidence", []) if isinstance(item, dict) and "id" in item}
    errors: list[str] = []

    for section_name in ("objectives", "action_items"):
        for index, item in enumerate(payload.get(section_name, [])):
            for evidence_id in item.get("evidence_ids", []):
                if evidence_id not in evidence_ids:
                    errors.append(
                        f"{section_name}[{index}] references missing evidence id '{evidence_id}'"
                    )
    return errors


def validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    errors = _collect_schema_errors(payload)
    if not errors:
        errors.extend(_collect_evidence_errors(payload))

    return {
        "valid": not errors,
        "errors": errors,
    }


def validate_file(input_path: str | Path, output_path: str | Path | None = None) -> dict[str, Any]:
    input_file = Path(input_path)
    with input_file.open(encoding="utf-8") as handle:
        payload = json.load(handle)

    result = validate_payload(payload)
    result["input_path"] = str(input_file)

    if output_path is not None:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open("w", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2)
            handle.write("\n")

    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate deck content JSON against the repo schema.")
    parser.add_argument("input_path", help="Path to the deck content JSON file.")
    parser.add_argument("--output", dest="output_path", help="Optional report output path.")
    args = parser.parse_args()

    report = validate_file(args.input_path, args.output_path)
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["valid"] else 1)

