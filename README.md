# mateo_borina_zadatak1


## Getting Started

Follow these steps to set up and run the application locally.

### Clone the repository

```bash
git clone https://github.com/b0rke-mborina/mateo_borina_zadatak1
cd https://github.com/b0rke-mborina/mateo_borina_zadatak1
```

### Create and activate a virtual environment

```bash
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set PYTHONPATH

```bash
$env:PYTHONPATH="src"
```

### Run the application

Start the development server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

Visit http://127.0.0.1:8000 in your browser.

### Run Tests

Run all tests using pytest:

```bash
pytest
```

## Notes

Commands are written for PowerShell on Windows.
On Linux/macOS, use the appropriate activation command:

```bash
source .venv/bin/activate
export PYTHONPATH=src
```
