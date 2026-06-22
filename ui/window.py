from __future__ import annotations

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PySide6.QtGui import QKeyEvent, QLinearGradient, QColor, QPainter, QFontDatabase, QFont, QIcon, QPen
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.favorites import load_favorites, toggle_favorite
from core.launcher import launch_game
from core.scanner import get_games
from core.search import search_games
from core.settings import load_settings
from models.game import Game
from ui.results import ResultsList
from ui.styles import COLORS, WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_OPACITY, FOOTER_HEIGHT, get_font_path, get_stylesheet


class LauncherWindow(QWidget):
    MARGIN = 20

    def __init__(self, games: list[Game], font_family: str = "Orbitron", position: str = "center", parent: QWidget | None = None):
        super().__init__(parent)
        self._all_games = games
        self._game_map: dict[str, Game] = {g.appid: g for g in games}
        self._favorites = load_favorites()
        self._filtered_games: list[Game] = []
        self._font_family = font_family
        self._position = position
        self._fade_anim: QPropertyAnimation | None = None

        settings = load_settings()
        self._win_width = settings.get("window_width", WINDOW_WIDTH)
        self._win_height = settings.get("window_height", WINDOW_HEIGHT)
        self._win_opacity = settings.get("window_opacity", WINDOW_OPACITY)
        self._hotkey_str = settings.get("hotkey", "alt+space")

        self._load_font()
        self._setup_window()
        self._build_ui()
        self._show_recents()

    def update_font(self, font_family: str) -> None:
        self._font_family = font_family
        self.setStyleSheet(get_stylesheet(self._font_family))
        self._results._font_family = font_family

    def update_position(self, position: str) -> None:
        self._position = position

    def apply_settings(self, settings: dict) -> None:
        self._win_width = settings.get("window_width", self._win_width)
        self._win_height = settings.get("window_height", self._win_height)
        self._win_opacity = settings.get("window_opacity", self._win_opacity)
        self._hotkey_str = settings.get("hotkey", self._hotkey_str)
        self.setFixedSize(self._win_width, self._win_height)
        self._update_hotkey_hints()
        self.update()

    def _load_font(self) -> None:
        font_path = get_font_path()
        if font_path:
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    self._font_family = families[0]

    def _setup_window(self) -> None:
        self.setWindowTitle("LudexHub")
        self.setObjectName("launcher")
        self.setFixedSize(self._win_width, self._win_height)
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(get_stylesheet(self._font_family))

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(0)

        title_bar = self._build_title_bar()
        layout.addWidget(title_bar)

        layout.addSpacing(6)

        search_row = self._build_search_row()
        layout.addLayout(search_row)

        layout.addSpacing(4)

        self._results = ResultsList(favorites=self._favorites, font_family=self._font_family)
        self._results.favorite_toggled.connect(self._on_toggle_favorite)
        layout.addWidget(self._results, 1)

        layout.addSpacing(4)

        footer = self._build_footer()
        layout.addWidget(footer)

    def _build_title_bar(self) -> QWidget:
        title_bar = QWidget()
        title_bar.setObjectName("title_bar")
        title_bar.setFixedHeight(48)
        h = QHBoxLayout(title_bar)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)

        settings = load_settings()
        icon_path = settings.get("tray_icon", "")
        self._icon_label = QLabel()
        icon = QIcon(icon_path)
        pixmap = icon.pixmap(50, 50)
        self._icon_label.setPixmap(pixmap)
        self._icon_label.setFixedSize(50, 50)
        h.addWidget(self._icon_label)

        h.addStretch()

        self._minimize_btn = QPushButton("\u2012")
        self._minimize_btn.setObjectName("minimize_btn")
        self._minimize_btn.setFixedSize(32, 32)
        self._minimize_btn.clicked.connect(self.showMinimized)
        h.addWidget(self._minimize_btn)

        h.addSpacing(4)

        self._close_btn_title = QPushButton("\u2715")
        self._close_btn_title.setObjectName("close_btn")
        self._close_btn_title.setFixedSize(32, 32)
        self._close_btn_title.clicked.connect(self._fade_out)
        h.addWidget(self._close_btn_title)

        return title_bar

    def _build_search_row(self) -> QHBoxLayout:
        self._search_row = QHBoxLayout()
        self._search_row.setSpacing(8)

        self._search_input = QLineEdit()
        self._search_input.setObjectName("search_input")
        self._search_input.setPlaceholderText("Search games...")
        self._search_input.textChanged.connect(self._on_search)
        self._search_input.returnPressed.connect(self._on_launch)
        self._search_row.addWidget(self._search_input)

        self._hotkey_hints: list[QLabel] = []
        parts = self._hotkey_str.split("+")
        for part in parts:
            hint = QLabel(part.upper())
            hint.setObjectName("hotkey_hint")
            hint.setAlignment(Qt.AlignCenter)
            hint.setFixedHeight(30)
            hint.setMinimumWidth(28)
            self._hotkey_hints.append(hint)
            self._search_row.addWidget(hint)

        return self._search_row

    def _update_hotkey_hints(self) -> None:
        for hint in self._hotkey_hints:
            self._search_row.removeWidget(hint)
            hint.setParent(None)
            hint.deleteLater()
        self._hotkey_hints.clear()

        parts = self._hotkey_str.split("+")
        for part in parts:
            hint = QLabel(part.upper())
            hint.setObjectName("hotkey_hint")
            hint.setAlignment(Qt.AlignCenter)
            hint.setFixedHeight(30)
            hint.setMinimumWidth(28)
            self._hotkey_hints.append(hint)
            self._search_row.addWidget(hint)

    def _build_footer(self) -> QWidget:
        footer = QWidget()
        footer.setObjectName("footer")
        footer.setFixedHeight(FOOTER_HEIGHT)
        h = QHBoxLayout(footer)
        h.setContentsMargins(8, 0, 8, 0)
        h.setSpacing(6)

        h.addWidget(self._make_key_label("\u2191\u2193"))
        h.addWidget(self._make_text_label("Navigate"))
        h.addSpacing(12)
        h.addWidget(self._make_key_label("\u21B5"))
        h.addWidget(self._make_text_label("Launch"))
        h.addSpacing(12)
        h.addWidget(self._make_key_label("Esc"))
        h.addWidget(self._make_text_label("Exit"))

        h.addStretch()
        return footer

    def _make_key_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("footer_key")
        label.setAlignment(Qt.AlignCenter)
        return label

    def _make_text_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("footer_text")
        return label

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        alpha = int(self._win_opacity * 255)

        gradient = QLinearGradient(0, 0, rect.width(), rect.height())
        gradient.setColorAt(0.0, QColor(11, 6, 20, alpha))
        gradient.setColorAt(0.5, QColor(17, 12, 34, alpha))
        gradient.setColorAt(1.0, QColor(11, 6, 20, alpha))
        painter.setBrush(gradient)

        pen = QPen(QColor(COLORS["accent"]))
        pen.setWidthF(1.5)
        painter.setPen(pen)
        painter.drawRoundedRect(rect.adjusted(0, 0, -1, -1), 12, 12)

        painter.end()

    def _show_recents(self) -> None:
        games: list[Game] = []

        for appid in self._favorites:
            if appid in self._game_map:
                games.append(self._game_map[appid])

        for game in sorted(self._all_games, key=lambda g: g.name.lower()):
            if game.appid not in self._favorites:
                games.append(game)

        self._results.set_favorites(self._favorites)
        self._results.update_results(games)

    def _on_search(self, text: str) -> None:
        if not text.strip():
            self._show_recents()
            return
        self._filtered_games = search_games(text, self._all_games)
        self._results.set_favorites(self._favorites)
        self._results.update_results(self._filtered_games)

    def _on_launch(self) -> None:
        game = self._results.get_selected_game()
        if game is not None:
            launch_game(game)
            self.hide()

    def _on_toggle_favorite(self, game: Game) -> None:
        toggle_favorite(game.appid)
        self._favorites = load_favorites()
        self._on_search(self._search_input.text())

    def toggle(self) -> None:
        if self.isVisible():
            self._fade_out()
        else:
            self.show_centered()

    def refresh_games(self) -> None:
        settings = load_settings()
        self._all_games = get_games(
            steam_override=settings.get("steam_path", ""),
            epic_override=settings.get("epic_path", ""),
            gog_override=settings.get("gog_path", ""),
        )
        self._game_map = {g.appid: g for g in self._all_games}
        self._on_search(self._search_input.text())

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self._fade_out()
        elif event.key() == Qt.Key_Up:
            self._results.navigate_up()
        elif event.key() == Qt.Key_Down:
            self._results.navigate_down()
        else:
            super().keyPressEvent(event)

    def show_centered(self) -> None:
        screen = self.screen()
        if screen is not None:
            geo = screen.availableGeometry()
            w, h = self.width(), self.height()
            m = self.MARGIN
            x, y = 0, 0

            if self._position == "top-left":
                x, y = geo.x() + m, geo.y() + m
            elif self._position == "top-center":
                x = geo.x() + (geo.width() - w) // 2
                y = geo.y() + m
            elif self._position == "top-right":
                x = geo.x() + geo.width() - w - m
                y = geo.y() + m
            elif self._position == "center":
                x = geo.x() + (geo.width() - w) // 2
                y = geo.y() + (geo.height() - h) // 2
            elif self._position == "bottom-left":
                x = geo.x() + m
                y = geo.y() + geo.height() - h - m
            elif self._position == "bottom-center":
                x = geo.x() + (geo.width() - w) // 2
                y = geo.y() + geo.height() - h - m
            elif self._position == "bottom-right":
                x = geo.x() + geo.width() - w - m
                y = geo.y() + geo.height() - h - m

            self.move(x, y)
        self.show()
        self.raise_()
        self.activateWindow()
        self._search_input.setFocus()
        self._search_input.clear()
        self._show_recents()
        self._fade_in()

    def _fade_in(self) -> None:
        self._fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_anim.setDuration(150)
        self._fade_anim.setStartValue(0.0)
        self._fade_anim.setEndValue(1.0)
        self._fade_anim.setEasingCurve(QEasingCurve.OutQuad)
        self._fade_anim.start()

    def _fade_out(self) -> None:
        self._fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self._fade_anim.setDuration(120)
        self._fade_anim.setStartValue(1.0)
        self._fade_anim.setEndValue(0.0)
        self._fade_anim.setEasingCurve(QEasingCurve.InQuad)
        self._fade_anim.finished.connect(self.hide)
        self._fade_anim.start()
