from AppData import ProjectData , status
from Creator_methods import show_message , Browser
import easygui
def main(**keywargs):
    try :
        open_scene = Browser.open_scene()
        project_data = ''
        for key , value in list(Browser().items()):
            key = key.replace("_", " ")
            project_data += f"{key} : {value}\n"
        
        match (open_scene):
            case True:
                easygui.msgbox(title="Open scene" , msg=f"Successfully at open scene :D\nProject data:\n{project_data}")
            case 'cancel' :
                easygui.msgbox(title="Open scene" , msg=f"Construction of the Open project has been canceled.\nProject data:\n{project_data}")
            case None:
                easygui.msgbox(title="Open scene" , msg=f"The scene opening operation was not successful because the selected file does not have the scene format (*{Browser.scene_format}).\nProject data:\n{project_data}")
            case False:
                easygui.msgbox(title="Open scene" , msg=f"Open a project before operation open scene.\nProject data:\n{project_data}")


        print("Trieing run 2_Open scene.py was sucsessfully :)")
    except Exception as e:
        easygui.exceptionbox(
            title="Field at open project :(" , 
            msg="An unexpected error occurred in 2_Open scene.py"
        )
        print(f"Field at open project : \n\t\t{e}")