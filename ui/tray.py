from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenu, QSystemTrayIcon


class TrayIcon(QObject):
    open_requested = Signal()
    refresh_requested = Signal()
    change_hotkey_requested = Signal()
    exit_requested = Signal()

    def __init__(self, icon_path: str, parent: QObject | None = None):
        super().__init__(parent)

        resolved = Path(icon_path)
        if resolved.exists():
            icon = QIcon(str(resolved))
        else:
            icon = QIcon.fromTheme("application-exit")

        self._tray = QSystemTrayIcon(icon)
        self._tray.setToolTip("LudexHub")

        menu = QMenu()

        action_open = QAction("Open Launcher", menu)
        action_open.triggered.connect(self.open_requested.emit)
        menu.addAction(action_open)

        action_refresh = QAction("Refresh Library", menu)
        action_refresh.triggered.connect(self.refresh_requested.emit)
        menu.addAction(action_refresh)

        action_hotkey = QAction("Change Hotkey...", menu)
        action_hotkey.triggered.connect(self.change_hotkey_requested.emit)
        menu.addAction(action_hotkey)

        menu.addSeparator()

        action_exit = QAction("Exit", menu)
        action_exit.triggered.connect(self.exit_requested.emit)
        menu.addAction(action_exit)

        self._tray.setContextMenu(menu)
        self._tray.activated.connect(self._on_activated)

    def show(self) -> None:
        self._tray.show()

    def hide(self) -> None:
        self._tray.hide()

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.DoubleClick:
            self.open_requested.emit()
