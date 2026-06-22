from __future__ import annotations

from pathlib import Path

FONTS_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"

COLORS = {
    "bg": "#0F0A1A",
    "surface": "#16102A",
    "input_bg": "#1A1230",
    "text": "#E8E4F0",
    "text_dim": "#7A6F8A",
    "accent": "#7C3AED",
    "accent_light": "#A855F7",
    "accent_dark": "#5B21B6",
    "selection_bg": "#1E1540",
    "border": "#2A2040",
    "hover": "#1E1535",
    "steam": "#FCEE09",
    "epic": "#00F0FF",
    "gog": "#FF003C",
}

WINDOW_WIDTH = 540
WINDOW_HEIGHT = 440
ICON_SIZE = 120


def get_font_path() -> str:
    orbitron = FONTS_DIR / "Orbitron.ttf"
    if orbitron.exists():
        return str(orbitron)
    return ""


def get_stylesheet(font_family: str = "Orbitron") -> str:
    c = COLORS
    font = f"font-family: '{font_family}';" if font_family else ""

    return f"""
    QWidget#launcher {{
        background-color: transparent;
        border: 1px solid {c["accent"]};
        border-radius: 10px;
    }}

    QLineEdit#search_input {{
        background-color: {c["input_bg"]};
        color: {c["accent_light"]};
        border: 1px solid {c["border"]};
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 15px;
        {font}
        selection-background-color: {c["accent"]};
        selection-color: #FFFFFF;
    }}

    QLineEdit#search_input:focus {{
        border: 1px solid {c["accent"]};
    }}

    QListWidget#results {{
        background-color: transparent;
        border: none;
        outline: none;
        padding: 4px 0px;
    }}

    QListWidget#results::item {{
        color: {c["text"]};
        padding: 6px 12px;
        border-radius: 6px;
        margin: 2px 6px;
        min-height: 50px;
    }}

    QListWidget#results::item:selected {{
        background-color: {c["selection_bg"]};
        color: {c["accent_light"]};
        border: 1px solid {c["accent"]};
    }}

    QListWidget#results::item:hover:!selected {{
        background-color: {c["hover"]};
    }}

    QLabel#no_results {{
        color: {c["text_dim"]};
        font-size: 13px;
        padding: 24px;
        {font}
    }}

    QMenu {{
        background-color: {c["surface"]};
        color: {c["text"]};
        border: 1px solid {c["accent"]};
        border-radius: 6px;
        padding: 4px;
    }}

    QMenu::item {{
        padding: 8px 24px;
        border-radius: 4px;
        {font}
    }}

    QMenu::item:selected {{
        background-color: {c["selection_bg"]};
        color: {c["accent_light"]};
    }}

    QDialog {{
        background-color: {c["bg"]};
        color: {c["text"]};
        border: 1px solid {c["accent"]};
        border-radius: 8px;
    }}

    QGroupBox {{
        color: {c["accent_light"]};
        border: 1px solid {c["border"]};
        border-radius: 6px;
        margin-top: 10px;
        padding-top: 14px;
        font-size: 12px;
        {font}
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 4px;
    }}

    QLabel {{
        color: {c["text"]};
        font-size: 13px;
        {font}
    }}

    QLineEdit {{
        background-color: {c["input_bg"]};
        color: {c["accent_light"]};
        border: 1px solid {c["border"]};
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 13px;
        {font}
    }}

    QLineEdit:focus {{
        border: 1px solid {c["accent"]};
    }}

    QComboBox {{
        background-color: {c["input_bg"]};
        color: {c["accent_light"]};
        border: 1px solid {c["border"]};
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 13px;
        {font}
    }}

    QComboBox:focus {{
        border: 1px solid {c["accent"]};
    }}

    QComboBox::drop-down {{
        border: none;
        padding-right: 8px;
    }}

    QComboBox::down-arrow {{
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 6px solid {c["accent_light"]};
    }}

    QComboBox QAbstractItemView {{
        background-color: {c["surface"]};
        color: {c["text"]};
        border: 1px solid {c["accent"]};
        selection-background-color: {c["selection_bg"]};
        selection-color: {c["accent_light"]};
    }}

    QPushButton {{
        background-color: {c["accent"]};
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        padding: 8px 20px;
        font-size: 13px;
        font-weight: bold;
        {font}
    }}

    QPushButton:hover {{
        background-color: {c["accent_light"]};
    }}

    QPushButton#cancel {{
        background-color: {c["border"]};
        color: {c["text"]};
    }}

    QPushButton#cancel:hover {{
        background-color: #352A50;
    }}
    """
