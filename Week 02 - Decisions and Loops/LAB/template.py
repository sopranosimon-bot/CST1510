"""Record Check: IT lane, Typical tier. AI-assisted draft; see AI_ASSISTANCE.md."""

# INPUT
hostname = input("Hostname: ")
used_gb = float(input("GB used: "))
total_gb = float(input("GB total: "))

# PROCESS: the lab requires leaving zero-total division unfixed at this stage.
free_gb = total_gb - used_gb
percent_used = (used_gb / total_gb) * 100
if percent_used >= 100:
    status = "OVER LIMIT"
elif percent_used >= 90:
    status = "WARNING"
else:
    status = "OK"

# OUTPUT
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
