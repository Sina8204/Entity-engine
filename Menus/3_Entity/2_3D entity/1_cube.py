from ursina import *
from Creator_methods import create_entity , custom_fd ,Browser, entity_buttons #, add_entity_to_dict , add_child_to_tree
from AppData import ProjectData
import json

# class cube(create_entity):
#     def __init__(self, add_to_scene_entities=True, enabled=True, Model = "cube" , Script = None , Parent = None, Name = 'cube' , Color = color.gray , Position = (0 , 0 , 0) , Rotation = (0 , 0 , 0) , Scale = (1 , 1 , 1) ,**kwargs):
#         super().__init__(add_to_scene_entities, enabled, **kwargs)
#         self.model=Model
#         counter = 1
#         while (Name in ProjectData.data["__names__"]):
#             Name = f"{Name}{counter}"
#             counter+=1
#         self.name = Name
#         self.position = Position
#         self.rotation = Rotation
#         self.scale = Scale
#         self.color= Color
#         #self.scale=(0.5, 0.5, 0.5)
#         self.details_entity = {
#                 "model_path" : "Menus/3_Entity/2_3D entity/1_cube.py",
#                 "model" : f"'{Model}'",
#                 "color" : tuple(self.color) ,
#                 "position" : tuple(self.position) ,
#                 "rotation" : tuple(self.rotation),
#                 "scale" : tuple(self.scale),
#                 "script" : Script ,
#                 "children" : {}
#         }
#         if Parent:
#             self.parent = Parent
#             #self.scale=(1, 1 , 1)
#             self.group_gismo.parent = self.parent
#             self.group_gismo.scale = (1 , 1 , 1)
#             self.group_gismo.world_rotation = (0 , 0, 0)
#             self.select_button = Parent.select_button.add_child(self.name, color=color.rgb(0.3, 0.6, 0.8) , new_job = self.select_button_job)
#             print(f'Parent ====> {self.group_gismo.rotation}')
#             #details = add_entity_to_dict(self , "Menus/3_Entity/2_3D entity/1_cube.py")
#             ProjectData.add_children(self.parent.name , self.name , self.details_entity)
#         else:
#             self.select_button = entity_buttons.add_child(self.name, color=color.rgb(0.3, 0.6, 0.8) , new_job = self.select_button_job)
#             ProjectData.add_entity_to_dict(self , **self.details_entity)
        
#         # test = json.dumps(ProjectData.data , ensure_ascii= False , indent=4)
#         # print(f'{self.name} entity created ====> {test}')
    
#     def select_button_job(self):
#         if self.is_selected:
#             self.deselect()
#         else:
#             self.select()


def main(
        model_path = '',
        model = "cube",
        parent = None , 
        name = 'cube' , 
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
    
    model_path = 'Menus/3_Entity/2_3D entity/1_cube.py'
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

