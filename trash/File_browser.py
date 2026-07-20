from ursina import *
from AppData import ProjectData , status , ScriptManager

from Creator_methods.Scene_manager import SceneManager
from Creator_methods import show_message
import os , json

import easygui
import subprocess
import os
import shutil


class FileBrowserOpen:
    def __init__(self , mode = 'new'):
        self.browser_open_mode = mode
        self.assets_folder_name = 'Assets'
        self.project_scenes_json_name = 'project_scenes.json'
        self.browser_title = ''
        self.project_name = ''
        self.project_path = ''
        self.scene_path = ''
        self.project_scenes = ''
        self.new_scene_name = 'new_scene'
        self.scenes_format = "_scene.json"

        self.project_scenes_json_main = "__main__"

    def new_project(self):
        self.project_name = easygui.enterbox(
            title = "Project name" ,
            msg="Enter your project name" 
        )

        if not self.project_name:
            easygui.msgbox(
                title="Field at create new project" , 
                msg="Canceling the new project creation operation"
            )
            return
        
        self.project_path = easygui.diropenbox(
            title="New project" ,
            msg=self.browser_title
        )

        if not os.path.exists(self.project_path):
            easygui.msgbox(
                title="Field at create new project" , 
                msg=f"The path you selected does not exists!\n'{self.project_path}'"
            )
            return

        if os.path.exists(f"{self.project_path}/{self.project_name}"):
            easygui.msgbox(
                title="Field at create new project" , 
                msg=f"there is a project with name you selected \n'{self.project_path}'"
            )
            return
        
        self.JsonFile = self.create_project(path=self.project_path , name=self.project_name)
        if isinstance(self.JsonFile , dict) and "project_path" in (list(self.JsonFile.keys())):
            if os.path.exists(self.JsonFile["project_path"]):
                scene_clear = SceneManager()
                scene_clear.clear_scene()
                # status["is_saved"] = True
                status["project_path"] = self.JsonFile["project_path"]
                status["scene"] = ''
                ProjectData.clear_data()
                #ProjectData.path = status["scene"]
                #ProjectData.save_data()
                print(f"Sucssfully at creat new project :\n\t opened scene : '{ProjectData.path}'")
        else:
            easygui.msgbox(title="Field at creat new project" , msg = "The path you selected is not exist\nsee the terminal")
            # self.show_error = show_message(win_title="Field at creat new project" , message="The path you selected is not exist\nsee the terminal")
            print(f"Error : \n\tpath '{self.project_path}/{self.project_name}.json' is not exist")
    
    def new_scene(self):
        scene_clear = SceneManager()
        scene_clear.clear_scene()
        new_scene = self.create_new_scene()
        if new_scene:
            status['scene'] = ''
            print(f"status[scene] closed")
        else :
            pass

    def open_project(self):
        scene_clear = SceneManager()
        project_path = easygui.diropenbox(
            title="Open project" ,
            msg=self.browser_title ,
        )

        if not os.path.exists(project_path) or not project_path:
            easygui.msgbox(
                title="Field at open project" , 
                msg=f"The path you selected does not exists!\n'{project_path}'"
            )
            return
        if not os.path.exists(f"{project_path}/{self.project_scenes_json_name}"):
            easygui.msgbox(
                title="Field at open project" , 
                msg=f"The folder you selected is not a project."
            )
            return 
        
        self.project_scenes = f"{project_path}/{self.project_scenes_json_name}"
        self.project_name = os.path.basename(project_path)
        with open(self.project_scenes , "r" , encoding="utf-8") as file:
            project_scenes = json.load(file)
            status["project_path"] = project_path
            loaded_scene_name = ''
            if project_scenes[self.project_scenes_json_main] and os.path.exists(project_scenes[self.project_scenes_json_main]):
                loaded_scene_name = project_scenes[self.project_scenes_json_main]

                status["scene"] = project_scenes[loaded_scene_name]
                ProjectData.path = status["scene"]

                scene_clear.clear_scene()

                with open(ProjectData.path, 'r', encoding='utf-8') as file:
                    ProjectData.data = json.load(file)
                ProjectData.load_scene()
                ScriptManager.save_path = status["project_path"]
                self.update_project_scenes_list()
                self.update_project()
                print(f"Successfully at open scene : '{ProjectData.path}'")
                return
            elif not project_scenes[self.project_scenes_json_main]:
                print("############################## enterd to project_scenes['main'] ##############################")
                for main_scene , scene in list(project_scenes.items()):
                    if scene is self.project_scenes_json_main : continue
                    if os.path.exists(scene):
                        loaded_scene_name = main_scene
                        status["scene"] = scene

                        ProjectData.path = status["scene"]

                        scene_clear.clear_scene()
                        with open(ProjectData.path, 'r', encoding='utf-8') as file:
                            ProjectData.data = json.load(file)
                        ProjectData.load_scene()
                        print(f"Successfully at open scene : '{ProjectData.path}'")
                        return
                    else:
                        continue
            else:
                scene_clear.clear_scene()
                status["scene"] = ''
                print(f"Successfully at open project : You are working at new scene")
                return
    
    def open_scene(self):
        scene_clear = SceneManager()
        if status["project_path"]:
            Asset_path = status["project_path"]+"/Assets/"
            scene_path = easygui.fileopenbox(
                        title="New project" ,
                        msg=self.browser_title ,
                        default=Asset_path ,
                        filetypes=[f"*{self.scenes_format}"]
                        )
            if not os.path.exists(scene_path):
                easygui.msgbox(
                    title="Field at open scene" , 
                    msg=f"path '{scene_path}' is not exists"
                    )
                return
            if not scene_path.startswith(Asset_path):
                easygui.msgbox(
                    title="Field at open scene" ,
                    msg=f"Project details must be in the 'Assets' folder of project. But you select a file out of Assets folder\n\tAssets path = {Asset_path}"
                    )
                return
            
            if not scene_path.endswith(self.scenes_format):
                easygui.msgbox(
                    title="Field at open scene" ,
                    msg=f"The file you selected is not a scene!!\nScenes format is {self.scenes_format} , but file you selected that name is not end with {self.scenes_format}\n\tFile selected = {scene_path}"
                    )
                return
            status["scene"] = scene_path

            scene_clear.clear_scene()
            ProjectData.path = status["scene"]
            with open(ProjectData.path, 'r', encoding='utf-8') as file:
                ProjectData.data = json.load(file)
            ProjectData.load_scene()
            print(f"Successfully at open scene : {ProjectData.path}")
            return
        else :
            easygui.msgbox(
                    title="Field at open scene" ,
                    msg=f"Open a project or create a new project before opening scene"
                    )
    
    def save_scene(self):
        if status["project_path"]:
            Asset_path = status["project_path"]+"/Assets/"
            if status["scene"]:
                scene_path = status["scene"]
                if scene_path.startswith(Asset_path):
                    if os.path.exists(scene_path):
                        ProjectData.path = status["scene"]
                        ProjectData.save_data()
                        self.update_scene(scene_name = str(Path(ProjectData.path).stem) , scene_dict = ProjectData.data)
                        print(f"Successfully at save data\n\t{ProjectData.path}")
                        return
                    else:
                        easygui.msgbox(
                        title="Field at save scene" , 
                        msg=f"path '{scene_path}' is not exists"
                        )
                        return
                else :
                    easygui.msgbox(
                    title="Field at save scene" , 
                    msg="Project details must be in the 'Assets' folder of project."
                    )
                    return
            else:
                #if self.scene_path:
                scene_name = easygui.enterbox(title = "Save scene" , msg="Enter a name for this scene")
                if not scene_name:
                    easygui.msgbox(title="Field at save scene" , msg="Canceling the save operation")
                    return
    
                scene_path = easygui.diropenbox(
                    title="New project" ,
                    msg=self.browser_title ,
                    default=Asset_path
                    )
                if not os.path.exists(scene_path):
                    easygui.msgbox(title="Field at save scene" , msg=f"Path '{scene_path}' is not exists!!")
                    return
                self.scene_path = f"{scene_path}/{scene_name}{self.scenes_format}"
                print(f"Asset path ==> {Asset_path}")
                print(f"scene path ==> {self.scene_path}")
                if not self.scene_path.startswith(Asset_path):
                    easygui.msgbox(title="Field at save scene" , msg=f"Project details must be in the 'Assets' folder of project.\nBut you ar use another path")
                    self.scene_path = ''
                    return
                if os.path.exists(f"{self.scene_path}"):
                    easygui.msgbox(title="Field at save scene" , msg=f"There is a scene with name '{scene_name}'\nTry agian and choose another name for the scene.")
                    self.scene_path = ''
                    return
                status["scene"] = self.scene_path
                ProjectData.path = status["scene"]
                ProjectData.save_data()
                self.insert_scene_details(scene_name , self.scene_path)
                print(f"Successfully at save data\n\t{ProjectData.path}")
                return
                #
        else:
            easygui.msgbox(title="Field at save scene" , msg=f"Open a project or create new project and open a scene before save scene.")
            return
        
    def save_scene_as(self):
        scene_path = status["scene"]
        project_path =  status["project_path"]
        if not os.path.exists(project_path):
            Asset_path = status["project_path"]+"/Assets/"
            easygui.msgbox(title="Field at save as operation" , msg=f"path '{project_path}' is not exists")
            return
        if not os.path.exists(scene_path):
            easygui.msgbox(title="Field at save as operation" , msg=f"scene '{scene_path}' is not exists")
            return
        if project_path and scene_path:
            new_scene_name = easygui.enterbox(title = "Save as scene" , msg="Enter a name for this scene")
            if not new_scene_name:
                easygui.msgbox(title="Field at save scene" , msg="Canceling the save operation")
                return
            scene_path_as = easygui.diropenbox(
                    title="New project" ,
                    msg=self.browser_title ,
                    default=Asset_path
                    )
            if not os.path.exists(scene_path_as):
                easygui.msgbox(title="Field at save as operation" , msg=f"path '{scene_path_as}' is not exists")
                return
            save_as_path = f"{scene_path_as}/{new_scene_name}{self.scenes_format}"
            if os.path.exists(save_as_path):
                easygui.msgbox(title="Field at save as operation" , msg=f"There is a scene with name '{new_scene_name}' in your selected path.\nTry again and choose defferent path or name")
                return
            status["scene"] = save_as_path
            ProjectData.path = status["scene"]
            ProjectData.save_data()

            self.insert_scene_details(new_scene_name , save_as_path)
            print(f"Successfully at save data\n\t{ProjectData.path}")

    def save_project(self):
        project_path = status["project_path"]
        if not status["project_path"]:
            easygui.msgbox(title="Field at save project" , msg=f"Open a project or create a new project befor saving project :)")
            return
        if not os.path.exists(status["project_path"]):
            easygui.msgbox(title="Field at save project" , msg=f"Project path is not exists :\n\t{project_path}")
            return
        self.update_project_scenes_list()
        self.update_project()
        with open (self.project_scenes , "r" , encoding="utf-8") as file:
            ScriptManager.create_project_script(name = self.project_name , scenes_list = json.load(file))
      
    def create_project(self, path, name=''):
        try:
            if not os.path.exists(f"{path}/{name}"):
                if os.path.exists(path):
                    os.mkdir(f"{path}/{name}")
                    print(f"Maked dir : '{path}/{name}'")
                    if os.path.exists(f"{path}/{name}"):
                        os.mkdir(f"{path}/{name}/Source")
                        print(f"Maked dir : {path}/{name}/Source")
                        if os.path.exists(f"{path}/{name}/Source"):
                            with open(f"{path}/{name}/Source/{name}.py" , "w+" , encoding="utf-8") as project_script:
                                project_script.write("")
                            if not os.path.exists(f"{path}/{name}/Source/{name}.py"):
                                easygui.msgbox(title="Field at create new project" , msg=f"file '{path}/{name}/Source/{name}.py' doesn't created :|")
                                return
                        else:
                            easygui.msgbox(title="Field at create new project" , msg=f"Source folder doesn't created :|\n\t'{path}/{name}/Source' ")
                            return
                    else:
                        easygui.msgbox(title="Field at create new project" , msg=f"Project '{name}' folder doesn't created :|\n\t'{path}/{name}' ")
                        return
                else:
                    easygui.msgbox(title='Field at create projec' , msg=f"path '{path}' is not exists!!")
                    return ''
            else :
                easygui.msgbox(title='Field at create projec' , msg=f"There is a folder with name '{name} in path \n\t'{path}'\nSelect another name for your project")
                return ''
            if os.path.exists(f"{path}/{name}"):
                os.mkdir(f"{path}/{name}/{self.assets_folder_name}")
                print(f"Maked dir : '{path}/{name}/{self.assets_folder_name}'")
            else:
                easygui.msgbox(title='Field at create projec' , msg=f"Field at creat path '{path}/{name}'!!")
                return ''
            if os.path.exists(f"{path}/{name}/{self.assets_folder_name}"):
                # json_path = f"{path}/{name}/{self.assets_folder_name}/new_scene.json"
                # with open(json_path, 'w+', encoding='utf-8') as file:
                #     json.dump({}, file, indent=2, ensure_ascii=False)
                self.project_scenes = f"{path}/{name}/{self.project_scenes_json_name}"
                with open(self.project_scenes , 'w+', encoding='utf-8') as file:
                    json.dump({self.project_scenes_json_main : ''}, file, indent=2, ensure_ascii=False)
                # print(f"Maked file : '{json_path}'")
                print(f"########################### Successfuly at creat '{name}' project ###########################")
                return {
                    "selected_path" : path ,
                    "project_path" : f"{path}/{name}" #,
                    #"json_path" : json_path
                }
        except FileExistsError:
            easygui.exceptionbox(title="Error" , msg="Project file does not exists.")
            return ''
        except Exception as e:
            print(f"Error creating folder: {e}")
            easygui.exceptionbox(title="Error" , msg="An unexpected error occurred.")
            return ''

    def create_new_scene(self):
        Asset_path = status["project_path"]
        Asset_path = f'{Asset_path}/{self.assets_folder_name}'
        if status["project_path"] and os.path.exists(status["project_path"]) and os.path.exists(Asset_path):
            project_path = Asset_path
            new_scene = f"{project_path}/{self.new_scene_name}{self.scenes_format}"
            counter = 0
            if not os.path.exists(new_scene):
                self.scene_path = new_scene
                # with open(new_scene, 'w+', encoding='utf-8') as file:
                #     json.dump({}, file, indent=2, ensure_ascii=False)
                print(f"Sucssfully at creat scene : '{new_scene}'")
            else :
                while(os.path.exists(new_scene)):
                    counter += 1
                    new_scene = f"{project_path}/{self.new_scene_name}{counter}{self.scenes_format}"
                    print(f"Update name scene : '{new_scene}'")
                self.scene_path = new_scene
                status['scene'] = ''
                print(f"Sucssfully at creat scene : '{new_scene}'")
            return True
        else :
            easygui.msgbox(title='Field at create new scene' , msg=f"Creat a new project or open a project before creating new scene")
            return False
    
    def insert_scene_details(self , name , path):
        with open(f"{self.project_scenes}" , "r" , encoding='utf-8') as file:
            new_data = json.load(file)
            new_data.update({name : path})
            with open(f"{self.project_scenes}" , "w+" , encoding='utf-8') as file:
                json.dump(new_data, file , ensure_ascii=False , indent=4)
            Scn_list = list(new_data.keys())
            Scn_list.remove("__main__")
            # self.update_project(scenes_list = Scn_list)
    
    def update_project_scenes_list(self):
        updated_scn_dict = self._get_project_scenes()
        with open(f"{self.project_scenes}" , "r" , encoding='utf-8') as file:
            data = json.load(file)
            if data["__main__"] and data["__main__"] in list(updated_scn_dict.keys()):
                updated_scn_dict["__main__"] = data["__main__"]
            elif len(list(updated_scn_dict.keys())) > 1:
                updated_scn_dict["__main__"] = list(updated_scn_dict.keys())[1]
            else :
                updated_scn_dict["__main__"] = ''
            
            with open(f"{self.project_scenes}" , "w+" , encoding='utf-8') as file:
                json.dump(updated_scn_dict, file , ensure_ascii=False , indent=4)
    
    def update_project(self):
        search_scenes_with_path = self._get_project_scenes()
        scenes_list = [scene_name for scene_name in search_scenes_with_path if scene_name != "__main__"]
        
        project_path = status["project_path"]
        source_path = f"{project_path}/Source"
        if project_path and os.path.exists(project_path):
            if not os.path.exists(source_path):
                easygui.msgbox(title=f"Source folder is not exists in your project path\n\t'{project_path}'")
                return
            
            items = sorted(os.listdir(source_path))

            for item in items:
                if item.startswith("__") : continue
                item_path = os.path.join(source_path, item)
                if not os.path.isdir(item_path):
                    continue
                scene_name = item
                if not scene_name in scenes_list:
                    self._remove_folder(item_path)
        
    
    def update_scene(self , scene_dict : dict , scene_name):
        entities_list = scene_dict["__names__"] if len(scene_dict["__names__"])> 0 else None
        if entities_list is None:
            entities_list = self._get_entities_list(scene_dict)
        project_path = status["project_path"]
        source_path = f"{project_path}/Source"
        scene_path = f"{source_path}/{scene_name}"
        if project_path and os.path.exists(project_path):
            if not os.path.exists(source_path):
                easygui.msgbox(title=f"Source folder is not exists in your project path\n\t'{project_path}'")
                return
            if not os.path.exists(scene_path):
                easygui.msgbox(title=f"scene folder is not exists in \n\t {source_path}\nCan not check path\n\t'{project_path}'")
                return
            items = sorted(os.listdir(scene_path))

            for item in items:
                if item.startswith("__") : continue
                item_path = os.path.join(scene_path, item)
                if not os.path.isdir(item_path):
                    continue
                ent_name = item
                if not ent_name in entities_list:
                    self._remove_folder(item_path)

    def _get_project_scenes(self , path = None):
        project_path = status["project_path"]
        check_folder = f"{project_path}/{self.assets_folder_name}" if path is None else path
        scn_dict = {"__main__" : ''}
        items = sorted(os.listdir(check_folder))
        for item in items:
            item_path = os.path.join(check_folder, item)
            if not os.path.isdir(item_path):
                if item.endswith(self.scenes_format):
                    scn_dict.update({item : item_path})
            else:
                scn_dict.update(self._get_project_scenes(item_path))
        return scn_dict

    @property
    def open_project_scenes(self):
        with open(f"{self.project_scenes}" , "r" , encoding='utf-8') as file:
            scn_list = json.load(file)
            return scn_list

    def _get_entities_list(self , scene : dict):
        ent_list = []
        for ent_name , ent_attr in list(scene.items()):
            if ent_name == "__names__" : continue
            ent_list.append(ent_name)
            if len(ent_attr["children"].keys()) > 0:
                ent_list.extend(self._get_entities_list(ent_attr["children"]))
        return ent_list

                    
    
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




                
Browser = FileBrowserOpen()
# class FileButtonSave(FileButton):
#     def on_click(self):
#         if len([e for e in self.parent.children if e.selected]) >= self.load_menu.selection_limit and not self.selected:
#             for e in self.parent.children:  # clear selection
#                 e.selected = False

#         self.selected = True
#         self.load_menu.file_name_field.text = str(self.path.name)

#     def on_double_click(self):
#         if self.path.is_dir():
#             self.load_menu.path = self.path
#         else:
#             self.selected = True
#             self.load_menu.open()

# @generate_properties_for_class()
# class FileBrowserOpen(FileBrowser):
#     def __init__(self, **kwargs):
#         super().__init__(file_button_class=FileButtonSave)
#         self.browser_open_mode = kwargs["mode"]
        
#         self.save_button = self.open_button
#         self.save_button.color = color.azure
#         self.save_button.text = 'Select this path'
#         match (self.browser_open_mode):
#             case "new" : 
#                 self.save_button.on_click = self._new
#                 self.title_bar.text = "Go to your path and enter a name for your project"
#             case "open" : 
#                 self.save_button.on_click = self._open
#                 self.title_bar.text = "Select *.json project file to open that"
#             case "save" : 
#                 self.save_button.on_click = self._save
#                 self.title_bar.text = "Save path: Go to your path and enter a name for your project"
#             case _ : self.save_button.on_click = lambda : print(f"{self.browser_open_mode} is not created")
        
#         self.file_name_field = InputField(parent=self, scale_x=.75, scale_y=self.save_button.scale_y, y=self.save_button.y)
#         self.save_button.y -= .075
#         self.cancel_button.y -= .075
#         self.file_name_field.text_field.text = ''
#         self.project_name = ''
#         self.project_path = ''
#         self.file_type = '' # to save as
#         self.show_error = None

#         self.last_saved_file = None     # gets set when you save a file

#         self._created_entities = []
#         self.overwrite_prompt = WindowPanel(
#             content=(
#                 Text('Overwrite?'),
#                 Button('Yes', color=color.azure),
#                 Button('Cancel')
#             ), z=-1, popup=True, enabled=False)
#         match (self.browser_open_mode):
#             case "new" : 
#                 self.overwrite_prompt = WindowPanel(
#                     content=(
#                         Text("The path you selected is already exists.\nPlease select an empty path with\n diffrent name"),
#                         Button('Ok', color=color.azure , on_click = self.hide_overwrite_promt)
#                     ), z=-1, popup=True, enabled=False)
#             case "open" : 
#                 self.overwrite_prompt = WindowPanel(
#                     content=(
#                         Text("The path you selected is not exists.\nPlease select an exists path"),
#                         Button('Ok', color=color.azure , on_click = self.hide_overwrite_promt)
#                     ), z=-1, popup=True, enabled=False)
#             case "save" : 
#                 self.overwrite_prompt = WindowPanel(
#                     content=(
#                         Text("The path you selected is already exists.\nThat file might have important details.\nPlease create project with diffrent name"),
#                         Button('Ok', color=color.azure , on_click = self.hide_overwrite_promt)
#                     ), z=-1, popup=True, enabled=False)
#         self._created_entities.append(self.overwrite_prompt)

#         for key, value in kwargs.items():
#             setattr(self, key ,value)

#     def file_type_setter(self, value):
#         self._file_type = value
#         self.file_types = (value, )

#     def on_enable(self):
#         super().on_enable()
#         self.file_name_field.active = True

#     def on_disable(self):
#         self.file_name_field.active = False

#     def hide_overwrite_promt(self):
#         if hasattr(self, 'overwrite_prompt'):
#             self.overwrite_prompt.enabled = None
#     def _new(self):
#         scene_clear = SceneManager()
#         scene_clear.clear_scene()
        
#         file_name = self.file_name_field.text_field.text.strip()
#         self.project_name = file_name
        
#         if not file_name:
#             self.show_error = show_message(
#                 win_title='Field to make project',
#                 message='Select a name for your project'
#             )
#             self._created_entities.append(self.show_error)  # ✅ اضافه شد
#             return

#         path = self.path / file_name
#         if path.exists() and hasattr(self, 'overwrite_prompt'):
#             try:
#                 if self.overwrite_prompt and not self.overwrite_prompt.is_empty():
#                     self.overwrite_prompt.enabled = True
#                     return
#                 else:
#                     self.create_overwrite_prompt()
#             except Exception as e:
#                 print(f"Error setting overwrite prompt: {e}")
#                 self.create_overwrite_prompt()
        
#         self.project_path = path
        
#         json_path = self.create_project(path=self.project_path, name=self.project_name)
#         if json_path:
#             status["is_saved"] = True
#             status["project_path"] = f"{self.project_path}/{self.project_name}.json"
#             ProjectData.clear_data()
#             ProjectData.path = status["project_path"]
#             ProjectData.save_data()
#             print(f"Sucssfully at creat new project :\n\t Project path : '{json_path}'")
#         else:
#             self.show_error = show_message(win_title="Field at creat new project" , message="The path you selected is not exist\nsee the terminal")
#             print(f"Error : \n\tpath '{json_path}' is not exist")
#         self.last_saved_file = path
        
#         if hasattr(self, 'overwrite_prompt') and self.overwrite_prompt:
#             try:
#                 if not self.overwrite_prompt.is_empty():
#                     self.overwrite_prompt.enabled = False
#             except:
#                 pass
        
#         self.close()
#         #self.on_submit(path)

#     def _open(self):
#         scene_clear = SceneManager()
#         scene_clear.clear_scene()
#         # ProjectData.data.clear()
        
#         file_name = self.file_name_field.text_field.text.strip()
#         self.project_name = file_name

#         path = self.path / file_name
        
#         if not path.exists() and hasattr(self, 'overwrite_prompt'):
#             try:
#                 if self.overwrite_prompt and not self.overwrite_prompt.is_empty():
#                     self.overwrite_prompt.enabled = True
#                 else:
#                     self.create_overwrite_prompt()
#                     if self.overwrite_prompt:
#                         self.overwrite_prompt.enabled = True
#                 return
#             except Exception as e:
#                 print(f"Error setting overwrite prompt in _open: {e}")
#                 self.create_overwrite_prompt()
        
#         self.project_path = path
        
#         status["is_saved"] = True
#         status["project_path"] = self.project_path
#         ProjectData.path = status["project_path"]
#         print(f"Project path ==> {ProjectData.path}\n--------------------------")
        
#         try:
#             if not os.path.isdir(ProjectData.path):
#                 with open(ProjectData.path, 'r', encoding='utf-8') as file:
#                     with open("AppData/last_data.json", 'w', encoding='utf-8') as current_file:
#                         json.dump(ProjectData.data , current_file , ensure_ascii=False , indent=4)
#                     ProjectData.data = json.load(file)
#                 ProjectData.load_scene()
#                 if hasattr(self, 'overwrite_prompt') and self.overwrite_prompt:
#                     try:
#                         if not self.overwrite_prompt.is_empty():
#                             self.overwrite_prompt.enabled = False
#                     except Exception as e:
#                         print(f"Error disabling overwrite_prompt: {e}")
#                 self.close()
#                 #self.on_submit(path)
#             else :
#                 try:
#                     if self.overwrite_prompt and not self.overwrite_prompt.is_empty():
#                         self.overwrite_prompt.content[0].text = "The path you selected is a directory.\nPlease select an true json file \nthat have true details."
#                         self.overwrite_prompt.enabled = True
#                     else:
#                         self.create_overwrite_prompt()
#                         if self.overwrite_prompt:
#                             self.overwrite_prompt.enabled = True
#                 except Exception as e:
#                     print(f"Error setting overwrite prompt in _open: {e}")
#                     self.create_overwrite_prompt()
#             return
#         #except IsADirectoryError as e:   
#         except Exception as e:
#             with open("AppData/last_data.json", 'r', encoding='utf-8') as current_file:
#                 ProjectData.data = json.load(current_file)
#             print(f"Error loading project: {e}")
#             self.show_error = show_message(
#                 win_title='Error Loading Project',
#                 message=f'Could not load project: {e}'
#             )
#             self._created_entities.append(self.show_error)  # ✅ اضافه شد
        
#         self.last_saved_file = path

#     def _save(self):
#         file_name = self.file_name_field.text_field.text.strip()
#         self.project_name = file_name
        
#         if not file_name:
#             self.show_error = show_message(
#                 win_title='Field to make project',
#                 message='Select a name for your project'
#             )
#             self._created_entities.append(self.show_error)  # ✅ اضافه شد
#             return

#         path = self.path / file_name
        
#         if path.exists() and hasattr(self, 'overwrite_prompt'):
#             try:
#                 if self.overwrite_prompt and not self.overwrite_prompt.is_empty():
#                     self.overwrite_prompt.enabled = True
#                 else:
#                     self.create_overwrite_prompt()
#                     if self.overwrite_prompt:
#                         self.overwrite_prompt.enabled = True
#                 return
#             except Exception as e:
#                 print(f"Error setting overwrite prompt in _save: {e}")
#                 self.create_overwrite_prompt()
#         self.project_path = path
        
#         try:
#             json_path = self.create_project(self.project_path, self.project_name)
            
#             status["is_saved"] = True
#             status["project_path"] = json_path
#             ProjectData.path = status["project_path"]
#             ProjectData.save_data()
#             if hasattr(self, 'overwrite_prompt') and self.overwrite_prompt:
#                 try:
#                     if not self.overwrite_prompt.is_empty():
#                         self.overwrite_prompt.enabled = False
#                 except Exception as e:
#                     print(f"Error disabling overwrite_prompt: {e}")
#             self.close()
#         except Exception as e:
#             print(f"Error saving project: {e}")
#             self.show_error = show_message(
#                 win_title='Error Saving Project',
#                 message=f'Could not save project: {e}'
#             )
#             self._created_entities.append(self.show_error)  # ✅ اضافه شد
#             return
        
#         self.last_saved_file = path
        
#         #self.on_submit(path)

#     def on_submit(self, path):
#         try :
#             match (self.browser_open_mode):
#                 case "new" : self._new()
#                 case "open" : self._open()
#                 case "save" : 
#                     self._save()
#                     print("____________________________ i entered on_submit _____________________________")
#                 case "_" : print('save to path:', path, 'please implement .on_submit to handle saving')
#         except Exception as e:
#             print('save to path:', path, 'please implement .on_submit to handle saving')
#             print(f"Error :\n\t{e}")
        
    
#     def create_project(self, path, name=''):
#         try:
#             os.mkdir(path)
#             json_path = f"{path}/{name}.json"
#             with open(json_path, 'w+', encoding='utf-8') as file:
#                 json.dump({}, file, indent=2, ensure_ascii=False)
#             print(f"Successfully created folder '{path}'")
#             return json_path
#         except FileExistsError:
#             print(f"Failed to create folder '{path}'")
#             self.show_error = show_message(
#                 win_title='Failed to create folder',
#                 message='There is a folder with the name you entered'
#             )
#             self._created_entities.append(self.show_error)
#             return
#         except Exception as e:
#             print(f"Error creating folder: {e}")
#             self.show_error = show_message(
#                 win_title='Failed to create folder',
#                 message='See the terminal to read the error'
#             )
#             self._created_entities.append(self.show_error)  # ✅ اضافه شد
#             return
    
#     def _destroy_entity_safe(self, entity):
#         """Safe destroy method with proper None checking"""
#         try:
#             # ✅ بررسی کامل‌تر
#             if entity is None:
#                 return
            
#             # ✅ بررسی اینکه entity هنوز وجود دارد و active است
#             if hasattr(entity, 'active') and entity.active is not None:
#                 # فقط اگر active وجود داشت و boolean بود
#                 if isinstance(entity.active, bool):
#                     entity.active = False
            
#             # ✅ destroy کردن با try-except
#             try:
#                 destroy(entity)
#             except Exception as e:
#                 print(f"Error destroying entity: {e}")
                
#         except Exception as e:
#             print(f"Error in _destroy_entity_safe: {e}")
    
#     def close(self):
#         """Override close method to properly destroy all entities"""
#         try:
#             # ✅ گام ۱: غیرفعال کردن entityهای خودمان
#             for attr_name in ['overwrite_prompt', 'show_error', 'file_name_field', 
#                             'save_button', 'cancel_button']:
#                 if hasattr(self, attr_name):
#                     entity = getattr(self, attr_name)
#                     if entity is not None and hasattr(entity, 'active'):
#                         try:
#                             entity.active = False
#                         except:
#                             pass
            
#             # ✅ گام ۲: صدا زدن super().close() با try-except مخصوص
#             try:
#                 super().close()
#             except Exception as e:
#                 error_msg = str(e)
#                 if "'NoneType' object has no attribute 'active'" in error_msg:
#                     print("Super().close() encountered None active attribute - continuing")
#                 else:
#                     print(f"Unexpected error in super().close(): {e}")
            
#             # ✅ گام ۳: destroy کردن entityها
#             entities_to_destroy = []
            
#             # جمع‌آوری entityها
#             for attr_name in ['show_error', 'overwrite_prompt', 'file_name_field', 
#                             'save_button', 'cancel_button']:
#                 if hasattr(self, attr_name):
#                     entity = getattr(self, attr_name)
#                     if entity is not None:
#                         entities_to_destroy.append(entity)
#                         setattr(self, attr_name, None)
            
#             if hasattr(self, '_created_entities'):
#                 entities_to_destroy.extend(self._created_entities[:])
#                 self._created_entities.clear()
            
#             # destroy کردن entityها
#             for entity in entities_to_destroy:
#                 if entity is not None:
#                     try:
#                         # غیرفعال کردن قبل از destroy
#                         if hasattr(entity, 'active'):
#                             try:
#                                 entity.active = False
#                             except:
#                                 pass
#                         destroy(entity)
#                     except Exception as e:
#                         print(f"Error destroying entity: {e}")
            
#             # ✅ گام ۴: پاک کردن children
#             if hasattr(self, 'children'):
#                 try:
#                     self.children.clear()
#                 except:
#                     pass
            
#             # ✅ گام ۵: garbage collection
#             import gc
#             gc.collect()
            
#             print("FileBrowserOpen closed successfully.")
            
#         except Exception as e:
#             print(f"Error in close method: {e}")
#             # تلاش نهایی برای بستن
#             try:
#                 super().close()
#             except:
#                 pass
    
#     def create_overwrite_prompt(self):
#         """ایجاد یا بازسازی prompt برای تایید بازنویسی فایل"""
#         try:
#             if hasattr(self, 'overwrite_prompt') and self.overwrite_prompt:
#                 try:
#                     if not self.overwrite_prompt.is_empty():
#                         self._destroy_entity_safe(self.overwrite_prompt)
#                 except:
#                     pass
            
#             self.overwrite_prompt = WindowPanel(
#                 content=(
#                     Text('Overwrite?'),
#                     Button('Yes', color=color.azure, on_click=self._save),
#                     Button('Cancel')
#                 ), 
#                 z=-1, 
#                 popup=True, 
#                 enabled=False
#             )
#             self._created_entities.append(self.overwrite_prompt)
#             return self.overwrite_prompt
            
#         except Exception as e:
#             print(f"Error creating overwrite prompt: {e}")
#             return None
        
#     def __call__(self, *args, **kwargs):
#         return {
#             "path": self.project_path,
#             "name": self.project_name
#         }