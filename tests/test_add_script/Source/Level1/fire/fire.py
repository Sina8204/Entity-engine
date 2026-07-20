from ursina import *

class fire (Entity):
    def __init__(self, add_to_scene_entities=True, enabled=True, **kwargs):
        super().__init__(add_to_scene_entities, enabled, **kwargs)
        self.model = "cube"
        self.position = (1, 1, 0)
        self.color = (0.5, 0.2, 0.0 , 0.5)
        