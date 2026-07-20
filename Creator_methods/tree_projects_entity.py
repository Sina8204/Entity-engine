def add_entity_to_dict(ent , path):
    return {
        ent.name : {
            "model_path" : path ,
            "color" : tuple(ent.color) ,
            "position" : tuple(ent.position) ,
            "rotation" : tuple(ent.rotation),
            "scale" : tuple(ent.scale),
            "children" : {
                child.name : add_entity_to_dict(child) for child in ent.children
            }
        }
        
    }

def add_child_to_tree(tree, parent_name, child_name, child_data):
    # اگر parent در سطح فعلی پیدا شد
    if parent_name in tree:
        # اگر children وجود ندارد، ایجاد کن
        if "children" not in tree[parent_name]:
            tree[parent_name]["children"] = {}
        # فرزند جدید را اضافه کن
        tree[parent_name]["children"][child_name] = child_data
        return tree
    
    # در غیر این صورت، در childrenهای موجود جستجو کن
    for key, value in tree.items():
        if isinstance(value, dict) and "children" in value:
            # جستجوی بازگشتی در children
            result = add_child_to_tree(value["children"], parent_name, child_name, child_data)
            # اگر پیدا شد و تغییر کرد، درخت را برگردان
            if result is not None:
                return tree
    
    # اگر parent پیدا نشد، درخت بدون تغییر برگردانده می‌شود
    return tree

def rename_key_in_tree(tree, old_key, new_key):
    """تغییر نام یک کلید در درخت به صورت بازگشتی"""
    if old_key in tree:
        tree[new_key] = tree.pop(old_key)
        return True
    
    for key, value in tree.items():
        if isinstance(value, dict) and "children" in value:
            if rename_key_in_tree(value["children"], old_key, new_key):
                return True
    return False

def set_value_in_tree(tree , parent_name , key , value):
    if parent_name in tree:
        tree[parent_name][key] = value
        return tree
    
    for other_key , other_value in tree.items():
        if key in other_value:
            found = add_child_to_tree(other_value[key] , parent_name , value)
            if found:
                return found
    return

# داده‌های تست
data = {
    "cube1": {
        "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
        "color": "Color(0.5, 0.5, 0.5, 1.0)",
        "position": "Vec3(0, 0, 0)",
        "rotation": "Vec3(0, 0, 0)",
        "scale": "Vec3(1, 1, 1)",
        "children": {
            "cube2": {
                "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
                "color": "Color(0.5, 0.5, 0.5, 1.0)",
                "position": "Vec3(0, 0, 0)",
                "rotation": "Vec3(0, 0, 0)",
                "scale": "Vec3(1, 1, 1)",
                "children": {
                    "cube3": {
                        "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
                        "color": "Color(0.5, 0.5, 0.5, 1.0)",
                        "position": "Vec3(0, 0, 0)",
                        "rotation": "Vec3(0, 0, 0)",
                        "scale": "Vec3(1, 1, 1)",
                        "children": {
                            "cube4": {
                                "model_path": "Menus/3_Entity/2_3D entity/1_cube.py",
                                "color": "Color(0.5, 0.5, 0.5, 1.0)",
                                "position": "Vec3(0, 0, 0)",
                                "rotation": "Vec3(0, 0, 0)",
                                "scale": "Vec3(1, 1, 1)",
                                "children": {}
                            }
                        }
                    }
                }
            }
        }
    }
}

lst = ["ali" , "bibi" , "gol" , "hosi"]

def names():
    return True , lst

# names = ["ali" , "hosi" , "bibi"]
# names.remove("ali2")
# print(names)
# rename_key_in_tree(data , 'cube2' , 'new_cube2')
# print(data)