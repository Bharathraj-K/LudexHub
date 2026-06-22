from __future__ import annotations

from pathlib import Path

FONTS_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"

COLORS = {
    "bg": "#0B0614",
    "surface": "#110C22",
    "input_bg": "#150F2A",
    "text": "#E0DCF0",
    "text_dim": "#6B5F80",
    "accent": "#7C3AED",
    "accent_light": "#A855F7",
    "accent_dark": "#5B21B6",
    "selection_bg": "#1A1040",
    "border": "#2A1F45",
    "hover": "#1C1335",
    "steam": "#FCEE09",
    "epic": "#00F0FF",
    "gog": "#FF003C",
}

WINDOW_WIDTH = 750
WINDOW_HEIGHT = 500
WINDOW_OPACITY = 0.92
ICON_SIZE = 160

TITLE_BAR_HEIGHT = 60
FOOTER_HEIGHT = 36
ITEM_HEIGHT = 56
ITEM_ICON_SIZE = 42


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
        border-radius: 12px;
    }}

    QWidget#title_bar {{
        background-color: transparent;
        border: none;
    }}

    QPushButton#minimize_btn {{
        background-color: transparent;
        color: {c["text_dim"]};
        border: none;
        font-size: 18px;
        font-weight: bold;
        padding: 4px 8px;
    }}

    QPushButton#minimize_btn:hover {{
        color: {c["accent_light"]};
    }}

    QPushButton#close_btn {{
        background-color: transparent;
        color: {c["text_dim"]};
        border: none;
        font-size: 18px;
        font-weight: bold;
        padding: 4px 8px;
    }}

    QPushButton#close_btn:hover {{
        color: #EF4444;
    }}

    QLineEdit#search_input {{
        background-color: {c["input_bg"]};
        color: {c["accent_light"]};
        border: 1px solid {c["border"]};
        border-radius: 10px;
        padding: 12px 18px;
        font-size: 16px;
        {font}
        selection-background-color: {c["accent"]};
        selection-color: #FFFFFF;
    }}

    QLineEdit#search_input:focus {{
        border: 1px solid {c["accent"]};
    }}

    QLabel#hotkey_hint {{
        background-color: {c["surface"]};
        color: {c["text_dim"]};
        border: 1px solid {c["border"]};
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 11px;
        font-weight: bold;
        font-family: 'Consolas', 'Courier New', monospace;
    }}

    QListWidget#results {{
        background-color: transparent;
        border: none;
        outline: none;
        padding: 2px 0px;
    }}

    QListWidget#results::item {{
        color: {c["text"]};
        padding: 0px 12px;
        border-radius: 8px;
        margin: 2px 4px;
        min-height: {ITEM_HEIGHT}px;
        border-left: 3px solid transparent;
    }}

    QListWidget#results::item:selected {{
        background-color: {c["selection_bg"]};
        color: {c["accent_light"]};
        border-left: 3px solid {c["accent"]};
    }}

    QListWidget#results::item:hover:!selected {{
        background-color: {c["hover"]};
    }}

    QLabel#no_results {{
        color: {c["text_dim"]};
        font-size: 14px;
        padding: 24px;
        {font}
    }}

    QWidget#footer {{
        background-color: transparent;
        border: none;
    }}

    QLabel#footer_text {{
        color: {c["text_dim"]};
        font-size: 12px;
        font-family: 'Consolas', 'Courier New', monospace;
        border: none;
    }}

    QLabel#footer_key {{
        color: {c["text_dim"]};
        font-size: 12px;
        font-family: 'Consolas', 'Courier New', monospace;
        background-color: {c["surface"]};
        border: 1px solid {c["border"]};
        border-radius: 3px;
        padding: 2px 6px;
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
