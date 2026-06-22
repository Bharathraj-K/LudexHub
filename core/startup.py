"""STARTUP FEATURE — Manages Windows startup shortcut.

Creates/deletes a .lnk shortcut in the Windows Startup folder so LudexHub
launches automatically when the user logs in.

To remove this feature entirely:
  1. Delete this file (core/startup.py)
  2. Remove the startup checkbox from ui/settings_dialog.py (search for STARTUP)
  3. Remove "start_with_windows" from core/settings.py DEFAULTS
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from core.paths import get_app_root

APP_ROOT = get_app_root()
SHORTCUT_NAME = "LudexHub.lnk"
STARTUP_FOLDER = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
SHORTCUT_PATH = STARTUP_FOLDER / SHORTCUT_NAME


def is_startup_enabled() -> bool:
    return SHORTCUT_PATH.exists()


def set_startup(enabled: bool) -> None:
    if enabled:
        _create_shortcut()
    else:
        _remove_shortcut()


def _create_shortcut() -> None:
    is_frozen = getattr(sys, 'frozen', False)

    if is_frozen:
        target = sys.executable
        args = ""
    else:
        target = sys.executable
        args = f'"{APP_ROOT / "main.py"}"'

    ps_script = (
        f'$ws = New-Object -ComObject WScript.Shell; '
        f'$sc = $ws.CreateShortcut("{SHORTCUT_PATH}"); '
        f'$sc.TargetPath = "{target}"; '
        f'$sc.Arguments = "{args}"; '
        f'$sc.WorkingDirectory = "{APP_ROOT}"; '
        f'$sc.Save()'
    )

    try:
        subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass


def _remove_shortcut() -> None:
    try:
        SHORTCUT_PATH.unlink(missing_ok=True)
    except OSError:
        pass
