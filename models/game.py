from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Game:
    name: str
    appid: str
    library: str
    launcher: str = "steam"
    executable: str = ""
    favorite: bool = False

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "appid": self.appid,
            "library": self.library,
            "launcher": self.launcher,
            "executable": self.executable,
            "favorite": self.favorite,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Game:
        return cls(
            name=data["name"],
            appid=data["appid"],
            library=data.get("library", ""),
            launcher=data.get("launcher", "steam"),
            executable=data.get("executable", ""),
            favorite=data.get("favorite", False),
        )
