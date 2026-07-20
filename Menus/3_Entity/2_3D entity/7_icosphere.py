from ursina import *
from Creator_methods import create_entity

class icosphere(create_entity):
    def __init__(self, add_to_scene_entities=True, enabled=True, **kwargs):
        super().__init__(add_to_scene_entities, enabled, **kwargs)
        self.model='icosphere'
        self.color= color.gray  # رنگ تصادفی برای هر مکعب
        self.scale=(0.5, 0.5, 0.5)
        self.position=(0 , 0 , 0)


def main():
    icosphere()