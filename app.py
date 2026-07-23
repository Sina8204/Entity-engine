from ursina import *
import json
#from Creator_methods.Entity_creator import create_entity
#from Creator_methods.panel_contents import create_entity_winPanel
#from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
#from Creator_methods.tree_button import TreeButton , entity_buttons
from Creator_methods.UI_classes import Sort_menus , catch_menus
from AppData import ProjectData
from Creator_methods import Browser
# from AppData import data_manager

app = Ursina()

menu = catch_menus('Menus')
Sort_menus(menu() , menus_x_pos=0.5)

ground = Entity(model='plane', scale=20, texture='white_cube', texture_scale=(20, 20))
ground.y -= 1
# راه‌اندازی دوربین
from Creator_methods.Camera_controller import Active_camera_controller
# data_manager.set_item(child_items = 'test')
#my_entity = Entity(model='camera.glb', position=(0, 0, 0))
def input(key):
    match(key):
        case "q": print(json.dumps(ProjectData.data , ensure_ascii=False , indent=2))
        case "t" : print(ProjectData.data)
        case "b": print(json.dumps(Browser() , ensure_ascii=False , indent=2))
app.run()