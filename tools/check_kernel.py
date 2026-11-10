"""Execute a real notebook twice in the project's Python 3.12 Jupyter kernel."""

import json
import asyncio
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parents[1]
KERNEL = "cst1510-py312"


def main():
    """Check the kernel executable, imports and real cell execution."""
    assert sys.version_info[:2] == (3, 12), sys.version
    expected = ROOT / ".venv" / "Scripts" / "python.exe"
    assert Path(sys.executable).resolve() == expected.resolve(), sys.executable
    spec = KernelSpecManager().get_kernel_spec(KERNEL)
    assert Path(spec.argv[0]).resolve() == expected.resolve(), spec.argv
    artifact_dir = ROOT / ".review"
    artifact_dir.mkdir(exist_ok=True)
    # Keep runtime files and plotting caches inside this project.
    os.environ.setdefault("JUPYTER_RUNTIME_DIR", str(artifact_dir / "runtime"))
    os.environ.setdefault("IPYTHONDIR", str(artifact_dir / "ipython"))
    os.environ.setdefault("MPLCONFIGDIR", str(artifact_dir / "matplotlib"))
    for folder in ("runtime", "ipython", "matplotlib"):
        (artifact_dir / folder).mkdir(exist_ok=True)
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    source = f'''import sys
import importlib
from importlib.metadata import version
from pathlib import Path
assert sys.version_info[:2] == (3, 12), sys.version
assert Path(sys.executable).resolve() == Path({str(expected)!r}).resolve()
packages = ["ipykernel", "pandas", "matplotlib", "requests", "bcrypt", "streamlit", "openai", "pytest"]
for package in packages:
    importlib.import_module(package)
print("Interpreter:", sys.executable)
print("Python:", sys.version.split()[0])
print("Packages:", {{package: version(package) for package in packages}})
assert 6 * 7 == 42
print("KERNEL SMOKE TEST PASSED")'''
    runs = []
    for number in (1, 2):
        book = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(source)])
        book.metadata.kernelspec = {
            "display_name": "Python 3.12 (CST1510 .venv)",
            "language": "python", "name": KERNEL,
        }
        NotebookClient(book, kernel_name=KERNEL, timeout=60,
                       resources={"metadata": {"path": str(ROOT)}}).execute()
        output = "".join(item.get("text", "") for item in book.cells[0].outputs)
        assert "KERNEL SMOKE TEST PASSED" in output, output
        nbformat.write(book, artifact_dir / f"kernel_smoke_{number}.ipynb")
        runs.append({"fresh_kernel": number, "output": output})
        print(f"Fresh kernel {number}: PASS")
        print(output, end="")
    report = {"timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "kernel": KERNEL, "runs": runs}
    (artifact_dir / "kernel_smoke.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
