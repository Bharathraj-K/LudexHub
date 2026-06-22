from __future__ import annotations

import os
from models.game import Game


def launch_game(game: Game) -> None:
    os.system(f"start steam://rungameid/{game.appid}")
