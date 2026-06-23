from ursina import *
from ursina.prefabs.file_browser import FileBrowser

def on_submit(paths):
    print("Project opened")
    print(paths[0])

def main():
    open_project = FileBrowser(file_types=('details.json') , enabled=False)
    open_project.on_submit = on_submit
    open_project.enabled = True