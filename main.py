from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication, QDialog

from core.hotkey import HotkeyManager
from core.scanner import get_games
from core.settings import load_settings
from ui.hotkey_dialog import HotkeyDialog
from ui.tray import TrayIcon
from ui.window import LauncherWindow


def _show_hotkey_dialog(tray: TrayIcon, hotkey_manager: HotkeyManager) -> None:
    dialog = HotkeyDialog(hotkey_manager.hotkey)
    dialog.start_listening()
    result = dialog.exec()
    dialog.stop_listening()

    if result == QDialog.Accepted:
        new_hotkey = dialog.get_new_hotkey()
        if new_hotkey:
            hotkey_manager.update(new_hotkey)


def main() -> None:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("LudexHub")

    settings = load_settings()
    games = get_games()

    window = LauncherWindow(games)

    # System tray
    tray = TrayIcon(settings["tray_icon"])
    tray.open_requested.connect(window.toggle)
    tray.refresh_requested.connect(window.refresh_games)
    tray.change_hotkey_requested.connect(
        lambda: _show_hotkey_dialog(tray, hotkey_manager)
    )

    # Hotkey
    hotkey_manager = HotkeyManager(settings["hotkey"])
    hotkey_manager.hotkey_triggered.connect(window.toggle)

    def _quit() -> None:
        hotkey_manager.stop()
        tray.hide()
        app.quit()

    tray.exit_requested.connect(_quit)

    hotkey_manager.start()
    tray.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
