from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from core.settings import load_settings, save_settings
from core.startup import is_startup_enabled, set_startup  # STARTUP FEATURE
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

POSITION_OPTIONS = [
    "Top Left",
    "Top Center",
    "Top Right",
    "Center",
    "Bottom Left",
    "Bottom Center",
    "Bottom Right",
]

POSITION_KEYS = {
    "Top Left": "top-left",
    "Top Center": "top-center",
    "Top Right": "top-right",
    "Center": "center",
    "Bottom Left": "bottom-left",
    "Bottom Center": "bottom-center",
    "Bottom Right": "bottom-right",
}


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SETTINGS")
        self.setFixedSize(420, 660)
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)
        self._settings = load_settings()
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(16, 16, 16, 16)

        hotkey_group = QGroupBox("HOTKEY")
        hk_layout = QHBoxLayout(hotkey_group)
        self._hotkey_input = QLineEdit(self._settings.get("hotkey", "alt+space"))
        hk_layout.addWidget(self._hotkey_input)
        layout.addWidget(hotkey_group)

        font_group = QGroupBox("FONT")
        font_layout = QHBoxLayout(font_group)
        self._font_combo = QComboBox()
        for f in FONT_OPTIONS:
            self._font_combo.addItem(f)
        current_font = self._settings.get("font_family", "Orbitron")
        idx = self._font_combo.findText(current_font)
        if idx >= 0:
            self._font_combo.setCurrentIndex(idx)
        font_layout.addWidget(self._font_combo)
        layout.addWidget(font_group)

        pos_group = QGroupBox("WINDOW POSITION")
        pos_layout = QHBoxLayout(pos_group)
        self._pos_combo = QComboBox()
        for p in POSITION_OPTIONS:
            self._pos_combo.addItem(p)
        current_pos = self._settings.get("position", "center")
        display = next((k for k, v in POSITION_KEYS.items() if v == current_pos), "Center")
        idx = self._pos_combo.findText(display)
        if idx >= 0:
            self._pos_combo.setCurrentIndex(idx)
        pos_layout.addWidget(self._pos_combo)
        layout.addWidget(pos_group)

        size_group = QGroupBox("WINDOW SIZE")
        size_layout = QHBoxLayout(size_group)
        size_layout.addWidget(QLabel("W:"))
        self._width_input = QLineEdit(str(self._settings.get("window_width", 540)))
        self._width_input.setFixedWidth(60)
        size_layout.addWidget(self._width_input)
        size_layout.addWidget(QLabel("H:"))
        self._height_input = QLineEdit(str(self._settings.get("window_height", 300)))
        self._height_input.setFixedWidth(60)
        size_layout.addWidget(self._height_input)
        size_layout.addStretch()
        layout.addWidget(size_group)

        opacity_group = QGroupBox("OPACITY")
        opacity_layout = QHBoxLayout(opacity_group)
        self._opacity_input = QLineEdit(str(self._settings.get("window_opacity", 0.92)))
        self._opacity_input.setFixedWidth(60)
        opacity_layout.addWidget(self._opacity_input)
        opacity_layout.addWidget(QLabel("(0.0 - 1.0)"))
        opacity_layout.addStretch()
        layout.addWidget(opacity_group)

        paths_group = QGroupBox("LAUNCHER PATHS (leave empty for auto-detect)")
        paths_layout = QVBoxLayout(paths_group)

        for label, key in [("Steam", "steam_path"), ("Epic", "epic_path"), ("GOG", "gog_path")]:
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{label}:"))
            line = QLineEdit(self._settings.get(key, ""))
            line.setPlaceholderText("Auto-detect")
            row.addWidget(line)
            browse = QPushButton("...")
            browse.setFixedWidth(36)
            browse.clicked.connect(lambda checked, ln=line: self._browse_folder(ln))
            row.addWidget(browse)
            paths_layout.addLayout(row)
            setattr(self, f"_{key}_input", line)

        layout.addWidget(paths_group)

        # STARTUP FEATURE: checkbox to enable/disable Windows startup
        startup_group = QGroupBox("STARTUP")
        startup_layout = QHBoxLayout(startup_group)
        self._startup_checkbox = QCheckBox("Start with Windows")
        self._startup_checkbox.setChecked(is_startup_enabled())
        startup_layout.addWidget(self._startup_checkbox)
        startup_layout.addStretch()
        layout.addWidget(startup_group)

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

    def _browse_folder(self, line_edit: QLineEdit) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            line_edit.setText(folder)

    def _save(self) -> None:
        self._settings["hotkey"] = self._hotkey_input.text().strip() or "alt+space"
        self._settings["font_family"] = self._font_combo.currentText()
        self._settings["position"] = POSITION_KEYS.get(self._pos_combo.currentText(), "center")
        try:
            self._settings["window_width"] = int(self._width_input.text().strip())
        except ValueError:
            pass
        try:
            self._settings["window_height"] = int(self._height_input.text().strip())
        except ValueError:
            pass
        try:
            self._settings["window_opacity"] = float(self._opacity_input.text().strip())
        except ValueError:
            pass
        self._settings["steam_path"] = self._steam_path_input.text().strip()
        self._settings["epic_path"] = self._epic_path_input.text().strip()
        self._settings["gog_path"] = self._gog_path_input.text().strip()
        self._settings["start_with_windows"] = self._startup_checkbox.isChecked()
        set_startup(self._startup_checkbox.isChecked())  # STARTUP FEATURE
        save_settings(self._settings)
        self.accept()

    def get_settings(self) -> dict:
        return self._settings
