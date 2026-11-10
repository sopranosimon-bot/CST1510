"""Verify that original note photos are embedded intact in their lab notebooks."""

import argparse
import base64
import hashlib
import io
import json
from collections import Counter
from pathlib import Path

import nbformat
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def check_photos(source_dir=None):
    """Verify every photo reference, JPEG, archived copy and recorded checksum."""
    manifest = json.loads((ROOT / "NOTE_PHOTOS.json").read_text(encoding="utf-8"))
    photos = manifest["photos"]
    assert Counter(photo["week"] for photo in photos) == Counter({1: 1, 2: 1, 3: 2, 4: 1, 5: 1, 6: 1, 7: 1})
    for photo in photos:
        book = nbformat.read(ROOT / photo["notebook"], as_version=4)
        nbformat.validate(book)
        cells = [cell for cell in book.cells if cell.id == photo["journal_cell_id"]]
        assert len(cells) == 1, photo["original_filename"]
        journal = cells[0]
        name = photo["attachment"]
        assert f"](attachment:{name})" in journal.source, name
        assert "*(paste here)*" not in journal.source, name
        content = base64.b64decode(journal.attachments[name]["image/jpeg"], validate=True)
        assert len(content) == photo["size_bytes"], name
        assert hashlib.sha256(content).hexdigest() == photo["sha256"], name
        assert content == (ROOT / photo["file"]).read_bytes(), name
        if source_dir is not None:
            assert content == (source_dir / photo["original_filename"]).read_bytes(), name
        with Image.open(io.BytesIO(content)) as image:
            assert image.format == "JPEG", name
            assert image.size == (photo["width"], photo["height"]), name
            image.verify()
        print(f"Week {photo['week']}: {name} - embedded, intact, self-contained")
    print("PASS: 8 original photos embedded across 7 notebooks; no USB connection is needed to view them.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, help="Also compare against the original photo folder")
    check_photos(parser.parse_args().source_dir)
