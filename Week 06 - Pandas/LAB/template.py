"""Record Check: IT lane, Typical tier. AI-assisted draft; see AI_ASSISTANCE.md."""

from pathlib import Path
import pandas as pd

# Synthetic practice records, stored beside this script.
df = pd.read_csv(Path(__file__).with_name("servers.csv"))
df["percent"] = (df["used_gb"] / df["total_gb"]) * 100
df["status"] = df["percent"].apply(
    lambda p: "OVER LIMIT" if p >= 100 else "WARNING" if p >= 90 else "OK"
)
print(df)
print("\nRecords needing attention:")
print(df[df["status"] != "OK"])
