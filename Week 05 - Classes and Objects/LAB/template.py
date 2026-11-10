"""Record Check: IT lane, Typical tier. AI-assisted draft; see AI_ASSISTANCE.md."""

class Record:
    def __init__(self, label, value, limit):
        """Store the three fields on this particular record."""
        self.label = label
        self.value = value
        self.limit = limit

    def status(self):
        """Return the three-tier status for this record."""
        percent = (self.value / self.limit) * 100
        if percent >= 100:
            return "OVER LIMIT"
        elif percent >= 90:
            return "WARNING"
        else:
            return "OK"


if __name__ == "__main__":
    # Synthetic IT practice records, including each status category.
    records = [Record("test-srv-01", 87.0, 120.0),
               Record("test-srv-02", 95.0, 100.0),
               Record("test-srv-03", 120.0, 100.0)]
    for record in records:
        status = record.status()
        print()
        print("=" * 34)
        print(f"  RECORD CHECK  -  {record.label}")
        print("=" * 34)
        print(f"  Used        : {record.value:>10.2f}")
        print(f"  Total       : {record.limit:>10.2f}")
        print(f"  Status      : {status:>10}")
        print("=" * 34)
