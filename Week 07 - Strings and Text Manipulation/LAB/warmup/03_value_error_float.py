# AI-assisted repair of the intentionally broken exercise.
# Run it, read the last line, then fix it.

raw_line = "srv-01,used=unknown,total=100"
hostname_part, rest = raw_line.split(",", 1)

for piece in rest.split(","):
    key, value = piece.split("=")
    try:
        print(key, float(value))
    except ValueError:
        print(f"{key}: not a number ({value})")
