from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
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
from ui.styles import COLORS, WINDOW_HEIGHT, WINDOW_WIDTH, get_stylesheet


class LauncherWindow(QWidget):
    def __init__(self, games: list[Game], parent: QWidget | None = None):
        super().__init__(parent)
        self._all_games = games
        self._game_map: dict[str, Game] = {g.appid: g for g in games}
        self._favorites = load_favorites()
        self._filtered_games: list[Game] = []

        self.setWindowTitle("LudexHub")
        self.setObjectName("launcher")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setStyleSheet(get_stylesheet())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        self._search_input = QLineEdit()
        self._search_input.setObjectName("search_input")
        self._search_input.setPlaceholderText("Search games...")
        self._search_input.textChanged.connect(self._on_search)
        self._search_input.returnPressed.connect(self._on_launch)
        layout.addWidget(self._search_input)

        self._results = ResultsList(favorites=self._favorites)
        self._results.favorite_toggled.connect(self._on_toggle_favorite)
        layout.addWidget(self._results)

        self._show_recents()

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
            self.hide()
        else:
            self.show_centered()

    def refresh_games(self) -> None:
        self._all_games = get_games()
        self._game_map = {g.appid: g for g in self._all_games}
        self._on_search(self._search_input.text())

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.hide()
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
