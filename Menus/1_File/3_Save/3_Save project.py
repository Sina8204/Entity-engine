from AppData import ProjectData , status
from Creator_methods import show_message , Browser
import easygui
def main(**kwargs):
    try :
        save_project = Browser.save_project()
        project_data = ''
        for key , value in list(Browser().items()):
            key = key.replace("_", " ")
            project_data += f"{key} : {value}\n"
        
        match (save_project):
            case True:
                easygui.msgbox(title="Save project" , msg=f"Successfully at save scene as :D\nProject data:\n{project_data}")
            case 'cancel':
                easygui.msgbox(title="Save project" , msg=f"Construction of the save project has been canceled.\nProject data:\n{project_data}")
            case False:
                easygui.msgbox(title="Save project" , msg=f"Source path is not exists in the project. So created Source folder in the project \nTry again using a different name or path.\nProject data:\n{project_data}")
            case None:
                easygui.msgbox(title="Save project" , msg=f"Open a project or creat a new project before operation save project.\nProject data:\n{project_data}")
    except Exception as e:
        easygui.exceptionbox(
            title="Field at open project :(" , 
            msg="An unexpected error occurred in 3_Save scene.py"
        )
        print(f"Field at open project : \n\t\t{e}")
    