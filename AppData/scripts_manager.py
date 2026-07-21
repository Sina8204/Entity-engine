import os , easygui , shutil , subprocess , sys , re



sourse = {
    "entity" : 
    f"""from ursina import *
--import--

--script--

class --name-- (Entity):
    def __init__(self, add_to_scene_entities=True, enabled=True, **kwargs):
        super().__init__(add_to_scene_entities, enabled, **kwargs)
        --attr--
        --add_script--
""" ,
    "scene" :
    f"""from ursina import *
--import--

class --name--:
    def __init__(self):
        --entity--
        --parent--

if __name__ == "__main__":
    app = Ursina()

    --name--()

    app.run()
""" ,
    "run" :
    f"""from ursina import *
from __Runner import run

app = Ursina()
run()
app.run()

""" ,
    "project" : """from ursina import *
--import--

class run:
    def __init__(self):
        --scene--

""" ,
    "scn_run": 
    f"""from ursina import *
from __ScnRunner import run

app = Ursina()
run()
app.run()

""" ,
    "scn" : """from ursina import *
--import--

class run:
    def __init__(self):
        --scene--

""" 
} 

class Script_Manager:
    def __init__(self):
        self.save_path = ''

        self.entity = ''
        self.scene = ''
        self.project = ''
        self.scn = ''

        self.main_path = ''
        self.opened_scene_path = ''

    ###################### push scripts ######################
    def create_entity_script(self , SceneName , scene_dict : dict):
        unattributes = ["children" , "model_path"]
        for Ent_name , attributes in list(scene_dict.items()):
            if Ent_name == "__names__" : continue
            #easygui.msgbox(msg=f"{Ent_name}\n{attributes}")
            self.script_entity(name=Ent_name , attrs=attributes)
            self.save_entity_script(scene_name = SceneName , ent_name = Ent_name)
            if len(list(attributes["children"].keys())) > 0:
                self.create_entity_script(SceneName , attributes["children"])
    
    def create_scene_script(self , Scene_Name , scene_data):
        folder_path = f"{self.save_path}/Source/{Scene_Name}"
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        self.create_entity_script(SceneName = Scene_Name , scene_dict = scene_data)
        self.script_scene(name = Scene_Name , ents = scene_data)
        self.save_scene_script(scene_name = Scene_Name)

    def create_project_script(self , scenes_list : dict , ProjectName):
        self.script_project(project_scenes = scenes_list)
        self.save_runner_script()
        self.save_project_script(project_name = ProjectName)
    
    def create_scn_runner_script(self , scenes_list : dict , SceneName):
        self.script_scn_runner(project_scenes = scenes_list , name=SceneName)
        self.save_scn_runner_script()
        self.save_scn_runner_source()
    ###################### push scripts ######################

    def remove_unavalable_ents_folder(self , path , avalable_entities : list):
        items = sorted(os.listdir(path))
        for item in items:
            item_path = os.path.join(path , item)
            if not os.path.isdir(item_path):
                continue
            ent_name = item
            if ent_name in avalable_entities:
                continue
            else:
                self._remove_folder(item_path)

    ###################### Preparing scripts ######################
    def script_entity(self , name : str , attrs : dict, modules = ()):
        self.entity = sourse["entity"].replace("--name--", name)
        tab_attr = "        "
        if len(modules) > 0:
            for module in modules:
                if isinstance(module , tuple):
                    self.entity = self.entity.replace("--import--", f"from {module[0]} import {module[1]}\n--import--")
                elif isinstance(module , list):
                    if isinstance(module[0] , tuple):
                        self.entity = self.entity.replace("--import--", f"from {module[0][0]} import {module[0][1]} as {module[1]}\n--import--")
                    else :
                        self.entity = self.entity.replace("--import--", f"import {module[0]} as {module[1]}\n--import--")
                else :
                    self.entity = self.entity.replace("--import--", f"import {module}\n--import--")
        unattributes = ["children" , "model_path"]
        print(f"----------------------- type attrs ==> {type(attrs)}")
        for attr , value in list(attrs.items()):
            if attr in unattributes : continue
            match(attr):
                case 'script' : self._add_script_to_entity(script = value)
                case 'texture' : self.entity = self.entity = self.entity.replace("--attr--", f"self.{attr} = load_texture('{value}')\n{tab_attr}--attr--")
                case 'model' : self.entity = self.entity = self.entity.replace("--attr--", f"self.{attr} = '{value}'\n{tab_attr}--attr--")
                case _ : self.entity = self.entity = self.entity.replace("--attr--", f"self.{attr} = {value}\n{tab_attr}--attr--")
            # if attr == 'script':
            #     self._add_script_to_entity(script = value)
            # elif attr == 'texture':
            #     self.entity = self.entity = self.entity.replace("--attr--", f"self.{attr} = load_texture('{value}')\n{tab_attr}--attr--")
            # else:
            #     self.entity = self.entity = self.entity.replace("--attr--", f"self.{attr} = {value}\n{tab_attr}--attr--")
        
        return
    
    def script_scene(self , name : str , ents : dict , parent = None):
        scene_name = name
        self.scene = sourse["scene"].replace("--name--", scene_name) if parent is None else self.scene
        tab_init = "        "
        
        for ent_name , attr in list(ents.items()):
            if ent_name == "__names__" : continue
            import_code = f"""if __name__ == "__main__":
    from {ent_name}.script import *
else :
    from .{ent_name}.script import *
--import--"""
            self.scene = self.scene.replace("--import--", f"{import_code}")
            self.scene = self.scene.replace("--entity--", f"self.{ent_name} = {ent_name}()\n{tab_init}--entity--")
            if not parent is None:
                self.scene = self.scene.replace("--parent--", f"self.{ent_name}.parent = self.{parent}\n{tab_init}--parent--")
            if len(list(attr["children"].keys())) > 0:
                self.scene = self.script_scene(name = scene_name , ents = attr["children"] , parent = ent_name)
        return self.scene

    def script_project(self , project_scenes : dict):
        check_main_scene = project_scenes["__main__"]
        main_scene = ''
        self.project = sourse["project"]
        if check_main_scene:
            if os.path.exists(project_scenes[check_main_scene]):
                main_scene = check_main_scene
            else :
                for scene_name , path in list(project_scenes.items()):
                    if scene_name == "__main__" : continue
                    if os.path.exists(path):
                        main_scene = scene_name
        else :
            for scene_name , path in list(project_scenes.items()):
                if scene_name == "__main__" : continue
                if os.path.exists(path):
                    main_scene = scene_name
        if main_scene:
            self.project = self.project.replace("--import--", f"from {main_scene} import *")
            self.project = self.project.replace("--scene--", f"self.{main_scene} = {main_scene}()")
        else :
            return "there isn't any scene to load"
        return self.project
    
    def script_scn_runner(self , project_scenes : dict , name = ''):
        print("------------------ run function ------------------------")
        check_scene = name
        main_scene = ''
        self.scn = sourse["scn"]
        if check_scene:
            print(f"------------------ enter check scene if => {check_scene} ------------------------")
            if os.path.exists(project_scenes[check_scene]):
                print(f"------------------ enter check path of scene => {project_scenes[check_scene]} ------------------------")
                main_scene = check_scene
                self.scn = self.scn.replace("--import--", f"from {main_scene} import *")
                self.scn = self.scn.replace("--scene--", f"self.{main_scene} = {main_scene}()")
                print(f"----------------------------\nscn source :\n{self.scn}\n------------------------")
            else :
                print(f"{check_scene} is not exists")
                return None
        return self.scn
    ###################### Preparing scripts ######################

    ###################### saving scripts ######################
    def save_entity_script(self , scene_name , ent_name):
        path = f"{self.save_path}/Source/{scene_name}/{ent_name}/script.py"
        folder_ent = f"{self.save_path}/Source/{scene_name}/{ent_name}"
        if not os.path.exists(folder_ent):
            os.mkdir(folder_ent)
        with open(path , "w+" , encoding='utf-8') as file:
            file.write(self.__remove_markers(self.entity , "--import--" , "--script--" , "--attr--" , "--add_script--"))
       
    def save_scene_script(self , scene_name):
        path = f"{self.save_path}/Source/{scene_name}/details.py"
        folder_path = f"{self.save_path}/Source/{scene_name}"
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        with open(path , "w+" , encoding='utf-8') as file:
            file.write(self.__remove_markers(self.scene , "--import--" , "--entity--" , "--parent--"))
        self.__make_init(path = f"{self.save_path}/Source/{scene_name}/__init__.py")
    
    def save_runner_script(self):
        path = f"{self.save_path}/Source/__Runner/run.py"
        if not os.path.exists(path):
            easygui.msgbox(title="Script path not found" , msg=f"Script path '{path}' is not exists.")
            return  
        with open(path , "w+" , encoding='utf-8') as file:
            file.write(self.__remove_markers(self.project , "--import--" , "--scene--"))
        self.__make_init(run_mode=True , path=f"{self.save_path}/Source/__Runner/__init__.py")
    
    def save_scn_runner_script(self):
        print(f"######################### enter function ##################")
        path = f"{self.save_path}/Source/__ScnRunner/run.py"
        if not os.path.exists(path):
            easygui.msgbox(title="Script path not found" , msg=f"Script path '{path}' is not exists.")
            return  
        with open(path , "w+" , encoding='utf-8') as file:
            print(f"################# opened path {path}")
            file.write(self.__remove_markers(self.scn , "--import--" , "--scene--"))
            test = self.__remove_markers(self.scn , "--import--" , "--scene--")
            print(f"#########################\nscript writed :\n{test}\n#####################")
        self.__make_init(run_mode=True , path = f"{self.save_path}/Source/__ScnRunner/__init__.py")
    

    def save_project_script(self , project_name):
        path = f"{self.save_path}/Source/{project_name}.py"
        if not os.path.exists(path):
            easygui.msgbox(title="Script path not found" , msg=f"Script path '{path}' is not exists.")
            return  
        with open(path , "w+" , encoding='utf-8') as file:
            file.write(sourse["run"])
    
    def save_scn_runner_source(self):
        path = f"{self.save_path}/Source/scn.py"
        if not os.path.exists(path):
            easygui.msgbox(title="Script path not found" , msg=f"Script path '{path}' is not exists.")
            return  
        with open(path , "w+" , encoding='utf-8') as file:
            file.write(sourse["scn_run"])

    ###################### saving scripts ######################
    def _add_script_to_entity(self , script):
        if not script is None and isinstance(script , dict) :
            script_source_path = script["source_path"]
            
            if not os.path.exists(script_source_path):
                easygui.msgbox(title='Entity script not found' , msg=f"path '{script_source_path}' is not exists")
                return
            with open (script_source_path , "r" , encoding="utf-8") as script_file: 
                script_name = script["name"]
                script_content = re.sub(r'^\s*from\s+ursina\s+import\s+\*\s*$', '', script_file.read(), flags=re.MULTILINE)
                self.entity = self.entity.replace("--script--", f"{script_content}")
                self.entity = self.entity.replace("--add_script--", f"self.add_script({script_name}(--args--))")
                args = ''
                kwargs = ''
                if len(script["args"]) > 0:
                    for arg in script["args"]:
                        args += f"{arg} , "
                    args = args.rstrip(", ")
                if len(script["kwargs"].keys()) > 0:
                    for key , script_value in list(script["kwargs"].items()):
                        kwargs += f", {key} = {script_value}"
                    if not args:
                        kwargs = kwargs.lstrip(", ")
                
                self.entity = self.entity.replace("--args--", f"{args}{kwargs}")
        
    def __make_init(self , path , run_mode = False):
        with open(path , 'w+' , encoding='utf-8') as file:
            if run_mode:
                file.write("from .run import *")
            else:
                file.write("from .details import *")

    def __remove_markers (self, scr , *markers):
        for marker in markers:
            scr = scr.replace(marker, "")
        return scr
    
    def _remove_folder(self , folder_path):
        try:
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                shutil.rmtree(folder_path)
                print(f"پوشه {folder_path} حذف شد.")
            else:
                print(f"پوشه {folder_path} وجود ندارد.")
        except PermissionError:
            print(f"خطا: دسترسی به {folder_path} وجود ندارد.")
        except Exception as e:
            print(f"خطا در حذف پوشه: {e}")

    def run_python_file_subprocess(self , file_path):
        """
        اجرای فایل پایتون با استفاده از subprocess
        """
        try:
            # اجرا با همان مفسر پایتون
            result = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                check=True
            )
            print("خروجی برنامه:")
            print(result.stdout)
            if result.stderr:
                print("خطاهای برنامه:")
                print(result.stderr)
            print(f"\nفایل {file_path} با موفقیت اجرا شد.")
            return result
        except subprocess.CalledProcessError as e:
            print(f"خطا در اجرای فایل: {e}")
            print(f"خروجی خطا: {e.stderr}")
        except FileNotFoundError:
            print(f"خطا: فایل {file_path} یافت نشد.")
        except Exception as e:
            print(f"خطای غیرمنتظره: {e}")

ScriptManager = Script_Manager()

if __name__ == "__main__":
    #print(sourse["project"])

#     use_script = """if __name__ == "__main__":
#     from ursina import *

# class move_player:
#     def __init__(self , key_up , key_down , key_right , key_left):
#         self.key_up = key_up
#         self.key_down = key_down
#         self.key_right = key_right
#         self.key_left = key_left
    
#     def update(self):
#         if held_keys[self.key_up]:
#             self.entity.y += time.dt
#         elif held_keys[self.key_down]:
#             self.entity.y -= time.dt
#         elif held_keys[self.key_right]:
#             self.entity.x += time.dt
#         elif held_keys[self.key_left]:
#             self.entity.x -= time.dt
#         """
    
    script_manager = Script_Manager()
    # imports = ("os" , ["tkinter" , "tk"] , ("tkinter" , "messagebox") , [("tkinter" , "filedialog") , "fg"])
    # attributs = {
    #     "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
    #     "color": [
    #         0.17616666853427887,
    #         0.16500000655651093,
    #         0.5,
    #         1.0
    #     ],
    #     "position": [
    #         -0.5347223281860352,
    #         0.0,
    #         0.0
    #     ],
    #     "rotation": [
    #         -0.0,
    #         45.0,
    #         0.0
    #     ],
    #     "scale": [
    #         1.0,
    #         1.0,
    #         1.0
    #     ],
    #     "children": {
    #         "Clothes": {
    #             "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
    #             "color": [
    #                 0.1731666624546051,
    #                 0.5,
    #                 0.12999999523162842,
    #                 0.7599999904632568
    #             ],
    #             "position": [
    #                 -1.3854167461395264,
    #                 0.0,
    #                 0.0
    #             ],
    #             "rotation": [
    #                 -0.0,
    #                 -0.0,
    #                 45.0
    #             ],
    #             "scale": [
    #                 1.0,
    #                 1.0,
    #                 1.0
    #             ],
    #             "children": {}
    #         }
    #     }
    # }
    # add_script = {
    #     "name" : "move_player" ,
    #     "source" : use_script ,
    #     "args" : ("w" , "s" , "d" , "a"),
    #     "kwargs" : {}
    # }

#     scenc_dict = {
#     "__names__": [],
#     "Friend": {
#         "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
#         "color": [
#             0.17616666853427887,
#             0.16500000655651093,
#             0.5,
#             1.0
#         ],
#         "position": [
#             -0.5347223281860352,
#             0.0,
#             0.0
#         ],
#         "rotation": [
#             -0.0,
#             45.0,
#             0.0
#         ],
#         "scale": [
#             1.0,
#             1.0,
#             1.0
#         ],
#         "children": {
#             "Clothes": {
#                 "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
#                 "color": [
#                     0.1731666624546051,
#                     0.5,
#                     0.12999999523162842,
#                     0.7599999904632568
#                 ],
#                 "position": [
#                     -1.3854167461395264,
#                     0.0,
#                     0.0
#                 ],
#                 "rotation": [
#                     -0.0,
#                     -0.0,
#                     45.0
#                 ],
#                 "scale": [
#                     1.0,
#                     1.0,
#                     1.0
#                 ],
#                 "children": {}
#             },
#             "Gun": {
#                 "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
#                 "color": [
#                     0.5,
#                     0.06499999761581421,
#                     0.06499999761581421,
#                     1.0
#                 ],
#                 "position": [
#                     1.170139193534851,
#                     0.0,
#                     0.0
#                 ],
#                 "rotation": [
#                     -0.0,
#                     -0.0,
#                     0.0
#                 ],
#                 "scale": [
#                     1.0,
#                     1.0,
#                     2.299999952316284
#                 ],
#                 "children": {}
#             }
#         }
#     },
#     "Hat": {
#         "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
#         "color": [
#             0.0,
#             0.49166667461395264,
#             0.5,
#             1.0
#         ],
#         "position": [
#             0.0,
#             1.3333333730697632,
#             0.0
#         ],
#         "rotation": [
#             -0.0,
#             -0.0,
#             0.0
#         ],
#         "scale": [
#             1.0,
#             1.0,
#             1.0
#         ],
#         "children": {}
#     }
# }
    
    project_scene = {
    "__main__": "",
    "player": "/media/sina/New Volume/python projects/Linux/Python/save_testing/test10/Assets/Enemy.json" , 
    "gun":  "/media/sina/New Volume/python projects/Linux/Python/save_testing/test10/Assets/t.json" ,
    "Friend": "/media/sina/New Volume/python projects/Linux/Python/save_testing/test10/Assets/g.json" ,
    "Enemy": "/media/sina/New Volume/python projects/Linux/Python/save_testing/test10/Assets/f.json"
}
    scene_code = script_manager.script_project(project_scenes=project_scene)
    print(scene_code)
    #script_manager.save_entity_script("/media/sina/New Volume/python projects/Linux/Python/Engine/AppData/test.py")
    #print(script)
    # from ursina import *
    # import os
    # import tkinter as tk
    # from tkinter import messagebox
    # from tkinter import filedialog as fg


    # if __name__ == "__main__":
    #     from ursina import *

    # class move_player:
    #     def __init__(self , key_up , key_down , key_right , key_left):
    #         self.key_up = key_up
    #         self.key_down = key_down
    #         self.key_right = key_right
    #         self.key_left = key_left
        
    #     def update(self):
    #         if held_keys[self.key_up]:
    #             self.entity.y += time.dt
    #         elif held_keys[self.key_down]:
    #             self.entity.y -= time.dt
    #         elif held_keys[self.key_right]:
    #             self.entity.x += time.dt
    #         elif held_keys[self.key_left]:
    #             self.entity.x -= time.dt
            

    # class player (Entity):
    #     def __init__(self, add_to_scene_entities=True, enabled=True, **kwargs):
    #         super().__init__(add_to_scene_entities, enabled, **kwargs)
    #         self.color = [0.17616666853427887, 0.16500000655651093, 0.5, 1.0]
    #         self.position = [-0.5347223281860352, 0.0, 0.0]
    #         self.rotation = [-0.0, 45.0, 0.0]
    #         self.scale = [1.0, 1.0, 1.0]

    #         self.add_script(move_player("w" , "s" , "d" , "a"))
        
    # app = Ursina()

    # player(model = "cube")

    # app.run()
