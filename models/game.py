from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Game:
    name: str
    appid: str
    library: str
    favorite: bool = False

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "appid": self.appid,
            "library": self.library,
            "favorite": self.favorite,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Game:
        return cls(
            name=data["name"],
            appid=data["appid"],
            library=data["library"],
            favorite=data.get("favorite", False),
        )
