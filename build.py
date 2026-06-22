"""Build script for LudexHub.

Run: python build.py
Output: dist/LudexHub.exe
"""

import subprocess
import sys


def main() -> None:
    print("Building LudexHub...")
    subprocess.run(
        [sys.executable, "-m", "PyInstaller", "LudexHub.spec", "--noconfirm"],
        check=True,
    )
    print("Build complete: dist/LudexHub.exe")


if __name__ == "__main__":
    main()
