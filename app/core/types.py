from typing import Literal, List
from core.constants import Player


UsablePlayer = Literal[Player.O, Player.X]

Board = List[List[Player]]
