from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from core.settings import load_settings, save_settings
from ui.styles import COLORS


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(420, 200)
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)
        self._settings = load_settings()
        self._build_ui()

    def _build_ui(self) -> None:
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS["bg"]};
                color: {COLORS["text"]};
            }}
            QGroupBox {{
                color: {COLORS["text"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 14px;
                font-size: 13px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px;
            }}
            QLineEdit {{
                background-color: {COLORS["input_bg"]};
                color: {COLORS["text"]};
                border: 1px solid {COLORS["border"]};
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border: 1px solid {COLORS["selection"]};
            }}
            QPushButton {{
                background-color: {COLORS["selection"]};
                color: {COLORS["text"]};
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: #4A8AFF;
            }}
            QPushButton#cancel {{
                background-color: {COLORS["border"]};
            }}
            QPushButton#cancel:hover {{
                background-color: #555555;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        hotkey_group = QGroupBox("Hotkey")
        hk_layout = QHBoxLayout(hotkey_group)
        self._hotkey_input = QLineEdit(self._settings.get("hotkey", "alt+space"))
        hk_layout.addWidget(self._hotkey_input)
        layout.addWidget(hotkey_group)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self._save)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

    def _save(self) -> None:
        self._settings["hotkey"] = self._hotkey_input.text().strip() or "alt+space"
        save_settings(self._settings)
        self.accept()

    def get_settings(self) -> dict:
        return self._settings
