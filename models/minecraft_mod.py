from enum import Enum
from typing import Any


class ModProvider(Enum):
    MODRINTH = 0,
    CURSEFORGE = 1


class MinecraftMod:
    id: str
    name: str
    categories: list[str]
    provider: ModProvider
    version: str
    alternation: Any
