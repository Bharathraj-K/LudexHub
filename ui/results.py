from __future__ import annotations

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QColor, QFontDatabase, QIcon, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QMenu, QVBoxLayout, QWidget

from core.icon_loader import IconLoader
from models.game import Game
from ui.styles import COLORS

FAVORITE_STAR = "\u2605"
LAUNCHER_COLORS = {
    "steam": COLORS["steam"],
    "epic": COLORS["epic"],
    "gog": COLORS["gog"],
}
LAUNCHER_LABELS = {
    "steam": "Steam",
    "epic": "Epic Games",
    "gog": "GOG",
}


class GameItemWidget(QWidget):
    def __init__(self, game: Game, is_favorite: bool, font_family: str = "Orbitron", parent=None):
        super().__init__(parent)
        self._game = game

        h = QHBoxLayout(self)
        h.setContentsMargins(8, 4, 12, 4)
        h.setSpacing(10)

        self._icon_label = QLabel()
        self._icon_label.setFixedSize(72, 54)
        self._icon_label.setAlignment(Qt.AlignCenter)
        h.addWidget(self._icon_label)

        self._star_label = QLabel()
        if is_favorite:
            self._star_label.setText(FAVORITE_STAR)
            self._star_label.setStyleSheet(f"color: {COLORS['accent_light']}; font-size: 16px; border: none; background: transparent;")
        else:
            self._star_label.setText("")
            self._star_label.setStyleSheet("border: none; background: transparent;")
        self._star_label.setFixedWidth(18)
        h.addWidget(self._star_label)

        self._name_label = QLabel(game.name)
        font = f"font-family: '{font_family}';" if font_family else ""
        self._name_label.setStyleSheet(f"color: {COLORS['text']}; font-size: 14px; {font} border: none; background: transparent;")
        h.addWidget(self._name_label, 1)

        launcher = game.launcher.lower()
        launcher_color = LAUNCHER_COLORS.get(launcher, COLORS["text_dim"])
        launcher_text = LAUNCHER_LABELS.get(launcher, launcher.capitalize())
        self._launcher_label = QLabel(launcher_text)
        self._launcher_label.setStyleSheet(f"color: {launcher_color}; font-size: 12px; border: none; background: transparent;")
        self._launcher_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        h.addWidget(self._launcher_label)

        self._arrow_label = QLabel("\u21B5")
        self._arrow_label.setStyleSheet(f"color: {COLORS['text_dim']}; font-size: 16px; border: none; background: transparent;")
        self._arrow_label.setAlignment(Qt.AlignCenter)
        self._arrow_label.setFixedWidth(24)
        h.addWidget(self._arrow_label)

    def set_icon(self, pixmap: QPixmap) -> None:
        scaled = pixmap.scaled(72, 54, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._icon_label.setPixmap(scaled)


class ResultsList(QWidget):
    favorite_toggled = Signal(object)

    def __init__(self, favorites: set[str] | None = None, font_family: str = "Orbitron", parent: QWidget | None = None):
        super().__init__(parent)
        self._games: list[Game] = []
        self._favorites = favorites or set()
        self._font_family = font_family
        self._appid_to_items: dict[str, list[QListWidgetItem]] = {}
        self._appid_to_widget: dict[str, GameItemWidget] = {}
        self._icon_loader = IconLoader(self)
        self._icon_loader.image_ready.connect(self._on_icon_ready)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._list = QListWidget()
        self._list.setObjectName("results")
        self._list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
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
        self._appid_to_widget.clear()
        self._list.clear()

        if not games:
            self._list.setVisible(False)
            self._no_results.setVisible(True)
            return

        self._list.setVisible(True)
        self._no_results.setVisible(False)

        for game in games:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, game)
            item.setSizeHint(self._list.iconSize())
            self._list.addItem(item)

            is_fav = game.appid in self._favorites
            widget = GameItemWidget(game, is_fav, self._font_family)
            self._list.setItemWidget(item, widget)

            self._appid_to_items.setdefault(game.appid, []).append(item)
            self._appid_to_widget[game.appid] = widget
            self._icon_loader.load_icon(game.appid)

        self._list.setCurrentRow(0)

    @Slot(str, QPixmap)
    def _on_icon_ready(self, appid: str, pixmap: QPixmap) -> None:
        widget = self._appid_to_widget.get(appid)
        if widget:
            widget.set_icon(pixmap)

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
