from Creator_methods import Browser
from AppData import ScriptManager
import os
from easygui import msgbox

def main():
    if ScriptManager.main_path:
        if os.path.exists(ScriptManager.main_path):
            ScriptManager.run_python_file_subprocess(ScriptManager.main_path)
        else :
            msgbox(title="Field at run project" , msg=f"path '{ScriptManager.main_path}' is not exists")
    else:
        msgbox(title="Field at run project" , msg=f"Project path has not been set")