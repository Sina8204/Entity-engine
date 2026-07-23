# from ursina import *
# from Creator_methods import create_entity

# class diamond(create_entity):
#     def __init__(self, add_to_scene_entities=True, enabled=True, **kwargs):
#         super().__init__(add_to_scene_entities, enabled, **kwargs)
#         self.model='diamond'
#         self.color= color.gray  # رنگ تصادفی برای هر مکعب
#         self.scale=(0.5, 0.5, 0.5)
#         self.position=(0 , 0 , 0)


# def main():
#     diamond()

from ursina import *
from Creator_methods import create_entity , custom_fd ,Browser
from AppData import ProjectData
import json


def main(
        model_path = '',
        model = "diamond",
        parent = None , 
        name = 'diamond' , 
        color = color.gray , 
        position = (0 , 0 , 0) , 
        rotation = (0 , 0 , 0) , 
        scale = (1 , 1 , 1) , 
        texture = None ,
        script = None):
    #print(f'main parent ==> {parent}')
    if not Browser.project_path:
        custom_fd.show_msg(type='warnning' , box_title="Field at create entity" , msg="Create or open a project before operation create entity")
        return
    
    model_path = 'Menus/3_Entity/2_3D entity/3_diamond.py'
    if parent:
        return create_entity(
            model_path = model_path ,
            Model = model ,
            Name = name ,
            Position = position ,
            Rotation = rotation ,
            Scale = scale ,
            Color = color ,
            Parent = parent ,
            Texture = texture ,
            Script = script
            )
    else:
        return create_entity(
            model_path = model_path ,
            Model = model ,
            Name = name ,
            Position = position ,
            Rotation = rotation ,
            Scale = scale ,
            Color = color ,
            Texture = texture ,
            Script = script
        )

