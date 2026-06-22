from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QListWidget, QListWidgetItem, QVBoxLayout, QWidget

from models.game import Game
from ui.styles import COLORS


class ResultsList(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._games: list[Game] = []

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._list = QListWidget()
        self._list.setObjectName("results")
        self._list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._layout.addWidget(self._list)

        self._no_results = QLabel("No games found")
        self._no_results.setObjectName("no_results")
        self._no_results.setAlignment(Qt.AlignCenter)
        self._no_results.setVisible(False)
        self._layout.addWidget(self._no_results)

    def update_results(self, games: list[Game]) -> None:
        self._games = games
        self._list.clear()

        if not games:
            self._list.setVisible(False)
            self._no_results.setVisible(True)
            return

        self._list.setVisible(True)
        self._no_results.setVisible(False)

        for game in games:
            item = QListWidgetItem(f"  {game.name}")
            item.setData(Qt.UserRole, game)
            self._list.addItem(item)

        self._list.setCurrentRow(0)

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
