"""Record Check: IT lane, Typical tier. AI-assisted draft; see AI_ASSISTANCE.md."""

from pathlib import Path


def check_record(value, limit):
    """Return free capacity, percent used and the three-tier status."""
    difference = limit - value
    percent = (value / limit) * 100
    if percent >= 100:
        status = "OVER LIMIT"
    elif percent >= 90:
        status = "WARNING"
    else:
        status = "OK"
    return difference, percent, status


def print_report(label, value, limit, difference, percent, status):
    """Print one aligned IT capacity report."""
    print()
    print("=" * 34)
    print(f"  RECORD CHECK  -  {label}")
    print("=" * 34)
    print(f"  Used        : {value:>10.2f}")
    print(f"  Total       : {limit:>10.2f}")
    print(f"  Free        : {difference:>10.2f}")
    print(f"  Percent     : {percent:>10.2f} %")
    print(f"  Status      : {status:>10}")
    print("=" * 34)


def load_records(path):
    """Load label,value,limit lines into a list of dictionaries."""
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            label, value, limit = line.strip().split(",")
            records.append({"label": label, "value": float(value), "limit": float(limit)})
    return records


if __name__ == "__main__":
    # Synthetic practice data; resolve beside this script even when run from the repo root.
    records = load_records(Path(__file__).with_name("servers.txt"))
    for record in records:
        difference, percent, status = check_record(record["value"], record["limit"])
        print_report(record["label"], record["value"], record["limit"],
                     difference, percent, status)
