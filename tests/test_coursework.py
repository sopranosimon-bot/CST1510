"""Automated software checks; these do not attest to independent student work."""

import ast
import base64
import hashlib
import json
import subprocess
import runpy
import re
import warnings
import sys
from pathlib import Path

import pytest
import nbformat

ROOT = Path(__file__).resolve().parents[1]


def lab(week):
    return next(ROOT.glob(f"Week {week:02d}*/LAB"))


def run_file(path, answers=(), cwd=None):
    return subprocess.run([sys.executable, str(path)],
                          input="\n".join(answers) + "\n", text=True,
                          capture_output=True, timeout=20, cwd=cwd or path.parent)


@pytest.mark.parametrize("used,total,free,percent", [
    ("87", "120", "33.00", "72.50"),
    ("125.5", "100", "-25.50", "125.50"),
    ("0", "80", "80.00", "0.00"),
])
def test_week1_report(used, total, free, percent, tmp_path):
    result = run_file(lab(1) / "template.py", ["test-host", used, total], tmp_path)
    assert result.returncode == 0, result.stderr
    lines = result.stdout.splitlines()
    assert "  Free        : " + f"{free:>10}" in lines
    assert "  Percent     : " + f"{percent:>10}" + " %" in lines
    assert result.stdout.count("=" * 34) == 3
    assert "test-host" in result.stdout


def test_week1_keeps_required_zero_total_error():
    result = run_file(lab(1) / "template.py", ["test-host", "1", "0"])
    assert result.returncode != 0
    assert "ZeroDivisionError" in result.stderr


def test_week1_uses_only_week1_constructs():
    tree = ast.parse((lab(1) / "template.py").read_text(encoding="utf-8"))
    assert not any(isinstance(node, (ast.If, ast.For, ast.While, ast.FunctionDef,
                                     ast.List, ast.Dict, ast.Try)) for node in ast.walk(tree))


@pytest.mark.parametrize("filename,answers,expected", [
    ("01_name_error.py", [], "R-004"),
    ("02_type_error.py", ["23.7"], "24.7"),
    ("03_value_error.py", ["23.7"], "23.7"),
])
def test_week1_warmups(filename, answers, expected):
    result = run_file(lab(1) / "warmup" / filename, answers)
    assert result.returncode == 0, result.stderr
    assert expected in result.stdout


def test_week1_executed_outputs():
    book = nbformat.read(lab(1) / "W01_Lab.ipynb", as_version=4)
    output = "".join(item.get("text", "") for cell in book["cells"]
                     for item in cell.get("outputs", []))
    assert "4831 seconds = 1 hours, 20 minutes, 31 seconds" in output
    assert "     -8.80" in output
    assert "     82.40 %" in output
    assert "[AUTOMATED TEST INPUT]" in output
    assert not any(item.get("output_type") == "error" for cell in book["cells"]
                   for item in cell.get("outputs", []))


@pytest.mark.parametrize("value,status", [
    (0, "OK"), (87, "OK"), (89.99, "OK"), (90, "WARNING"),
    (95, "WARNING"), (99.99, "WARNING"), (100, "OVER LIMIT"), (120, "OVER LIMIT"),
])
def test_week2_status_boundaries(value, status, tmp_path):
    result = run_file(lab(2) / "template.py", ["test-host", str(value), "100"], tmp_path)
    assert result.returncode == 0, result.stderr
    assert f"  Status      : {status:>10}" in result.stdout
    assert f"{100 - value:>10.2f}" in result.stdout
    assert f"{value:>10.2f} %" in result.stdout


def test_week2_zero_total_is_required_failure():
    result = run_file(lab(2) / "template.py", ["test-host", "87", "0"])
    assert result.returncode != 0 and "ZeroDivisionError" in result.stderr


def test_week2_notebook_loop_results():
    book = nbformat.read(lab(2) / "W02_Lab.ipynb", as_version=4)
    outputs = {cell.source.splitlines()[0]: "".join(o.get("text", "") for o in cell.outputs)
               for cell in book.cells if cell.cell_type == "code"}
    assert outputs["# D9"].splitlines() == [str(n) for n in range(1, 11)]
    assert outputs["# D10"].splitlines() == [str(n) for n in range(1, 6)]
    assert outputs["# D12"].splitlines() == [str(n) for n in range(1, 11) if n != 5]
    assert "Total: 17.5" in outputs["# D11"]
    assert outputs["# D16"].endswith("Welcome\n")


@pytest.mark.parametrize("value,total,difference,percent,status", [
    (87, 120, 33, 72.5, "OK"), (90, 100, 10, 90, "WARNING"),
    (100, 100, 0, 100, "OVER LIMIT"), (120, 100, -20, 120, "OVER LIMIT"),
])
def test_week3_pure_functions_and_cli(value, total, difference, percent, status):
    functions = runpy.run_path(str(lab(3) / "template.py"), run_name="review_import")
    actual_difference, actual_percent = functions["check"](value, total)
    assert actual_difference == pytest.approx(difference)
    assert actual_percent == pytest.approx(percent)
    assert functions["status_of"](actual_percent) == status
    result = run_file(lab(3) / "template.py", ["test-host", str(value), str(total)])
    assert result.returncode == 0, result.stderr
    assert f"  Status      : {status:>10}" in result.stdout


def test_week3_required_zero_error():
    functions = runpy.run_path(str(lab(3) / "template.py"), run_name="review_import")
    with pytest.raises(ZeroDivisionError):
        functions["check"](1, 0)


def test_week3_scope_exercise_has_exactly_its_expected_error():
    book = nbformat.read(lab(3) / "W03_Lab.ipynb", as_version=4)
    errors = [(cell.source.splitlines()[0], item.get("ename")) for cell in book.cells
              for item in cell.get("outputs", []) if item.output_type == "error"]
    assert errors == [("# D9", "NameError")]


def test_week4_file_loading_and_reports(tmp_path):
    functions = runpy.run_path(str(lab(4) / "template.py"), run_name="review_import")
    fixture = tmp_path / "records.txt"
    fixture.write_text("test-a,87,120\ntest-b,95,100\ntest-c,120,100\n", encoding="utf-8")
    records = functions["load_records"](fixture)
    assert records == [
        {"label": "test-a", "value": 87.0, "limit": 120.0},
        {"label": "test-b", "value": 95.0, "limit": 100.0},
        {"label": "test-c", "value": 120.0, "limit": 100.0},
    ]
    assert [functions["check_record"](r["value"], r["limit"])[2] for r in records] == [
        "OK", "WARNING", "OVER LIMIT"]
    result = run_file(lab(4) / "template.py", cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert result.stdout.count("RECORD CHECK") == 5
    assert "33.00" in result.stdout and "72.50 %" in result.stdout
    with pytest.raises(FileNotFoundError):
        functions["load_records"](tmp_path / "not-there.txt")


def test_week4_notebook_generated_file():
    assert (lab(4) / "notes.txt").read_text(encoding="utf-8") == "R-001\nR-002\n"


@pytest.mark.parametrize("value,status", [
    (0, "OK"), (89.99, "OK"), (90, "WARNING"), (99.99, "WARNING"),
    (100, "OVER LIMIT"), (120, "OVER LIMIT"),
])
def test_week5_object_status(value, status):
    Record = runpy.run_path(str(lab(5) / "template.py"), run_name="review_import")["Record"]
    assert Record("test-a", value, 100).status() == status


def test_week5_independent_objects_and_cli(tmp_path):
    Record = runpy.run_path(str(lab(5) / "template.py"), run_name="review_import")["Record"]
    first = Record("test-a", 10, 100)
    second = Record("test-b", 20, 100)
    first.value = 120
    assert first.status() == "OVER LIMIT"
    assert second.value == 20 and second.status() == "OK"
    result = run_file(lab(5) / "template.py", cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert result.stdout.count("RECORD CHECK") == 3
    assert "WARNING" in result.stdout and "OVER LIMIT" in result.stdout


def test_week6_vectorized_status_and_filter(tmp_path, capsys):
    script = tmp_path / "template.py"
    script.write_text((lab(6) / "template.py").read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "servers.csv").write_text(
        "hostname,used_gb,total_gb\nzero,0,100\nbelow,89.99,100\n"
        "warning,90,100\nalmost,99.99,100\nexact,100,100\nover,120,100\n",
        encoding="utf-8")
    data = runpy.run_path(str(script))["df"]
    assert data["status"].tolist() == ["OK", "OK", "WARNING", "WARNING", "OVER LIMIT", "OVER LIMIT"]
    filtered_output = capsys.readouterr().out.split("Records needing attention:")[1]
    assert "zero" not in filtered_output and "below" not in filtered_output
    assert all(host in filtered_output for host in ("warning", "almost", "exact", "over"))
    tree = ast.parse(script.read_text(encoding="utf-8"))
    assert not any(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))


def test_week6_generated_report_and_chart():
    import pandas as pd
    from PIL import Image
    report = pd.read_csv(lab(6) / "records_report.csv")
    assert report["percent"].tolist() == [87, 120, 45, 93, 101, 60]
    assert report["status"].value_counts().to_dict() == {"OK": 3, "OVER LIMIT": 2, "WARNING": 1}
    assert not any(name.startswith("Unnamed") for name in report.columns)
    with Image.open(lab(6) / "status_counts.png") as chart:
        chart.verify()


@pytest.mark.parametrize("raw,expected,status", [
    ("  SRV-TEST , USED=87 , TOTAL=120  ", {"hostname": "srv-test", "used": 87.0, "total": 120.0}, "OK"),
    ("Srv-Test,TOTAL=100, used = 90", {"hostname": "srv-test", "total": 100.0, "used": 90.0}, "WARNING"),
    ("srv-TEST,used=100,total=100", {"hostname": "srv-test", "used": 100.0, "total": 100.0}, "OVER LIMIT"),
    ("srv-test,used=0,total=100", {"hostname": "srv-test", "used": 0.0, "total": 100.0}, "OK"),
    ("srv-test,used=120.5,total=100", {"hostname": "srv-test", "used": 120.5, "total": 100.0}, "OVER LIMIT"),
])
def test_week7_messy_record_parsing(raw, expected, status):
    functions = runpy.run_path(str(lab(7) / "template.py"), run_name="review_import")
    record = functions["parse_line"](raw)
    assert record == expected
    assert functions["status_of"](record["used"], record["total"]) == status


@pytest.mark.parametrize("raw", ["srv-test,used=unknown,total=100", "srv-test,used=1=2,total=100", "bad-record"])
def test_week7_invalid_numbers_are_visible(raw):
    functions = runpy.run_path(str(lab(7) / "template.py"), run_name="review_import")
    with pytest.raises(ValueError):
        functions["parse_line"](raw)


def test_week7_cli_contains_at_least_five_messy_examples(tmp_path):
    result = run_file(lab(7) / "template.py", cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert len(result.stdout.splitlines()) >= 5
    assert "WARNING" in result.stdout and "OVER LIMIT" in result.stdout


@pytest.mark.parametrize("week,filename,answers,expected", [
    (2, "01_indentation_error.py", [], "OVER"),
    (2, "02_syntax_error.py", [], "checking..."),
    (2, "03_type_error.py", ["23.7"], "OVER"),
    (3, "01_missing_argument.py", [], "WARNING"),
    (3, "02_scope_error.py", [], "OK"),
    (3, "03_import_error.py", [], "4.0"),
    (4, "01_index_error.py", [], "R-003"),
    (4, "02_key_error.py", [], "not checked"),
    (4, "03_file_not_found_error.py", [], "R-001,87,100"),
    (5, "01_missing_self.py", [], "95"),
    (5, "02_attribute_error.py", [], "87.0"),
    (5, "03_name_error.py", [], "OVER LIMIT"),
    (6, "01_key_error.py", [], "120"),
    (6, "02_value_error.py", [], ""),
    (6, "03_type_error.py", [], ""),
    (7, "01_value_error_unpack.py", [], "note server=east"),
    (7, "02_attribute_error.py", [], "87.0"),
    (7, "03_value_error_float.py", [], "used: not a number (unknown)"),
])
def test_remaining_warmups(week, filename, answers, expected, tmp_path):
    result = run_file(lab(week) / "warmup" / filename, answers, tmp_path)
    assert result.returncode == 0, result.stderr
    assert expected in result.stdout


@pytest.mark.parametrize("week,count", [(1, 6), (2, 16), (3, 15), (4, 16), (5, 11), (6, 14), (7, 15)])
def test_regular_drills_are_filled_and_executed(week, count):
    book = nbformat.read(lab(week) / f"W{week:02d}_Lab.ipynb", as_version=4)
    nbformat.validate(book)
    found = set()
    for cell in book.cells:
        match = re.match(r"# D(\d+)\b", cell.source) if cell.cell_type == "code" else None
        if match and int(match[1]) <= count:
            assert ast.parse(cell.source).body, match[0]
            assert cell.execution_count is not None, match[0]
            found.add(int(match[1]))
    assert found == set(range(1, count + 1))
    assert book.metadata.kernelspec.name == "cst1510-py312"
    assert book.metadata.cst1510_review.not_independent_student_evidence
    assert book.metadata.cst1510_review.hash_scope == "code_cells"
    digest = hashlib.sha256(json.dumps([cell.source for cell in book.cells if cell.cell_type == "code"],
                            ensure_ascii=False).encode("utf-8")).hexdigest()
    assert book.metadata.cst1510_review.source_sha256 == digest, "Rerun the notebook after code changes"


@pytest.mark.parametrize("week", range(1, 8))
def test_instructions_are_preserved_and_only_supplied_photos_are_added(week):
    path = lab(week) / f"W{week:02d}_Lab.ipynb"
    relative = path.relative_to(ROOT).as_posix()
    original = subprocess.run(["git", "show", f"d0ccc19:{relative}"], cwd=ROOT,
                              capture_output=True, check=True).stdout.decode("utf-8")
    # The supplied notebooks predate mandatory cell IDs; normalize in memory only.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", nbformat.warnings.MissingIDFieldWarning)
        before = nbformat.reads(original, as_version=4)
    after = nbformat.read(path, as_version=4)
    manifest = json.loads((ROOT / "NOTE_PHOTOS.json").read_text(encoding="utf-8"))
    photos = [photo for photo in manifest["photos"] if photo["week"] == week]
    assert len(photos) == (2 if week == 3 else 1)
    assert len(before.cells) == len(after.cells)
    for index, (old, new) in enumerate(zip(before.cells, after.cells)):
        if old.cell_type == "markdown":
            if index == 0:
                assert new.source.startswith(old.source)
            elif "*(paste here)*" in old.source:
                links = [f"![User-provided handwritten notes - Week {week}, photo {number}]"
                         f"(attachment:{photo['attachment']})"
                         for number, photo in enumerate(photos, start=1)]
                replacement = "\n\n".join(links) + "\n\n*Original photographs supplied by the student; kept unchanged.*"
                assert new.source == old.source.replace("*(paste here)*", replacement)
                assert set(new.attachments) == {photo["attachment"] for photo in photos}
                for photo in photos:
                    content = base64.b64decode(new.attachments[photo["attachment"]]["image/jpeg"], validate=True)
                    assert hashlib.sha256(content).hexdigest() == photo["sha256"]
                    assert content == (ROOT / photo["file"]).read_bytes()
            else:
                assert new.source == old.source
            if "*(paste here)*" not in old.source:
                assert new.get("attachments", {}) == old.get("attachments", {})


@pytest.mark.parametrize("week", range(1, 8))
def test_lab_python_files_compile(week):
    for path in lab(week).rglob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
