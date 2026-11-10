# CST1510 review report - 10 November 2026

Weeks 1-7 have been prepared sequentially as **AI-assisted Typical-tier lab
drafts**, using the IT lane. They are for review, not a claim of independent
student work. The scope is the lab notebooks, warm-ups and mini-projects;
workshop walkthroughs, teaching examples, demonstrations, Excellent challenges
and optional extra projects remain as supplied.

## Changes

| Week | Regular drills completed | Typical mini-project |
|---|---|---|
| 1 | D1-D6 | Input, casting, calculated free space and percentage, aligned report |
| 2 | D1-D16 | Three-tier status, including exact 90% and 100% boundaries |
| 3 | D1-D15 | `status_of` and pure `check` functions, returning results |
| 4 | D1-D16 | `load_records`, list of dicts, separate checking and reporting |
| 5 | D1-D11 | Independent `Record` objects with a `status` method |
| 6 | D1-D14 | CSV loading, vectorized percentage, lambda classification and boolean filtering |
| 7 | D1-D15 | Clean and parse messy text, convert numbers and classify records |

All 93 regular drills were filled and executed. All 21 warm-up files were
repaired. Each lab notebook selects `Python 3.12 (CST1510 .venv)` and contains a
visible AI-assistance notice. Actual automated outputs and test-fixture metadata
are saved; a source hash detects outputs that have become stale after edits.

New synthetic input files are `Week 04 .../LAB/servers.txt` (five records) and
`Week 06 .../LAB/servers.csv` (six records). Week 7 contains six deliberately
messy synthetic records in its script. The supplied sample files were preserved.
Week 4's `notes.txt` is the output of the file-writing code drill, not handwritten
course notes. Week 6's `records_report.csv` and `status_counts.png` were generated
by the actual notebook run. The chart was visually inspected.

The Python environment was repaired by using the installed **Python 3.12.10**
directly to create `.venv`; the terminal previously resolved `python` to the
Microsoft Store alias and the launcher did not detect the installation. The
Microsoft Jupyter extension and its supporting extensions were installed in
VS Code. The named `cst1510-py312` kernel was registered both within `.venv` and
in Jupyter's user directory. VS Code workspace settings select the environment
and use each notebook's folder for relative files. This follows the
[official IPython kernel installation guidance](https://ipython.readthedocs.io/en/stable/install/kernel_install.html).

The supplied eight dependencies plus `nbclient` are installed. Exact versions
are recorded in `requirements-lock.txt`; `requirements-review.txt` identifies
the extra execution tool. `tools/check_kernel.py`, `tools/execute_labs.py` and
`tools/audit_coursework.py` provide repeatable verification. `.gitignore` keeps
the environment, execution scratch files, pytest cache and editor crash log out
of Git. Instructor material remains excluded under the original ignore rules.

## Verification

- Two fresh Jupyter kernels executed assertions and imported every required
  package using `.venv/Scripts/python.exe`, Python 3.12.10.
- The supplied `Week 00 .../verify_setup.py` passed every check.
- `pip check` found no broken dependencies.
- All seven lab notebooks executed in ascending order in fresh real kernels.
  Inputs were explicitly labelled automated fixtures. Execution used temporary
  lab copies so file-writing drills did not overwrite existing working files.
- **84 pytest checks passed.** Coverage includes all 21 repaired warm-ups,
  numeric report output, decimal input, zero-total behaviour, status boundaries,
  file loading from another working directory, missing files, independent
  objects, pandas filtering, generated CSV/PNG files, messy and invalid text,
  all 93 regular drill cells, saved-output source hashes and Python compilation.
- All notebook instruction and Journal/photo cells were compared with the
  preserved starting commit. Their text and attachments match, apart from the
  explicitly added first-cell disclosure.
- Static inspection read 163 instruction, source, notebook and data files,
  including 35 notebooks, and checked notebook schemas and Python syntax. This
  does not claim that intentionally broken teaching examples all run successfully.

Week 3 D9 intentionally produces `NameError` to demonstrate local scope; it is
tagged as an expected exception so the remaining notebook can execute. Earlier
drills use another variable name so they cannot accidentally mask that error.
Weeks 1-3 still raise `ZeroDivisionError` for a zero total, as their instructions
require. Week 4's Typical loader still raises `FileNotFoundError` for a missing
file. Invalid numeric text in the Week 7 mini-project remains a visible
`ValueError`; its warm-up separately demonstrates catching that error. These
are deliberate teaching behaviours, not hidden test failures.

## Preservation and Git

`main` remains at `7a016b714e99c84bcfb29555d2711920ab2f7a99`. Work is on
`review/cst1510-typical`. Commit `d0ccc19` preserves the original lab files before
the AI-assisted changes. Later commits group the tested environment, Weeks 1-7
in order, and this report. Only that review branch is intended for the push;
there is no merge or coursework submission.

A separate pre-edit backup of all 197 existing files is at
`C:\Users\lildr\AppData\Local\Temp\CST1510-before-review-20261110-000547`.
The preservation check found zero missing originals; changes to originals are
limited to `.gitignore` and the seven lab notebooks, seven templates and 21
warm-up scripts. Teaching resources, the nested `CST1510/` clone and `exc2.py`
were preserved. The nested clone and `exc2.py` remain untracked, as found.
`exc2.py` still references an undefined `Server`; it was not silently replaced
with a different exercise. Local execution artifacts and the detailed audit are
in the ignored `.review/` folder. Temporary backups should not be relied on as
long-term storage; the preserved Git commit provides the lab baseline.

## Remaining student tasks

1. Review and understand each AI-assisted draft, and run it yourself with your
   own inputs. Add your own name where prompted. Make your own predictions
   before running exercises that request them. Observe and record the specified
   errors yourself; automated checks do not replace those learning activities.
2. Complete all handwritten notes, reflections and Cheat Sheet boxes yourself.
   Take your own photographs and insert them into the existing Journal/photo
   cells. Complete any requested peer demonstration yourself.
3. Read the actual CW1 brief and university/module AI-use rules, and make the
   required AI declaration before using any draft for assessment. The user
   stated that AI assistance was unrestricted, but the policy and brief were
   not supplied or independently verified. See `AI_ASSISTANCE.md` for the scope
   and provenance record.
4. In VS Code, select **Python 3.12 (CST1510 .venv)** in a notebook's kernel menu.
   If the new extension has not appeared yet, reload the VS Code window. The
   kernel was tested programmatically; the visible editor interaction was not
   exercised. The system-wide Python PATH/launcher aliases were not changed.

No handwritten evidence, photographs, personal reflections, peer activity or
learning dates were fabricated. Nothing was submitted.

## Repeat the checks from the project root

```powershell
.venv/Scripts/python.exe tools/check_kernel.py
.venv/Scripts/python.exe tools/execute_labs.py
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe tools/audit_coursework.py
```

The notebook runner saves executed copies under `.review/` by default. Add
`--write` only when you want to refresh the actual lab notebook outputs. To
execute only Week 1, use `--week 1`.

To recreate this tested environment on Windows with Python 3.12 installed:

```powershell
py -3.12 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-lock.txt
.venv/Scripts/python.exe -m ipykernel install --user --name cst1510-py312 --display-name "Python 3.12 (CST1510 .venv)"
```

On this machine the launcher was not detecting Python; if that persists, use
the installed executable at
`C:\Users\lildr\AppData\Local\Programs\Python\Python312\python.exe` in place
of `py -3.12` when creating the environment.
