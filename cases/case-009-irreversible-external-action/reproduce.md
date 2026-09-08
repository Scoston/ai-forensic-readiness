# Reproduction

From a clean checkout, install validation dependencies once:

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/build_cases.py --check
python scripts/run_case.py --case 9 --output dist/case-009-comparison.json
python scripts/validate.py
python -m unittest discover -s tests -v
```

`run_case.py` executes both conditions and writes their complete results to the
chosen local output. `build_cases.py --check` regenerates committed simulation
artifacts in a temporary directory and compares exact bytes, without modifying
evidence. `--write` is for deliberately rebuilding synthetic reference fixtures;
never use it to reseal collected production evidence.

No network access is needed after dependency installation. All timestamps and
identities are synthetic. Repetition is deterministic and is not an independent
experiment or external reproduction.
