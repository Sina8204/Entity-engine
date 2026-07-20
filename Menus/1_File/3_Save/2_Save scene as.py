from AppData import ProjectData , status
from Creator_methods import show_message , Browser
import easygui
def main(**kwargs):
    try :
        save_scene_as = Browser.save_scene_as()
        project_data = ''
        for key , value in list(Browser().items()):
            key = key.replace("_", " ")
            project_data += f"{key} : {value}\n"
        
        match (save_scene_as):
            case True:
                easygui.msgbox(title="Save scene as" , msg=f"Successfully at save scene as :D\nProject data:\n{project_data}")
            case 'cancel':
                easygui.msgbox(title="Save scene as" , msg=f"Construction of the save scene as has been canceled.\nProject data:\n{project_data}")
            case False:
                easygui.msgbox(title="Save scene as" , msg=f"A scene with the name you selected exists in the selected path. \nTry again using a different name or path.\nProject data:\n{project_data}")
            case None:
                easygui.msgbox(title="Save scene" , msg=f"Open a project or creat a new project before operation save scene as.\nProject data:\n{project_data}")
        
        print("Trieing run 4_Save scene as.py was sucsessfully :)")
    except Exception as e:
        easygui.exceptionbox(
            title="Field at open project :(" , 
            msg="An unexpected error occurred in 4_Save scene as.py"
        )
        print(f"Field at open project : \n\t\t{e}")
    