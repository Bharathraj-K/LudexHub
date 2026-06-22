from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from core.settings import load_settings, save_settings


class HotkeyManager(QObject):
    hotkey_triggered = Signal()

    def __init__(self, hotkey_str: str, parent: QObject | None = None):
        super().__init__(parent)
        self._hotkey_str = hotkey_str
        self._registered = False

    @property
    def hotkey(self) -> str:
        return self._hotkey_str

    def start(self) -> None:
        if self._registered:
            return
        try:
            import keyboard

            keyboard.add_hotkey(self._hotkey_str, self._on_hotkey, suppress=True)
            self._registered = True
        except Exception as e:
            print(f"[LudexHub] Failed to register hotkey '{self._hotkey_str}': {e}")

    def stop(self) -> None:
        if not self._registered:
            return
        try:
            import keyboard

            keyboard.remove_hotkey(self._hotkey_str)
            self._registered = False
        except Exception:
            pass

    def update(self, new_hotkey: str) -> None:
        self.stop()
        self._hotkey_str = new_hotkey
        self.start()
        settings = load_settings()
        settings["hotkey"] = new_hotkey
        save_settings(settings)

    def _on_hotkey(self) -> None:
        self.hotkey_triggered.emit()
