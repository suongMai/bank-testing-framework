# bank-testing-framework

XYZ Bank automation using Python, Playwright, and the Page Object Model (POM).

## Setup

```bash
pip install -r requirements.txt
# Required: download Playwright browsers (otherwise tests fail with "Executable doesn't exist")
python -m playwright install chromium   # default for this project
# Optional: python -m playwright install firefox
# Optional: python -m playwright install msedge
```

## Robot Framework

Run tests via Robot Framework (shared POM and browser factory):

```bash
# From project root. Set PYTHONPATH so libs can be imported.

# Windows CMD:
set PYTHONPATH=%CD%
python run_robot.py

# Or:  python -m run_robot
# Or call robot directly:  robot --outputdir report robot/bank_suite.robot
```

Output (report.html, log.html, output.xml) is written to **report/**.

## Config

Edit **config.py** at project root (no CLI params):

| Variable   | Default  | Description |
|-----------|----------|-------------|
| `HEADLESS` | `True`  | `True` = headless (no window). `False` = headed (browser visible). |
| `BROWSER`  | `chromium` | `chromium`, `firefox`, `msedge`, `chrome`, `edge`. |
| `BASE_URL` | (demo URL) | XYZ Bank app URL. |
| `CUSTOMER_NAME` | Hermoine Granger | Default customer name. |
