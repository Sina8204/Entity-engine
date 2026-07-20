from ursina import *

class player (Entity):
    def __init__(self, add_to_scene_entities=True, enabled=True, **kwargs):
        super().__init__(add_to_scene_entities, enabled, **kwargs)
        self.model = "cube"
        self.position = (1, 1, 0)
        self.color = (0.7, 0.4, 0.6 , 0.5)
        