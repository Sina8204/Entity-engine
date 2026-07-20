# from ursina import *
# from Creator_methods.UI_classes import execute_file_module
# project_objects = {
#     "test" : {
#         "model_path" : "Menus/3_Entity/2_3D entity/1_cube.py" ,
#         "color" : color.gray ,
#         "position" : (1 , 2 , 3) ,
#         "rotation" : (30 , 45 , 90) ,
#         "scale" : (0.5 , 0.5 , 0.5) ,
#         "child" : {
#             "test2" : {
#                 "model_path" : "Menus/3_Entity/2_3D entity/1_cube.py" ,
#                 "color" : color.gray ,
#                 "position" : (3 , 2 , 1) ,
#                 "rotation" : (90 , 0 , 40) ,
#                 "scale" : (0.5 , 0.5 , 0.5) ,
#                 "child" : {

#         }
#             } ,
#         "test3" : {
#                 "model_path" : "Menus/3_Entity/2_3D entity/1_cube.py" ,
#                 "color" : color.gray ,
#                 "position" : (3 , 2 , 1) ,
#                 "rotation" : (90 , 0 , 40) ,
#                 "scale" : (0.5 , 0.5 , 0.5) ,
#                 "child" : {

#         }
#     }

#         }
#     }
# }

# class load_project:
#     def __init__(self , items : dict , parent = None):
#         #print(items.keys())
#         self.items = items
#         self.objects_path = items.keys()
#         self.parent = parent
#         for obj in self.objects_path:
#             e = execute_file_module(
#                 file_path = self.items[obj]["model_path"] , 
#                 parent = self.parent ,
#                 name = obj ,
#                 position = self.items[obj]["position"] ,
#                 rotation = self.items[obj]["rotation"] ,
#                 scale = self.items[obj]["scale"] ,
#                 color = self.items[obj]["color"]
#                 )
#             #print(f'Entiti type ==> {type(e)}')
#             #
#             childeren_dict = self.items[obj]["child"]
#             #print(f'====> {childeren_dict}')
#             if len(childeren_dict.keys()) > 0:
#                 load_project(items = childeren_dict , parent = e)

# app = Ursina()

# load_project(items=project_objects)
#################################################################################
# data = {
#     "cube": {
#         "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
#         "color": "Color(0.5, 0.5, 0.5, 1.0)",
#         "position": "Vec3(0, 0, 0)",
#         "rotation": "Vec3(0, 0, 0)",
#         "scale": "Vec3(1, 1, 1)",
#         "child": {
#             "cube": {
#                 "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
#                 "color": "Color(0.5, 0.5, 0.5, 1.0)",
#                 "position": "Vec3(0, 0, 0)",
#                 "rotation": "Vec3(0, 0, 0)",
#                 "scale": "Vec3(1, 1, 1)",
#                 "child": {
#                     "cube": {
#                         "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
#                         "color": "Color(0.5, 0.5, 0.5, 1.0)",
#                         "position": "Vec3(0, 0, 0)",
#                         "rotation": "Vec3(0, 0, 0)",
#                         "scale": "Vec3(1, 1, 1)",
#                         "child": {}
#                     }
#                 }
#             }
#         }
#     }
# }
# # آرایه کلیدها
# keys = ["cube", "cube", "cube"]

# # روش ۱: دسترسی به child آخرین ایندکس
# current = data

# print(current.items())

# #app.run()

d = {
    "__names__": [
        "cube",
        "cube1",
        "cube12",
        "cube123"
    ],
    "cube": {
        "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
        "color": [
            0.5,
            0.5,
            0.5,
            1.0
        ],
        "position": [
            0.0,
            0.0,
            0.0
        ],
        "rotation": [
            -0.0,
            -0.0,
            0.0
        ],
        "scale": [
            1.0,
            1.0,
            1.0
        ],
        "children": {
            "cube1": {
                "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
                "color": [
                    0.5,
                    0.5,
                    0.5,
                    1.0
                ],
                "position": [
                    0.0,
                    0.0,
                    0.0
                ],
                "rotation": [
                    -0.0,
                    -0.0,
                    0.0
                ],
                "scale": [
                    1.0,
                    1.0,
                    1.0
                ],
                "children": {}
            }
        }
    },
    "cube12": {
        "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
        "color": [
            0.5,
            0.5,
            0.5,
            1.0
        ],
        "position": [
            0.0,
            0.0,
            0.0
        ],
        "rotation": [
            -0.0,
            -0.0,
            0.0
        ],
        "scale": [
            1.0,
            1.0,
            1.0
        ],
        "children": {}
    },
    "cube123": {
        "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
        "color": [
            0.5,
            0.5,
            0.5,
            1.0
        ],
        "position": [
            0.0,
            0.0,
            0.0
        ],
        "rotation": [
            -0.0,
            -0.0,
            0.0
        ],
        "scale": [
            1.0,
            1.0,
            1.0
        ],
        "children": {}
    }
}

from ursina import *

app = Ursina()

e1 = Entity(model = "cube")
e2 = Entity(model = "cube" , parent = e1 , color = color.red)

e1.rotation = (0 , 45 , 0)
e2.world_x += 2
# e3 = Entity(model = "cube" , parent = e1 , name = 'o2')
# e4 = Entity(model = "cube" , parent = e1 , name = 'o3')

# entities = [e for e in e1.children if "_" in e.name]
# print(entities)

app.run()
