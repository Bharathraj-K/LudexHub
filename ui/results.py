from __future__ import annotations

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWidgets import QLabel, QListWidget, QListWidgetItem, QMenu, QVBoxLayout, QWidget

from core.icon_loader import IconLoader
from models.game import Game
from ui.styles import COLORS

FAVORITE_STAR = "\u2605"
EMPTY_STAR = "  "


class ResultsList(QWidget):
    favorite_toggled = Signal(object)

    def __init__(self, favorites: set[str] | None = None, parent: QWidget | None = None):
        super().__init__(parent)
        self._games: list[Game] = []
        self._favorites = favorites or set()
        self._appid_to_items: dict[str, list[QListWidgetItem]] = {}
        self._icon_loader = IconLoader(self)
        self._icon_loader.image_ready.connect(self._on_icon_ready)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._list = QListWidget()
        self._list.setObjectName("results")
        self._list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._list.setIconSize(self._list.iconSize().scaled(120, 45, Qt.KeepAspectRatio))
        self._list.setContextMenuPolicy(Qt.CustomContextMenu)
        self._list.customContextMenuRequested.connect(self._show_context_menu)
        self._layout.addWidget(self._list)

        self._no_results = QLabel("No games found")
        self._no_results.setObjectName("no_results")
        self._no_results.setAlignment(Qt.AlignCenter)
        self._no_results.setVisible(False)
        self._layout.addWidget(self._no_results)

    def set_favorites(self, favorites: set[str]) -> None:
        self._favorites = favorites

    def update_results(self, games: list[Game]) -> None:
        self._games = games
        self._appid_to_items.clear()
        self._list.clear()

        if not games:
            self._list.setVisible(False)
            self._no_results.setVisible(True)
            return

        self._list.setVisible(True)
        self._no_results.setVisible(False)

        for game in games:
            star = FAVORITE_STAR if game.appid in self._favorites else EMPTY_STAR
            item = QListWidgetItem(f" {star}  {game.name}")
            item.setData(Qt.UserRole, game)
            self._list.addItem(item)

            self._appid_to_items.setdefault(game.appid, []).append(item)
            self._icon_loader.load_icon(game.appid)

        self._list.setCurrentRow(0)

    @Slot(str, QPixmap)
    def _on_icon_ready(self, appid: str, pixmap: QPixmap) -> None:
        items = self._appid_to_items.get(appid, [])
        icon = QIcon(pixmap)
        for item in items:
            item.setIcon(icon)

    def _show_context_menu(self, pos) -> None:
        item = self._list.itemAt(pos)
        if item is None:
            return

        game: Game = item.data(Qt.UserRole)
        if game is None:
            return

        menu = QMenu(self)
        is_fav = game.appid in self._favorites
        action_text = "Remove from Favorites" if is_fav else "Add to Favorites"
        action = menu.addAction(action_text)
        action.triggered.connect(lambda: self.favorite_toggled.emit(game))
        menu.exec(self._list.mapToGlobal(pos))

    def get_selected_game(self) -> Game | None:
        item = self._list.currentItem()
        if item is None:
            return None
        return item.data(Qt.UserRole)

    def navigate_up(self) -> None:
        row = self._list.currentRow()
        if row > 0:
            self._list.setCurrentRow(row - 1)

    def navigate_down(self) -> None:
        row = self._list.currentRow()
        if row < self._list.count() - 1:
            self._list.setCurrentRow(row + 1)

    @property
    def list_widget(self) -> QListWidget:
        return self._list
