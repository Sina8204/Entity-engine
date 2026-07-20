from ursina import *
import os

# class name (Entity):
#     def __init__(self, add_to_scene_entities=True, enabled=True, **kwargs):
#         super().__init__(add_to_scene_entities, enabled, **kwargs)
#         %%init%%

#     def input(key):
#         pass

#     def update(self):
#         pass

class __ScriptManager:
    def __init__(self , path_init):
        self.path_ini = path_init
        self.script = ''
        pass
    
    def new_script(self , name):
        self.script = self.source(name)


    def add_attribute(self , **attr_name):
        attributes = ""
        for key , value in list(attr_name.items()):
            attributes += f"self.{key} = {value}\n\t"
        attributes += "--init--"
        self.script = self.script.replace( "--init--" , attributes)
    
    def add_module(self , *libs):
        libraries = ""
        for value in libs:
            if isinstance(value , tuple):
                libraries += f"from {value[0]} import {value[1]}\n"
            elif isinstance(value , list):
                if isinstance(value[0] , tuple):
                    libraries += f"from {value[0][0]} import {value[0][1]} as {value[1]}\n"
                libraries += f"import {value[0]} as {value[1]}\n"
            else :
                libraries += f"import {value}\n"
            
        libraries += "--import--"
        self.script = self.script.replace( "--import--" , libraries)

    def source(self , name):
        return f"""from ursina import *
--import--

class {name} (Entity):
    def __init__(self, add_to_scene_entities=True, enabled=True, **kwargs):
        super().__init__(add_to_scene_entities, enabled, **kwargs)
        --init--
        --add_script--
        """
    
    def __call__(self, *args, **kwds):
        return self.script

script_manager = __ScriptManager()
script_manager.new_script("player")
script_manager.add_attribute(model = '"cube"' , position = (1 , 2 , 3) , color = (4 , 5 , 6))
script_manager.add_module("os" , ('tkinter' , 'filedialog') , ['tkinter' , 'tk'])
print(script_manager())