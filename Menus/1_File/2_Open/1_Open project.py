from AppData import ProjectData , status
from Creator_methods import show_message , Browser
import easygui
def main(**keywargs):
    try :
        open_project = Browser.open_project()
        project_data = ''
        for key , value in list(Browser().items()):
            key = key.replace("_", " ")
            project_data += f"{key} : {value}\n"
        
        match (open_project):
            case True :
                easygui.msgbox(title="Open project" , msg=f"Successfully at open project :D\nProject data:\n{project_data}")
            case 'cancel':
                easygui.msgbox(title="Open project" , msg=f"Construction of the Open project has been canceled.\nProject data:\n{project_data}")
            case None:
                easygui.msgbox(title="Open project" , msg=f"The open project operation was not successful because the selected path is not the correct project path.\nProject data:\n{project_data}")
        print("Trieing run 2_Open project.py was sucsessfully :)")
    except Exception as e:
        easygui.exceptionbox(
            title="Field at open project :(" , 
            msg="An unexpected error occurred in 2_Open project.py"
        )
        print(f"Field at open project : \n\t\t{e}")