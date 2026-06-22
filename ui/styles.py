from __future__ import annotations

COLORS = {
    "bg": "#222222",
    "input_bg": "#2D2D2D",
    "text": "#FFFFFF",
    "text_dim": "#888888",
    "selection": "#3A7AFE",
    "border": "#444444",
    "hover": "#2A2A2A",
}

WINDOW_WIDTH = 520
WINDOW_HEIGHT = 400


def get_stylesheet() -> str:
    c = COLORS
    return f"""
    QWidget#launcher {{
        background-color: {c["bg"]};
        border-radius: 10px;
    }}

    QLineEdit#search_input {{
        background-color: {c["input_bg"]};
        color: {c["text"]};
        border: 1px solid {c["border"]};
        border-radius: 6px;
        padding: 10px 14px;
        font-size: 16px;
        selection-background-color: {c["selection"]};
    }}

    QLineEdit#search_input:focus {{
        border: 1px solid {c["selection"]};
    }}

    QListWidget#results {{
        background-color: transparent;
        border: none;
        outline: none;
        padding: 4px 0px;
    }}

    QListWidget#results::item {{
        color: {c["text"]};
        padding: 8px 14px;
        border-radius: 4px;
        margin: 1px 4px;
    }}

    QListWidget#results::item:selected {{
        background-color: {c["selection"]};
        color: {c["text"]};
    }}

    QListWidget#results::item:hover {{
        background-color: {c["hover"]};
    }}

    QLabel#no_results {{
        color: {c["text_dim"]};
        font-size: 14px;
        padding: 20px;
    }}
    """
