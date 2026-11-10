"""Record Check: IT lane, Typical tier. AI-assisted draft; see AI_ASSISTANCE.md."""

def status_of(percent):
    """Return OVER LIMIT, WARNING or OK for a percentage."""
    if percent >= 100:
        return "OVER LIMIT"
    elif percent >= 90:
        return "WARNING"
    else:
        return "OK"


def check(value, limit):
    """Return free capacity (limit minus value) and percentage used."""
    return limit - value, (value / limit) * 100


if __name__ == "__main__":
    hostname = input("Hostname: ")
    used_gb = float(input("GB used: "))
    total_gb = float(input("GB total: "))
    free_gb, percent_used = check(used_gb, total_gb)
    status = status_of(percent_used)

    print()
    print("=" * 34)
    print(f"  RECORD CHECK  -  {hostname}")
    print("=" * 34)
    print(f"  Used        : {used_gb:>10.2f}")
    print(f"  Total       : {total_gb:>10.2f}")
    print(f"  Free        : {free_gb:>10.2f}")
    print(f"  Percent     : {percent_used:>10.2f} %")
    print(f"  Status      : {status:>10}")
    print("=" * 34)
