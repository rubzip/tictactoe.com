from typing import Literal, List
from app.core.constants import Player


UsablePlayer = Literal[Player.O, Player.X]

BoardType = List[List[Player]]
