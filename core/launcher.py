from __future__ import annotations

import os
from pathlib import Path

from core.recents import record_launch
from models.game import Game


def launch_game(game: Game) -> None:
    record_launch(game.appid)

    if game.launcher == "steam":
        os.system(f"start steam://rungameid/{game.appid}")
    elif game.launcher == "epic":
        os.system(f'start "com.epicgames.launcher://apps/{game.appid}/action"')
    elif game.launcher == "gog":
        if game.executable and Path(game.executable).exists():
            os.system(f'start "" "{game.executable}"')
        else:
            os.system(f"start galaxy://launch/{game.appid}")
    else:
        if game.executable and Path(game.executable).exists():
            os.system(f'start "" "{game.executable}"')
