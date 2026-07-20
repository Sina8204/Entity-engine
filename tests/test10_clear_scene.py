# from ursina import *

# app = Ursina()

# # ایجاد چند Entity نمونه
# Entity(model='cube', color=color.orange, position=(1,0,0))
# Entity(model='sphere', color=color.azure, position=(-1,0,0))

# # تابعی برای پاک کردن صحنه با فشردن کلید Space
# def input(key):
#     if key == 'space':
#         scene.clear()  # تمام Entityها را پاک می‌کند
#         print("همه موجودیت‌ها پاک شدند.")

# app.run()

######################################## get file name
# from pathlib import Path
# import easygui

# scene_path = easygui.fileopenbox(
#     title="New project",
#     msg="test"
# )

# if scene_path:
#     filename_without_ext = Path(scene_path).stem
#     print(filename_without_ext)  # مثلاً: "my_file"
######################################## get file name
# import json
# lst = {
#     "__main__": "gun",
#     "player": "/media/sina/New Volume/python projects/Linux/Python/save_testing/test2/Assets/player.json" ,
#     "gun": "/media/sina/New Volume/python projects/Linux/Python/save_testing/test2/Assets/player.json" ,
#     "hat": "/media/sina/New Volume/python projects/Linux/Python/save_testing/test2/Assets/player.json" ,
#     "clothes": "/media/sina/New Volume/python projects/Linux/Python/save_testing/test2/Assets/player.json" ,
#     "camera": "/media/sina/New Volume/python projects/Linux/Python/save_testing/test2/Assets/player.json"
# }

# lst2 = {
#     "__main__": '' ,
#     "player": "/media/sina/New Volume/python projects/Linux/Python/save_testing/test2/Assets/player.json" ,
#     "gun": "/media/sina/New Volume/python projects/Linux/Python/save_testing/test2/Assets/player.json" ,
#     "hat": "/media/sina/New Volume/python projects/Linux/Python/save_testing/test2/Assets/player.json" ,
#     "camera": "/media/sina/New Volume/python projects/Linux/Python/save_testing/test2/Assets/player.json"
# }

# if lst["__main__"]:
#     print("if")
#     if lst["__main__"] in list(lst2.keys()):
#         print("inside if")
#         lst2["__main__"] = lst["__main__"]
#     else :
#         print("inside else")
#         lst2["__main__"] = list(lst2.keys())[1]
# else :
#     print("outside else")
#     lst2["__main__"] = list(lst2.keys())[1]

# print("lst" , end=" ")
# print(json.dumps(lst , ensure_ascii=False , indent=4))
# print("--------------------------------------------")
# print("lst2" , end=" ")
# print(json.dumps(lst2 , ensure_ascii=False , indent=4))

# # entities_list = list(lst.keys())
# # print(entities_list)
# # entities_list.remove("__main__")
# # print(entities_list)

# import os

# folder_path = "/home/user/documents/projects/my_folder"

# # دریافت نام پوشه
# folder_name = os.path.basename(folder_path)
# print(folder_name)  # خروجی: my_folder

Traceback (most recent call last):
  File "/media/sina/New Volume/python projects/Linux/Python/Engine/Menus/1_File/2_Open/1_Open project.py", line 6, in main
    Browser.open_project()
  File "/media/sina/New Volume/python projects/Linux/Python/Engine/Creator_methods/File_browser.py", line 109, in open_project
    self.update_project_scenes_list()
  File "/media/sina/New Volume/python projects/Linux/Python/Engine/Creator_methods/File_browser.py", line 396, in update_project_scenes_list
    scenes_list = self._get_project_scenes()
  File "/media/sina/New Volume/python projects/Linux/Python/Engine/Creator_methods/File_browser.py", line 465, in _get_project_scenes
    items = sorted(os.listdir(check_folder))
FileNotFoundError: [Errno 2] No such file or directory: 'Assets'