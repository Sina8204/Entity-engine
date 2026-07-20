from ursina import *
from Source.Level1.Level1 import Level1
from Source.Level2.Level2 import Level2

app = Ursina()

Level1()

def input(key):
    if key == "x":
        scene.clear()
        Level2()
        print(list(scene.children))
        print("---------------------------------")
    if key == "c":
        scene.clear()
        Level1()
        print(list(scene.children))
        print("---------------------------------")

app.run()
