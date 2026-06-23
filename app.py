from ursina import *
from Camera_controller import CameraController
from Creator_methods.Entity_creator import create_entity
#from Creator_methods.panel_contents import create_entity_winPanel
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from Creator_methods.UI_classes import Sort_menus , catch_menus
from AppData import data_manager
app = Ursina()


menu = catch_menus('Menus')
Sort_menus(menu())

ground = Entity(model='plane', scale=20, texture='white_cube', texture_scale=(20, 20))
ground.y -= 1
# راه‌اندازی دوربین
Active_camera_controller = CameraController()
data_manager.set_item(child_items = 'test')
app.run()