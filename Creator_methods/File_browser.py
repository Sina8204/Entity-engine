from ursina import *
from AppData import ProjectData , ScriptManager

from Creator_methods.Scene_manager import SceneManager
from Creator_methods.Camera_controller import Active_camera_controller
import os , json

import easygui
import subprocess
import os
import shutil


class FileBrowserOpen:
    def __init__(self):
        self.project_path = ''
        self.opened_scene = ''

        self.project_name = ''
        self.opened_scene_name = ''
        self.Assets_path = ''

        self.scenes_dict_path = ''
        self.scenes_dict_file_name = 'project_scenes.json'

        self.assets_folder_name = "Assets"
        self.scene_format = ".scn.json"

        self.scene_manager = SceneManager()

    def new_project(self):
        project_name = easygui.enterbox(
            title = "Project name" ,
            msg="Enter your project name" 
        )

        if not project_name:
            easygui.msgbox(
                title="Field at create new project" , 
                msg="Canceling the new project creation operation"
            )
            return 'cancel'
        
        project_path = easygui.diropenbox(
            title="New project" ,
            msg="Select a path for the project"
        )

        if not os.path.exists(project_path):
            easygui.msgbox(
                title="Field at create new project" , 
                msg=f"The path you selected does not exists!\n'{project_path}'"
            )
            return None
        
        if os.path.exists(f"{project_path}/{project_name}"):
            easygui.msgbox(
                title="Field at create new project" , 
                msg=f"There is a project with your selected name in path \n'{project_path}'\n Try agian and use different name or another path"
            )
            return None
        
        project = self.create_project(path=project_path , name=project_name)
        if project:
            self.scene_manager.clear_scene()
            ProjectData.clear_data()
            self._close(mode="scene")
            Active_camera_controller.set_opened_scene_text(self.opened_scene)
            Active_camera_controller.set_opened_scene_source_text(self.opened_scene_name)
            
            print(f"Sucssfully at creat new project :\nproject name => {self.project_name}\nproject path => {self.project_path}")
            return True
        else:
            easygui.msgbox(title="Field at creat new project" , msg = "Unsuccessfully at create project operation")
            return False
    
    def save_scene(self):
        if self.project_path:
            self.Assets_path = f"{self.project_path}/{self.assets_folder_name}"
            if self.opened_scene:
                if self.opened_scene.startswith(self.Assets_path):
                    if not os.path.exists(self.opened_scene):
                        with open(self.opened_scene , "w+" , encoding="utf-8") as scene_file:
                            json.dump({} , scene_file , ensure_ascii=False , indent=4)
                    
                    self._save_data()
                    self._set_script_opened_scene_path()
                    
                    return True
                else:
                    easygui.msgbox(
                    title="Field at save scene" , 
                    msg="Project details must be in the 'Assets' folder of project."
                    )
                    return False
            else:
                self.opened_scene_name = easygui.enterbox(title = "Save scene" , msg="Enter a name for this scene")
                if not self.opened_scene_name:
                    easygui.msgbox(title="Field at save scene" , msg="Canceling the save operation")
                    self._close('scene')
                    return 'cancel'
                
                scene_path = easygui.diropenbox(
                    title="New project" ,
                    msg= "Select a path for the scene",
                    default=self.Assets_path
                    )
                if not os.path.exists(scene_path):
                    easygui.msgbox(title="Field at save scene" , msg=f"Path '{scene_path}' is not exists!!")
                    self._close('scene')
                    return 'cancel'
                if not scene_path.startswith(self.Assets_path):
                    print(f"opened scene : {scene_path}\nAsset path : {self.Assets_path}")
                    easygui.msgbox(title="Field at save scene" , msg=f"Project details must be in the 'Assets' folder of project.\nBut you are use another path")
                    self._close("scene")
                    return 'cancel'
                self.opened_scene = f"{scene_path}/{self.opened_scene_name}{self.scene_format}"
                if os.path.exists(f"{self.opened_scene}"):
                    easygui.msgbox(title="Field at save scene" , msg=f"There is a scene with name '{self.opened_scene_name}'\nTry agian and choose another name for the scene.")
                    self._close("scene")
                    return 'cancel'
                
                # ProjectData.path = self.opened_scene
                # ProjectData.source_path = self.project_path
                # ProjectData.save_data()
                self._save_data()
                self.update_project_scenes_dict_file()

                self._set_script_opened_scene_path()
                return True
        else:
            easygui.msgbox(title="Field at save scene" , msg=f"Open a project or create new project and open a scene before save scene.")
            self._close()
            return None

    def new_scene(self):
        if self.project_path:
            if self.opened_scene:
                # ProjectData.path = self.opened_scene
                # ProjectData.save_data()
                self._save_data(set_source_path = False)
                self.update_project_scenes_dict_file()
                self.scene_manager.clear_scene()
                self._close('scene')
                print("created new scene")
                return True
            else:
                if len(list(ProjectData.data.keys())) > 1:
                    user_choose = self._ChooseBox(
                    box_title = "Attention",
                    box_msg = "The scene you were working on has not been saved.\ndo you want to save it?")
                    match (user_choose):
                        case 0:
                            return self._save_emptyScene()
                        case 1:
                            self.scene_manager.clear_scene()
                            self._close('scene')
                            print("created new scene")
                            return True
                        case _:
                            print("Canceling new scene operation")
                            return 'cancel'
                else :
                    self.scene_manager.clear_scene()
                    print("*new scene was created")
                    return True
        else:
            easygui.msgbox(title="Field at operation create new scene" , msg="Create a project or open a project before creating new scene")
            return None
    def open_project(self):
        project_path = easygui.diropenbox(
            title="Open project" ,
            msg="Select path the project"
        )

        if not os.path.exists(project_path) or not project_path:
            easygui.msgbox(
                title="Field at open project" , 
                msg=f"The path you selected does not exists!\n'{project_path}'"
            )
            return 'cancel'
        if not os.path.exists(f"{project_path}/{self.scenes_dict_file_name}"):
            easygui.msgbox(
                title="Field at open project" , 
                msg=f"The folder you selected is not a project. Becuse the '{self.scenes_dict_file_name}' is not exists in '{project_path}' path"
            )
            return None
        self.project_path = project_path
        self.project_name = os.path.basename(project_path)
        self.Assets_path = f"{project_path}/{self.assets_folder_name}"
        self.scenes_dict_path = f"{project_path}/{self.scenes_dict_file_name}"
        self.opened_scene = self._receive_main_scene if not self._receive_main_scene is None else ''
        self.opened_scene_name = str(Path(self.opened_scene).stem) if not self.opened_scene is None else ''
        self.opened_scene_name = self.opened_scene_name if not self.opened_scene_name.endswith(".scn") else self.opened_scene_name.replace(".scn", '')
        if self.opened_scene:
            # ProjectData.path = self.opened_scene
            self._set_ProjectData_path()
            self.scene_manager.clear_scene()
            with open(ProjectData.path, 'r', encoding='utf-8') as file:
                ProjectData.data = json.load(file)
            ProjectData.load_scene()

            if self.opened_scene_name:
                if os.path.exists(f"{self.project_path}/Source/{self.opened_scene_name}/details.py"):
                    self._set_ProjectData_source_path()
            ScriptManager.save_path = self.project_path

            self._set_script_project_path()
            
            if self.opened_scene:
                self._set_script_opened_scene_path()
        else:
            easygui.msgbox(title = "There isn't any scene in this project" , msg="create a new scene and start use this project")
        return True

    def open_scene(self):
        if self.project_path:
            print(f"--------------- {self.Assets_path}")
            scene_path = easygui.fileopenbox(
                        title="Open scene" ,
                        msg="Select scene path" ,
                        default= f"{self.Assets_path}/" ,
                        filetypes=[f"*{self.scene_format}"]
                        )
            if not os.path.exists(scene_path):
                easygui.msgbox(
                    title="Field at open scene" , 
                    msg=f"path '{scene_path}' is not exists"
                    )
                return 'cancel'
            if not scene_path.startswith(self.Assets_path):
                easygui.msgbox(
                    title="Field at open scene" ,
                    msg=f"Project details must be in the 'Assets' folder of project. But you select a file out of Assets folder\n\tAssets path = {self.Assets_path}"
                    )
                return 'cancel'
            
            if not scene_path.endswith(self.scene_format):
                easygui.msgbox(
                    title="Field at open scene" ,
                    msg=f"The file you selected is not a scene!!\nScenes format is {self.scenes_format} , but file you selected that name is not end with {self.scenes_format}\n\tFile selected = {scene_path}"
                    )
                return None
            self.opened_scene = scene_path
            self.opened_scene_name = str(Path(self.opened_scene).stem)
            self.opened_scene_name = self.opened_scene_name if not self.opened_scene_name.endswith(".scn") else self.opened_scene_name.replace(".scn", '')
            ScriptManager.create_scn_runner_script(scenes_list = self._receive_project_scenes_dict , SceneName = self.opened_scene_name)

            print(f"--------------- {self.Assets_path}\n----------------{self.opened_scene_name}")
        
            self.scene_manager.clear_scene()
            #ProjectData.path = self.opened_scene
            self._set_ProjectData_path()
            with open(ProjectData.path, 'r', encoding='utf-8') as file:
                ProjectData.data = json.load(file)
            ProjectData.load_scene()
            print(f"Successfully at open scene : {ProjectData.path}")
            if self.opened_scene_name:
                if os.path.exists(f"{self.project_path}/Source/{self.opened_scene_name}/details.py"):
                    self._set_ProjectData_source_path()
                else:
                    with open(f"{self.project_path}/Source/{self.opened_scene_name}/details.py" , "w+" , encoding='utf-8') as file:
                        file.write("")
                        self._set_ProjectData_source_path()
            return True
        else:
            easygui.msgbox(title="Field at open scene" , msg=f"Open a project or create a new project before opening scene")
            return False
        
    def save_scene_as(self):
        if not os.path.exists(self.project_path) or self.project_path == '':
            easygui.msgbox(title="Field at save as operation" , msg=f"path '{self.project_path}' is not exists")
            return None
        
        if not os.path.exists(self.opened_scene):
            easygui.msgbox(title="Field at save as operation" , msg=f"scene '{self.opened_scene}' is not exists")
            return 'cancel'
        
        if self.project_path and self.opened_scene:
            new_scene_name = easygui.enterbox(title = "Save as scene" , msg="Enter a name for this scene")
            if not new_scene_name:
                easygui.msgbox(title="Field at save scene" , msg="Canceling the save operation")
                return 'cancel'
            
            scene_path_as = easygui.diropenbox(
                    title="Save as" ,
                    msg="Select a path for save as" ,
                    default=self.Assets_path
                    )
            if not os.path.exists(scene_path_as):
                easygui.msgbox(title="Field at save as operation" , msg=f"path '{scene_path_as}' is not exists")
                return 'cancel'
            save_as_path = f"{scene_path_as}/{new_scene_name}{self.scene_format}"
            
            if not save_as_path.startswith(self.Assets_path):
                easygui.msgbox(title="Field at save as operation" , msg=f"Project details must be in Assets folder. Try again and save as this scene in path '{self.Assets_path}'")
                return 'cancel'
            
            if os.path.exists(save_as_path):
                easygui.msgbox(title="Field at save as operation" , msg=f"There is a scene with name '{new_scene_name}' in your selected path.\nTry again and choose defferent path or name")
                return False
            
            self.opened_scene = save_as_path
            self.opened_scene_name = new_scene_name #str(Path(self.opened_scene).stem)
            # ProjectData.path = self.opened_scene
            # ProjectData.source_path = self.project_path
            # ProjectData.save_data()
            self._save_data()
            self.update_project_scenes_dict_file()
            print(f"Successfully at save data\n\t{ProjectData.path}")
            
            self._set_script_opened_scene_path()
            return True
            
    def save_project(self):
        if not self.project_path:
            easygui.msgbox(title="Field at save project" , msg="Open a project or creat a new project befor operation save project.")
            return None
        if not os.path.exists(self.project_path):
            easygui.msgbox(title="Field at save project" , msg=f"Project path is not exists!! \n\t{self.project_path}")
            return 'cancel'
        self.update_project_scenes_dict_file()
        if not self._receive_project_scenes_dict is None:
            if len(list(self._receive_project_scenes_dict.keys())) > 1:
                check_rm_unavalable_scn = self._remove_unavailable_scene(list(self._receive_project_scenes_dict.keys()))
                ScriptManager.save_path = self.project_path
                if check_rm_unavalable_scn:
                    ScriptManager.save_path = self.project_path
                    ScriptManager.create_project_script(ProjectName = self.project_name , scenes_list = self._receive_project_scenes_dict)
                    
                    self._set_script_project_path()
                    return True
                if check_rm_unavalable_scn == False:
                    ScriptManager.save_path = self.project_path
                    ScriptManager.create_project_script(ProjectName = self.project_name , scenes_list = self._receive_project_scenes_dict)
                    self._set_script_project_path()
                    return False
                else:
                    ScriptManager.save_path = ''
                    return None
            else:
                easygui.msgbox(title="Field at creat project script" , msg=f"'{self.project_path}/Scene/{self.project_name}.py' not created.Because ther isn't any scene in this project.")
                return False
        else:
            easygui.msgbox(title="Field at save project" , msg=f"The value of _receive_project_scenes_dict is None !! \nCheck '{self.scenes_dict_path}' path")
            return False
            


    def create_project(self , path , name):
        try :
            if os.path.exists(path):
                if not os.path.exists(f"{path}/{name}"):
                    os.mkdir(f"{path}/{name}")
                    print(f"Maked dir : '{path}/{name}'")
                    self.project_path = f"{path}/{name}"
                    self.project_name = f"{name}"
                    if os.path.exists(f"{self.project_path}"):
                        os.mkdir(f"{self.project_path}/Source")
                        print(f"Maked dir : {self.project_path}/Source")
                        os.mkdir(f"{self.project_path}/{self.assets_folder_name}")
                        os.mkdir(f"{self.project_path}/Source/__{self.assets_folder_name}")
                        self.Assets_path = f"{self.project_path}/{self.assets_folder_name}"
                        print(f"Maked dir : '{self.Assets_path}")
                        self.scenes_dict_path = f"{self.project_path}/{self.scenes_dict_file_name}"
                        with open(self.scenes_dict_path , 'w+', encoding='utf-8') as file:
                            json.dump({'__main__' : ''}, file, indent=2, ensure_ascii=False)
                        if os.path.exists(f"{self.project_path}/Source"):
                            os.mkdir(f"{self.project_path}/Source/__Runner")
                            os.mkdir(f"{self.project_path}/Source/__ScnRunner")
                            with open(f"{self.project_path}/Source/__Runner/run.py" , "w+" , encoding="utf-8") as runner_script:
                                runner_script.write("")
                            with open(f"{self.project_path}/Source/__ScnRunner/run.py" , "w+" , encoding="utf-8") as scnrunner_script:
                                scnrunner_script.write("")
                            with open(f"{self.project_path}/Source/{self.project_name}.py" , "w+" , encoding="utf-8") as project_script:
                                project_script.write("")
                            with open(f"{self.project_path}/Source/scn.py" , "w+" , encoding="utf-8") as scn_script:
                                scn_script.write("")
                            if not os.path.exists(f"{self.project_path}/Source/{self.project_name}.py"):
                                easygui.msgbox(title="Field at create new project" , msg=f"file '{path}/{name}/Source/{name}.py' doesn't created :|")
                                self._close()
                                return False
                        else:
                            easygui.msgbox(title="Field at create new project" , msg=f"Source folder doesn't created :|\n\t'{path}/{name}/Source' ")
                            self._close()
                            return False
                    else:
                        easygui.msgbox(title="Field at create new project" , msg=f"Project '{name}' folder doesn't created :|\n\t'{path}/{name}' ")
                        self._close()
                        return False
                else:
                    easygui.msgbox(title='Field at create projec' , msg=f"path '{path}' is not exists!!")
                    self._close()
                    return False
            else :
                easygui.msgbox(title='Field at create projec' , msg=f"There is a folder with name '{name} in path \n\t'{path}'\nSelect another name for your project")
                self._close()
                return
            return True
        except FileExistsError:
            easygui.exceptionbox(title="Error" , msg="Project file does not exists.")
            return False
        except Exception as e:
            print(f"Error creating folder: {e}")
            easygui.exceptionbox(title="Error" , msg="An unexpected error occurred.")
            return False
    
    @property
    def _receive_project_scenes_dict(self):
        try:
            if not os.path.exists(self.scenes_dict_path):
                print(f"'{self.scenes_dict_path}' is not exists")
                easygui.msgbox(title=f"Field at open {self.scenes_dict_file_name}" , msg=f"'{self.scenes_dict_path}' is not exists")
                return None
            with open(self.scenes_dict_path , 'r' ,encoding='utf-8') as project_scenes_dict:
                return json.load(project_scenes_dict)
        except FileExistsError:
            easygui.msgbox(title="Field at save project" , msg=f"Unreceive project scenes list :\n\t{self.scenes_dict_path}")
            return None
        except Exception as e:
            easygui.msgbox(title="Error at receive project scenes list" , msg=f"Error : {e}'\n\t{self.scenes_dict_path}'")
            return None

    @property
    def _receive_main_scene(self):
        scenes_dict = self._receive_project_scenes_dict
        if not scenes_dict is None:
            scn_names = list(scenes_dict.keys())
            if "__main__" in scn_names:
                scn_names.remove("__main__")
            if len(scn_names) > 0:
                if scenes_dict["__main__"]:
                    main_scene = scenes_dict["__main__"]
                    if main_scene in scn_names:
                        if os.path.exists(scenes_dict[main_scene]):
                            return scenes_dict[main_scene]
                        else:
                            return scenes_dict[scn_names[0]]
                    else:
                        return scenes_dict[scn_names[0]]
                else:
                    return scenes_dict[scn_names[0]]
            else:
                return None
        else:
            return None
    def update_project_scenes_dict_file(self):
        updated_scn_dict = self._get_project_scenes()
        with open(f"{self.scenes_dict_path}" , "r" , encoding='utf-8') as file:
            data = json.load(file)
            if data["__main__"] and data["__main__"] in list(updated_scn_dict.keys()):
                updated_scn_dict["__main__"] = data["__main__"]
            elif len(list(updated_scn_dict.keys())) > 1:
                updated_scn_dict["__main__"] = list(updated_scn_dict.keys())[1]
            else :
                updated_scn_dict["__main__"] = ''
            
            with open(f"{self.scenes_dict_path}" , "w+" , encoding='utf-8') as file:
                json.dump(updated_scn_dict, file , ensure_ascii=False , indent=4)

    def _get_project_scenes(self , path = None):
        check_folder = f"{self.project_path}/{self.assets_folder_name}" if path is None else path
        scn_dict = {"__main__" : ''}
        items = sorted(os.listdir(check_folder))
        for item in items:
            item_path = os.path.join(check_folder, item)
            if not os.path.isdir(item_path):
                if item.endswith(self.scene_format):
                    item = item.replace(self.scene_format , '')
                    print(item)
                    scn_dict.update({item : item_path})
            else:
                scn_dict.update(self._get_project_scenes(item_path))
        return scn_dict
    


    def _ChooseBox(self , box_title = "" , box_msg = "" , box_chooses = ("Yes" , "No" , "Cancel")):
        return easygui.indexbox(title = box_title , msg = box_msg , choices = box_chooses)

    def _save_emptyScene(self):
        self.opened_scene_name = easygui.enterbox(title = "Save scene" , msg="Enter a name for this scene")
        if not self.opened_scene_name:
            easygui.msgbox(title="Field at save scene" , msg="Canceling the save operation")
            self._close('scene')
            return 'cancel'
        
        scene_path = easygui.diropenbox(
            title="New project" ,
            msg= "Select a path for the scene",
            default=self.Assets_path
            )
        if not os.path.exists(scene_path):
            easygui.msgbox(title="Field at save scene" , msg=f"Path '{scene_path}' is not exists!!")
            self._close('scene')
            return False
        if not scene_path.startswith(self.Assets_path):
            easygui.msgbox(title="Field at save scene" , msg=f"Project details must be in the 'Assets' folder of project.\nBut you ar use another path")
            self._close("scene")
            return False
        self.opened_scene = f"{scene_path}/{self.opened_scene_name}{self.scene_format}"
        if os.path.exists(f"{self.opened_scene}"):
            easygui.msgbox(title="Field at save scene" , msg=f"There is a scene with name '{self.opened_scene_name}'\nTry agian and choose another name for the scene.")
            self._close("scene")
            return False
        # ProjectData.path = self.opened_scene
        # ProjectData.source_path = self.project_path
        # ProjectData.save_data()
        self._save_data()
        self.update_project_scenes_dict_file()
        self.scene_manager.clear_scene()
        self._close('scene')
        print("created new scene")
        return True
    
    def _remove_unavailable_scene(self , scenes_list : list):
        if self.project_path:
            if os.path.exists(self.project_path):
                if os.path.exists(f"{self.project_path}/Source"):
                    source_path = f"{self.project_path}/Source"
                    items = sorted(os.listdir(source_path))
                    scenes_list.remove("__main__")
                    for item in items:
                        if item.startswith("__"): continue
                        item_path = os.path.join(source_path, item)
                        if not os.path.isdir(item_path):
                            continue
                        scene_name = item
                        if scene_name in scenes_list:
                            continue
                        else:
                            self._remove_folder(item_path)
                    return True
                else:
                    os.mkdir(f"{self.project_path}/Source")
                    easygui.msgbox(title="Field at remove unavailable scenes" , msg=f"Created Source folder in project path. Because that was not exists.\n\t{self.project_path}/Source")
                    if not os.path.exists(f"{self.project_path}/Source"):
                        easygui.msgbox(title="Unavalable Source path" , msg=f"Source folder is not exists in '{self.project_name}' project.\nproject path : {self.project_path}")
                        return None
                    return False
            else:
                easygui.msgbox(title="Field at remove unavailable scenes" , msg=f"Project path is not exists : \n\t{self.project_path}")
                self._close()
                easygui.msgbox(title="Attention" , msg="Project is closed. open an existed project")
                return None
        else:
            easygui.msgbox(title="Field at remove unavailable scenes" , msg=f"Open a project or creat a new project befor operation save project.")
            return None


                    

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

    def _close(self , mode = 'all'):
        match (mode):
            case 'all' :
                self.project_path = ''
                self.opened_scene = ''
                self.project_name = ''
                self.opened_scene_name = ''
                self.scenes_dict_path = ''
                self.Assets_path = ''
            case 'scene':
                self.opened_scene = ''
                self.opened_scene_name = ''

    def _set_ProjectData_path(self):
        ProjectData.path = self.opened_scene
        opened_scene_relative_path = self.opened_scene.replace(self.Assets_path, '')
        Active_camera_controller.set_opened_scene_text(path = opened_scene_relative_path)
    
    def _set_ProjectData_source_path(self):
        ProjectData.source_path = f"{self.project_path}"
        opened_scene_source_relative_path = f"/Source/{self.opened_scene_name}/details.py"
        #ScriptManager.create_scn_runner_script(scenes_list = self._receive_project_scenes_dict , SceneName = self.opened_scene_name)
        Active_camera_controller.set_opened_scene_source_text(path = opened_scene_source_relative_path)

    def _save_data(self , set_source_path = True):
        self._set_ProjectData_path()
        if set_source_path:
            self._set_ProjectData_source_path()
        ProjectData.save_data()
    
    def _set_script_project_path(self):
        if os.path.exists(f"{ScriptManager.save_path}/Source/{self.project_name}.py"):
            ScriptManager.main_path = f"{ScriptManager.save_path}/Source/{self.project_name}.py"
        else:
            easygui.msgbox(title="Field at receive project source" , msg=f"path '{ScriptManager.save_path}/Source/{self.project_name}.py' is not exists")
        
    def _set_script_opened_scene_path(self):
        self.opened_scene_name = self.opened_scene_name if not self.opened_scene_name.endswith(".scn") else self.opened_scene_name.replace(".scn" , '')
        if os.path.exists(f"{self.project_path}/Source/{self.opened_scene_name}/details.py"):
            ScriptManager.opened_scene_path = f"{self.project_path}/Source/{self.opened_scene_name}/details.py"
            ScriptManager.create_scn_runner_script(scenes_list = self._receive_project_scenes_dict , SceneName = self.opened_scene_name)
        else :
            easygui.msgbox(title="Field at receive scene source" , msg=f"path '{self.project_path}/Source/{self.opened_scene_name}/details.py' is not exists")
        
    
    
    def __call__(self, *args, **kwds):
        return {
            "Project_path" : self.project_path if self.project_path else 'Note opened any project' ,
            "Project_name" : self.project_name if self.project_name else 'project name has been not set' ,
            "Opened_scene" : self.opened_scene if self.opened_scene else 'Not open any scene' ,
            "Opened_scene_name" : self.opened_scene_name if self.opened_scene_name else 'Opened scene has been not set' ,
            "Assets_path" : self.Assets_path if self.Assets_path else 'Has not been saved' ,
            "scenes_dict_path" : self.scenes_dict_path if self.scenes_dict_path else 'Has not been set'
            }

Browser = FileBrowserOpen()
            