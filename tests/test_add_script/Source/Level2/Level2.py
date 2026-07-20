from ursina import *

if __name__ == "__main__":
    from enemy.enemy import *
else :
    from .enemy.enemy import *
# from .enemy.enemy import enemy
# from .fire.fire import fire
# from .player.player import player
run_scene = True

class Level2():
    def __init__(self):
        self.ememy = enemy()
        # self.fire = fire()
        # self.player = player()

if __name__ == "__main__":
    print("Run local")
    app = Ursina()

    Level2()

    app.run()