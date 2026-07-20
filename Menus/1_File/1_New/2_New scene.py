from Creator_methods import show_message , Browser
import easygui

def main(**kwargs):
    try :
        new_scene = Browser.new_scene()
        project_data = ''
        for key , value in list(Browser().items()):
            key = key.replace("_", " ")
            project_data += f"{key} : {value}\n"
        match (new_scene):
            case True :
                easygui.msgbox(title="New scene" , msg=f"Successfully at creat new new scene :D\nProject data:\n{project_data}")
            case False:
                easygui.msgbox(title="New scene" , msg=f"Unsuccessfully at creat new scene :(\nProject data:\n{project_data}")
            case 'cancel' :
                easygui.msgbox(title="New scene" , msg=f"Construction of the new project has been canceled.\nProject data:\n{project_data}")
            case None:
                easygui.msgbox(title="New scene" , msg=f"Unsuccessfully at creat new scene. Because no project has been opened.\nProject data:\n{project_data}")

    except Exception as e:
        print(f"Field at making new project :( \n\t\t{e}")
        easygui.exceptionbox(title="Field at making new project :(" , msg="An unexpected error occurred in 1_new.py")
        #show_message(win_title="" , message="Check terminal to see errors")