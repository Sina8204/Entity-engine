from AppData import ProjectData , status
from Creator_methods import show_message , Browser
import easygui
def main(**kwargs):
    try :
        save_scene = Browser.save_scene()
        project_data = ''
        for key , value in list(Browser().items()):
            key = key.replace("_", " ")
            project_data += f"{key} : {value}\n"
        
        match (save_scene):
            case True:
                easygui.msgbox(title="Save scene" , msg=f"Successfully at save scene :D\nProject data:\n{project_data}")
            case 'cancel':
                easygui.msgbox(title="Save scene" , msg=f"Construction of the save scene has been canceled.\nProject data:\n{project_data}")
            case False:
                easygui.msgbox(title="Save scene" , msg=f"Open a scene or creat a new scene before operation save scene.\nProject data:\n{project_data}")
            case None:
                easygui.msgbox(title="Save scene" , msg=f"Open a project or creat a new project before operation save scene.\nProject data:\n{project_data}")
            
        print("Trieing run 3_Save scene.py was sucsessfully :)")
    except Exception as e:
        easygui.exceptionbox(
            title="Field at open project :(" , 
            msg="An unexpected error occurred in 3_Save scene.py"
        )
        print(f"Field at open project : \n\t\t{e}")
    