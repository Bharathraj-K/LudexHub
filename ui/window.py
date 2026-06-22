from __future__ import annotations

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PySide6.QtGui import QKeyEvent, QLinearGradient, QColor, QPainter, QFontDatabase, QFont
from PySide6.QtWidgets import (
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from core.favorites import load_favorites, toggle_favorite
from core.launcher import launch_game
from core.recents import get_recent_appids
from core.scanner import get_games
from core.search import search_games
from models.game import Game
from ui.results import ResultsList
from ui.styles import COLORS, WINDOW_HEIGHT, WINDOW_WIDTH, get_font_path, get_stylesheet


class LauncherWindow(QWidget):
    def __init__(self, games: list[Game], font_family: str = "Orbitron", parent: QWidget | None = None):
        super().__init__(parent)
        self._all_games = games
        self._game_map: dict[str, Game] = {g.appid: g for g in games}
        self._favorites = load_favorites()
        self._filtered_games: list[Game] = []
        self._font_family = font_family
        self._fade_anim: QPropertyAnimation | None = None

        self._load_font()
        self._setup_window()
        self._build_ui()
        self._show_recents()

    def update_font(self, font_family: str) -> None:
        self._font_family = font_family
        self.setStyleSheet(get_stylesheet(self._font_family))
        self._results._font_family = font_family

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
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
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
        layout.setSpacing(10)

        self._search_input = QLineEdit()
        self._search_input.setObjectName("search_input")
        self._search_input.setPlaceholderText("SEARCH GAMES...")
        self._search_input.textChanged.connect(self._on_search)
        self._search_input.returnPressed.connect(self._on_launch)
        layout.addWidget(self._search_input)

        self._results = ResultsList(favorites=self._favorites, font_family=self._font_family)
        self._results.favorite_toggled.connect(self._on_toggle_favorite)
        layout.addWidget(self._results)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()

        gradient = QLinearGradient(0, 0, rect.width(), rect.height())
        gradient.setColorAt(0.0, QColor("#0F0A1A"))
        gradient.setColorAt(0.5, QColor("#16102A"))
        gradient.setColorAt(1.0, QColor("#1A1040"))
        painter.setBrush(gradient)
        painter.setPen(QColor(COLORS["accent"]))
        painter.drawRoundedRect(rect.adjusted(0, 0, -1, -1), 10, 10)

        painter.end()

    def _show_recents(self) -> None:
        recent_ids = get_recent_appids()
        seen: set[str] = set()
        games: list[Game] = []

        for appid in self._favorites:
            if appid in self._game_map:
                games.append(self._game_map[appid])
                seen.add(appid)

        for appid in recent_ids:
            if appid in self._game_map and appid not in seen:
                games.append(self._game_map[appid])
                seen.add(appid)

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
        self._all_games = get_games()
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
            x = (geo.width() - self.width()) // 2 + geo.x()
            y = (geo.height() - self.height()) // 3 + geo.y()
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
