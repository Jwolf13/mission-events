from pathlib import Path
import sys
import uvicorn

# Ensure ./src is on sys.path
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

if __name__ == "__main__":
    uvicorn.run("lab02.main:app", reload=True)
