"""Run lab notebooks in real kernels with explicitly labelled automated inputs."""

import argparse
import asyncio
import hashlib
import json
import os
import shutil
import tempfile
import sys
from datetime import datetime, timezone
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
KERNEL = "cst1510-py312"
INPUTS = {
    1: ["Automated review fixture", "R-TEST", "41.2", "50"],
    2: ["5", "10", "2.5", "done", "1", "2", "3", "wrong", "letmein"],
    3: [], 4: [], 5: [], 6: [], 7: [],
}


def lab_dir(week):
    """Locate one week's lab without relying on the current working directory."""
    return next(ROOT.glob(f"Week {week:02d}*/LAB"))


def execute_week(week, write=False):
    """Execute in an isolated copy of the lab; optionally save genuine outputs."""
    artifact_dir = ROOT / ".review"
    artifact_dir.mkdir(exist_ok=True)
    for variable, folder in (("IPYTHONDIR", "ipython"),
                             ("MPLCONFIGDIR", "matplotlib"),
                             ("JUPYTER_RUNTIME_DIR", "runtime")):
        target = artifact_dir / folder
        target.mkdir(exist_ok=True)
        os.environ.setdefault(variable, str(target))
    os.environ.setdefault("MPLBACKEND", "Agg")
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    path = lab_dir(week) / f"W{week:02d}_Lab.ipynb"
    book = nbformat.read(path, as_version=4)
    nbformat.validate(book)
    original_ids = [cell.id for cell in book.cells]
    setup_source = f'''# Test harness only: this cell is removed before outputs are saved.
_review_inputs = iter({INPUTS[week]!r})
def _review_input(prompt=""):
    try:
        value = next(_review_inputs)
    except StopIteration:
        raise AssertionError("The notebook requested more inputs than its test fixture provides")
    print("[AUTOMATED TEST INPUT] " + prompt + value)
    return value
input = _review_input
'''
    book.cells.insert(0, nbformat.v4.new_code_cell(setup_source))
    finish = '''assert next(_review_inputs, None) is None, "Unused automated test inputs"
print("[AUTOMATED TEST] All supplied inputs consumed")'''
    book.cells.append(nbformat.v4.new_code_cell(finish))
    with tempfile.TemporaryDirectory(prefix=f"cst1510-w{week:02d}-") as temporary:
        work = Path(temporary) / "LAB"
        shutil.copytree(lab_dir(week), work)
        NotebookClient(book, kernel_name=KERNEL, timeout=60,
                       resources={"metadata": {"path": str(work)}}).execute()
        book.cells = book.cells[1:-1]
        assert [cell.id for cell in book.cells] == original_ids
        if week in (4, 6):
            artifacts = {4: ("notes.txt",), 6: ("records_report.csv", "status_counts.png")}
            for filename in artifacts[week]:
                produced = work / filename
                assert produced.is_file() and produced.stat().st_size > 0, filename
                if write:
                    shutil.copy2(produced, lab_dir(week) / filename)
    book.metadata["cst1510_review"] = {
        "ai_assisted": True, "execution": "automated synthetic fixtures",
        "inputs": INPUTS[week], "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "kernel": KERNEL, "not_independent_student_evidence": True,
        "source_sha256": hashlib.sha256(json.dumps(
            [cell.source for cell in book.cells], ensure_ascii=False
        ).encode("utf-8")).hexdigest(),
    }
    nbformat.validate(book)
    nbformat.write(book, artifact_dir / f"W{week:02d}_executed.ipynb")
    if write:
        nbformat.write(book, path)
    print(f"Week {week}: real-kernel execution PASS ({len(book.cells)} cells)")
    return book


def main():
    """Execute selected weeks in ascending order."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--week", type=int, choices=range(1, 8), action="append")
    parser.add_argument("--write", action="store_true",
                        help="Save actual outputs into the lab notebooks")
    args = parser.parse_args()
    for week in sorted(set(args.week or range(1, 8))):
        execute_week(week, write=args.write)


if __name__ == "__main__":
    main()
