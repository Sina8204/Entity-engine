from ursina import *
#from AppData import ProjectData , status
from ursina.prefabs.file_browser import FileBrowser
from ursina.prefabs.file_browser_save import FileBrowserSave , FileButton
from Creator_methods import show_message , Browser
import os , json
import easygui

def main(**kwargs):
    try :
        new_project = Browser.new_project()
        project_data = ''
        for key , value in list(Browser().items()):
            key = key.replace("_", " ")
            project_data += f"{key} : {value}\n"
        
        match(new_project):
            case True :
                easygui.msgbox(title="New project" , msg=f"Successfully at creat new project :D\nProject data:\n{project_data}")
            case False :
                easygui.msgbox(title="New project" , msg=f"UnSuccessfully at creat new project :(\nProject data:\n{project_data}")
            case None :
                easygui.msgbox(title="New project" , msg=f"UnSuccessfully at creat new project :(\nBecause There is a project with name you choose in path you selected , or path you selected is note existes.\nProject data:\n{project_data}")
            case 'cancel' :
                easygui.msgbox(title="New project" , msg=f"Construction of the new project has been canceled.\ndata:\n{project_data}")

    except Exception as e:
        print(f"Field at making new project :( \n\t\t{e}")
        easygui.exceptionbox(title="Field at making new project :(" , msg="An unexpected error occurred in 1_new.py")
        #show_message(win_title="" , message="Check terminal to see errors")