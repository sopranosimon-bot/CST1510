# AI-assisted repair of the intentionally broken exercise.
# Run it, read the last line, then fix it.

from pathlib import Path

with open(Path(__file__).resolve().parents[1] / "records_sample.txt", encoding="utf-8") as f:
    print(f.read())
