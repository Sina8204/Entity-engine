from ursina import *
from Creator_methods import create_camera , custom_fd ,Browser, entity_buttons #, add_entity_to_dict , add_child_to_tree
from AppData import ProjectData


def main(
        parent = None , 
        model = '/camera.glb',
        name = 'camera' , 
        color = color.gray , 
        position = (0 , 0 , 0) , 
        rotation = (0 , 0 , 0) , 
        scale = (1 , 1 , 1) , 
        fov = 40 ,
        near_plane = 0.1 ,
        far_plane = 100.0 ,
        orthographic = False ,
        script = None):
    #print(f'main parent ==> {parent}')
    if not Browser.project_path:
        custom_fd.show_msg(type='warnning' , box_title="Field at create entity" , msg="Create or open a project before operation create entity")
        return
    
    if parent:
        return create_camera(
            Name = name ,
            Model=model ,
            Position = position ,
            Rotation = rotation ,
            Scale = scale ,
            Color = color ,
            fov = fov ,
            near_plane = near_plane ,
            far_plane = far_plane ,
            orthographic = orthographic ,
            Parent = parent ,
            Script = script
            )
    else:
        return create_camera(
            Name = name ,
            Model=model ,
            Position = position ,
            Rotation = rotation ,
            Scale = scale ,
            Color = color ,
            fov = fov ,
            near_plane = near_plane ,
            far_plane = far_plane ,
            orthographic = orthographic ,
            Script = script
        )

