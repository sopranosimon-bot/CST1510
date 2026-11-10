"""Record Check: IT lane, Typical tier. AI-assisted draft; see AI_ASSISTANCE.md."""

def parse_line(raw_line):
    """Return an IT record with a clean hostname, keys and numeric values."""
    cleaned_line = raw_line.strip().lower()
    hostname_part, rest = cleaned_line.split(",", 1)
    record = {"hostname": hostname_part.strip()}
    for piece in rest.split(","):
        key, value = piece.split("=", 1)
        record[key.strip()] = float(value.strip())
    return record


def status_of(used, total):
    """Return the three-tier capacity status for used and total GB."""
    percent = (used / total) * 100
    if percent >= 100:
        return "OVER LIMIT"
    elif percent >= 90:
        return "WARNING"
    else:
        return "OK"


if __name__ == "__main__":
    # Deliberately messy synthetic examples, not observations of real servers.
    raw_records = [
        "  Test-Srv-01 , USED=87 , total=120  ",
        "TEST-SRV-02,used = 95,TOTAL =100",
        " test-srv-03 , Used=120 , Total=100 ",
        "Test-Srv-04, USED = 0, TOTAL=80   ",
        "  TEST-SRV-05 ,used=100, total =100",
        "test-SRV-06, total=200 , used = 180  ",
    ]
    for raw_record in raw_records:
        record = parse_line(raw_record)
        status = status_of(record["used"], record["total"])
        print(record, status)
