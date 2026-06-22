from __future__ import annotations

import os
from models.game import Game
from core.recents import record_launch


def launch_game(game: Game) -> None:
    record_launch(game.appid)
    os.system(f"start steam://rungameid/{game.appid}")
