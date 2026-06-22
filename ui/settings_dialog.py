from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from core.settings import load_settings, save_settings
from ui.styles import COLORS

FONT_OPTIONS = [
    "Orbitron",
    "Rajdhani",
    "Share Tech Mono",
    "Consolas",
    "Segoe UI",
    "Arial",
    "Helvetica",
]


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SETTINGS")
        self.setFixedSize(420, 240)
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)
        self._settings = load_settings()
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(16, 16, 16, 16)

        hotkey_group = QGroupBox("HOTKEY")
        hk_layout = QHBoxLayout(hotkey_group)
        self._hotkey_input = QLineEdit(self._settings.get("hotkey", "alt+space"))
        hk_layout.addWidget(self._hotkey_input)
        layout.addWidget(hotkey_group)

        font_group = QGroupBox("FONT")
        font_layout = QHBoxLayout(font_group)
        self._font_combo = QComboBox()
        available = QFontDatabase.families()
        for f in FONT_OPTIONS:
            self._font_combo.addItem(f)
        current_font = self._settings.get("font_family", "Orbitron")
        idx = self._font_combo.findText(current_font)
        if idx >= 0:
            self._font_combo.setCurrentIndex(idx)
        font_layout.addWidget(self._font_combo)
        layout.addWidget(font_group)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("CANCEL")
        cancel_btn.setObjectName("cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("SAVE")
        save_btn.clicked.connect(self._save)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

    def _save(self) -> None:
        self._settings["hotkey"] = self._hotkey_input.text().strip() or "alt+space"
        self._settings["font_family"] = self._font_combo.currentText()
        save_settings(self._settings)
        self.accept()

    def get_settings(self) -> dict:
        return self._settings
