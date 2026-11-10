"""Record Check: IT lane, Typical tier. AI-assisted draft; see AI_ASSISTANCE.md."""

# INPUT: input() returns text; convert the quantities to numbers.
hostname = input("Hostname: ")
used_gb = float(input("GB used: "))
total_gb = float(input("GB total: "))

# PROCESS: Week 1 deliberately leaves division by zero as an error to inspect.
free_gb = total_gb - used_gb
percent_used = (used_gb / total_gb) * 100

# OUTPUT: every numeric field has the same width and two decimal places.
print()
print("=" * 34)
print(f"  RECORD CHECK  -  {hostname}")
print("=" * 34)
print(f"  Used        : {used_gb:>10.2f}")
print(f"  Total       : {total_gb:>10.2f}")
print(f"  Free        : {free_gb:>10.2f}")
print(f"  Percent     : {percent_used:>10.2f} %")
print("=" * 34)
