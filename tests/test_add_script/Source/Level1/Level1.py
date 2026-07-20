from ursina import *
from .enemy.enemy import *
from .fire.fire import fire
from .player.player import player

class Level1:
    def __init__(self):
        self.ememy = enemy()
        self.fire = fire()
        self.player = player()

# app = Ursina()

# Level1()

# app.run()