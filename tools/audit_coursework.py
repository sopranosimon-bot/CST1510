"""Inspect supplied material without executing or modifying teaching examples."""

import ast
import json
import warnings
from datetime import datetime, timezone
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]


def main():
    """Report the files read, syntax findings and unfinished optional exercises."""
    entries = []
    for week in sorted(ROOT.glob("Week *")):
        for path in sorted(week.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            if path.suffix not in (".py", ".md", ".ipynb", ".txt", ".csv"):
                continue
            text = path.read_text(encoding="utf-8")
            entry = {"path": str(path.relative_to(ROOT)), "lines": len(text.splitlines())}
            if path.suffix == ".ipynb":
                with warnings.catch_warnings(record=True) as caught:
                    book = nbformat.reads(text, as_version=4)
                    nbformat.validate(book)
                entry["schema"] = "valid"
                entry["warnings"] = list(dict.fromkeys(str(w.message) for w in caught))
                entry["syntax_findings"] = []
                entry["unfilled_code_cells"] = []
                for index, cell in enumerate(book.cells):
                    if cell.cell_type != "code":
                        continue
                    try:
                        tree = ast.parse(cell.source)
                        if not tree.body:
                            entry["unfilled_code_cells"].append(index)
                    except SyntaxError as error:
                        entry["syntax_findings"].append({"cell": index, "error": str(error)})
            elif path.suffix == ".py":
                try:
                    ast.parse(text)
                    entry["syntax"] = "valid"
                except SyntaxError as error:
                    entry["syntax"] = str(error)
            entries.append(entry)
    report = {"timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "scope": "Static inspection; instructor error demonstrations are not runtime failures",
              "files": entries}
    target = ROOT / ".review" / "coursework_audit.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Read {len(entries)} instruction, source, notebook and data files.")
    for entry in entries:
        if entry.get("syntax_findings") or entry.get("syntax", "valid") != "valid":
            print(entry["path"], entry.get("syntax_findings", entry.get("syntax")))
    print(f"Full inspection report: {target}")


if __name__ == "__main__":
    main()
