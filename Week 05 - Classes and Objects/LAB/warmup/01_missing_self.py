# AI-assisted repair of the intentionally broken exercise.
# Run it, read the last line, then fix it.

class Record:
    def status(self, percent):
        return percent

r = Record()
print(r.status(95))
