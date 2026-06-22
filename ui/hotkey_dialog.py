from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from ui.styles import COLORS


class HotkeyDialog(QDialog):
    def __init__(self, current_hotkey: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("CHANGE HOTKEY")
        self.setFixedSize(340, 180)
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        self._status_label = QLabel(f"CURRENT: {current_hotkey.upper()}")
        layout.addWidget(self._status_label)

        self._capture_label = QLabel("PRESS NEW KEY COMBINATION...")
        self._capture_label.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 11px;")
        layout.addWidget(self._capture_label)

        btn_layout = QVBoxLayout()

        self._ok_btn = QPushButton("APPLY")
        self._ok_btn.setEnabled(False)
        self._ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self._ok_btn)

        cancel_btn = QPushButton("CANCEL")
        cancel_btn.setObjectName("cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

        self._new_hotkey: str | None = None
        self._listening = False
        self._keys_pressed: set[str] = set()

    def start_listening(self) -> None:
        try:
            import keyboard

            self._listening = True
            keyboard.on_press(self._on_key_press)
            keyboard.on_release(self._on_key_release)
        except ImportError:
            self._capture_label.setText("keyboard module not available")

    def stop_listening(self) -> None:
        self._listening = False
        try:
            import keyboard

            keyboard.unhook_all()
        except ImportError:
            pass

    def _on_key_press(self, event) -> None:
        if not self._listening:
            return
        name = event.name.lower()
        if name in ("alt", "ctrl", "shift", "win"):
            self._keys_pressed.add(name)
        else:
            combo_parts = sorted(self._keys_pressed)
            combo_parts.append(name)
            combo = "+".join(combo_parts)
            self._new_hotkey = combo
            self._status_label.setText(f"NEW: {combo.upper()}")
            self._capture_label.setText("CLICK APPLY TO CONFIRM")
            self._ok_btn.setEnabled(True)

    def _on_key_release(self, event) -> None:
        if not self._listening:
            return
        name = event.name.lower()
        self._keys_pressed.discard(name)

    def get_new_hotkey(self) -> str | None:
        return self._new_hotkey

    def closeEvent(self, event) -> None:
        self.stop_listening()
        super().closeEvent(event)
