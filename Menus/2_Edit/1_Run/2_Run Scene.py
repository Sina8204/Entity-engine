from Creator_methods import Browser
from AppData import ScriptManager , ProjectData
import os
from easygui import msgbox

#ScriptManager.run_python_file_subprocess(ScriptManager.opened_scene_path)

def main():
    if ScriptManager.opened_scene_path:
        if Browser.opened_scene_name:
            if os.path.exists(ScriptManager.opened_scene_path):
                if os.path.exists(f"{ScriptManager.save_path}/Source/__ScnRunner/run.py"):
                    if os.path.exists(f"{ScriptManager.save_path}/Source/scn.py"):
                        ScriptManager.run_python_file_subprocess(f"{ScriptManager.save_path}/Source/scn.py")
                    else:
                        msgbox(title="scn.py not found" , msg = f"path '{ScriptManager.save_path}/Source/scn.py' is not exists")
                        #print(f"Run from scene path : \n\t'{ScriptManager.opened_scene_path}'")
                else:
                    msgbox(title="scn -> run.py not found" , msg = f"path '{ScriptManager.save_path}/Source/__ScnRunner/run.py' is not exists")
            else:
                msgbox(title="Opened scene path not found" , msg = f"path '{ScriptManager.opened_scene_path}' is not exists")
        else:
            msgbox(title="Field at run project" , msg=f"Project Opened scene name has not been set")
            print(f"Run from scene path : \n\t'{ScriptManager.opened_scene_path}' is not exists")
    else :
        msgbox(title="Field at run project" , msg=f"Project path has not been set")
# else:
#     msgbox(title="Field at run project" , msg=f"Project path has not been set")