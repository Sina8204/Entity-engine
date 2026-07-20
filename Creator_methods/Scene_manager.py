from ursina import *
from .UI_classes import execute_file_module
from ursina.prefabs.dropdown_menu import DropdownMenu , DropdownMenuButton

class SceneManager():
    def __init__(self):
        pass

    def clear_scene(self):
        from AppData.ProjectData_manager import ProjectData
        #ProjectData_copy = ProjectData.data.copy()
        entities_to_remove = [e for e in scene.entities if ((e.name in ProjectData.data["__names__"]) and ((type(e) is not DropdownMenu) and (type(e) is not DropdownMenuButton)))]
        #print(f"#################\nProject data : {ProjectData}\nProject data copy : {ProjectData_copy}\n#################")
        for entity in entities_to_remove:
            try :
                entity.destroy_entity()
            except Exception as e:
                print(f"Error : {e}")
    
    def load_new_scene(self , details : dict , parent = None):
        Parent = parent
        for key , value in list(details.items()):
            if key == "__names__" : continue
            
            vec4_color = tuple(details[key]["color"])
            hsv_color = ()
            if isinstance(vec4_color, tuple) or isinstance(vec4_color, Vec4):
                hsv_color = Color(*vec4_color[:4])
            else:
                hsv_color = vec4_color
            attr = self._get_attr(data=details[key] , filter=['children' , 'model_path' , 'model'] , color = ('color' , hsv_color))
            e = execute_file_module(
                file_path = value["model_path"] , 
                model = value['model'],
                parent = Parent ,
                name = key ,
                **attr)
                # position = tuple(value["position"]) ,
                # rotation = tuple(value["rotation"]) ,
                # scale = tuple(value["scale"]) ,
                # color = hsv_color
                
            
            print(f"{e.name} scale ========> {e.scale} =========> type {type(e.scale)}")
            print(f"############## New entity created =======> {e.name} #####################")
            child_dict = value["children"].copy()
            if len(child_dict.keys()) > 0:
                self.load_new_scene(details = child_dict , parent = e)

    def _get_attr(self , data : dict , filter : list , **set_attr : tuple):
        args = {}
        for attr , value in list(data.items()):
            if attr not in filter :
                args.update({attr : value})
        
        for value in list(set_attr.values()):
            if isinstance(value , tuple):
                args[value[0]] = value[1]
        return args

