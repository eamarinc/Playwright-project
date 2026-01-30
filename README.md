Setup and run tests

1. Create and activate a virtual environment (macOS/Linux):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
python -m playwright install
```

3. Run the specific test:

```bash
python -m pytest tests/test_add_to_cart.py -q
```

Notes:
- If you get errors about browsers, run `python -m playwright install`.
- If using Chrome channel in `conftest.py`, ensure you have Chrome installed or remove the `channel` argument.
