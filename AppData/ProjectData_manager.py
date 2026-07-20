from Creator_methods.Scene_manager import SceneManager
from Creator_methods.UI_classes import show_message

if __name__ == "__main__":
    from scripts_manager import ScriptManager
else:
    from .scripts_manager import ScriptManager

from easygui import msgbox
from pathlib import Path
import json
import os



class ProjectDataManager:
    def __init__(self , path = 'AppData/project_date.json'):
        self.path = path
        self.source_path = ''
        self.data = {
            "__names__" : []
        }
    
    def add_entity_to_dict(self , ent , **attr):
        self.data.update({
            ent.name : {
                **attr
                # "model_path" : path ,
                # "color" : tuple(ent.color) ,
                # "position" : tuple(ent.position) ,
                # "rotation" : tuple(ent.rotation),
                # "scale" : tuple(ent.scale),
                # "children" : {
                #     child.name : self.add_entity_to_dict(child) for child in ent.children
                # }
            }
        })
        self.data["__names__"].append(ent.name)
        return 
    def add_children(self , parent_name, child_name, child_data):
        self.__add_child_to_tree(self.data , parent_name, child_name, child_data)
        self.data["__names__"].append(child_name)
    
    def rename_key(self , old_key ,  new_key):
        self.__rename_key_in_tree(self.data , old_key , new_key)
        if old_key in self.data["__names__"]:
            self.data["__names__"].remove(old_key)
        self.data["__names__"].append(new_key)
    
    def set_value(self , entity_name , key , new_value):
        self.__update_entity_property(self.data , entity_name , key , new_value)
    
    def set_values(self , entity_name , updates) :
        self.__update_multiple_properties(self.data , entity_name , updates)
    
    def remove_entity (self , entity_name):
        self.__delete_entity_by_name(self.data , entity_name)

    ##############################################
    def __add_child_to_tree(self , tree, parent_name, child_name, child_data):
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
                result = self.__add_child_to_tree(value["children"], parent_name, child_name, child_data)
                # اگر پیدا شد و تغییر کرد، درخت را برگردان
                if result is not None:
                    return tree
        
        # اگر parent پیدا نشد، درخت بدون تغییر برگردانده می‌شود
        return tree
    
    def __rename_key_in_tree(self , tree, old_key, new_key):
        """تغییر نام یک کلید در درخت به صورت بازگشتی"""
        if old_key in tree:
            tree[new_key] = tree.pop(old_key)
            return True
        
        for key, value in tree.items():
            if isinstance(value, dict) and "children" in value:
                if self.__rename_key_in_tree(value["children"], old_key, new_key):
                    return True
        return False
    
    def __update_entity_property(self , data, entity_name, key, new_value):
        """
        ویرایش یک ویژگی خاص از یک entity
        entity_name: نام entity مورد نظر (مثلاً "cube۲")
        key: نام کلید مورد نظر (به جز children)
        """
        def find_and_update(tree, target_name, key, value):
            if target_name in tree:
                if key in tree[target_name] and key != "children":
                    tree[target_name][key] = value
                    print(f"ویژگی '{key}' در '{target_name}' با موفقیت ویرایش شد")
                    return True
                else:
                    print(f"کلید '{key}' در '{target_name}' وجود ندارد یا children است!")
                    return False
            
            # جستجو در children
            for node in tree.values():
                if "children" in node and node["children"]:
                    if find_and_update(node["children"], target_name, key, value):
                        return True
            return False
        
        return find_and_update(data, entity_name, key, new_value)

    def __update_multiple_properties(self , data, entity_name, updates):
        """
        ویرایش چندین ویژگی یک entity
        updates: دیکشنری شامل کلید و مقدار جدید
        """
        def find_and_update(tree, target_name, updates):
            if target_name in tree:
                for key, value in updates.items():
                    if key in tree[target_name] and key != "children":
                        tree[target_name][key] = value
                        print(f"ویژگی '{key}' در '{target_name}' با موفقیت ویرایش شد")
                    else:
                        print(f"کلید '{key}' در '{target_name}' وجود ندارد یا children است!")
                return True
            
            # جستجو در children
            for node in tree.values():
                if "children" in node and node["children"]:
                    if find_and_update(node["children"], target_name, updates):
                        return True
            return False
        
        return find_and_update(data, entity_name, updates)
    
    def __get_all_children_names(self, data, entity_name):
        """
        دریافت نام تمام فرزندان یک entity به صورت بازگشتی
        """
        children_names = []
        
        def recursive_collect(tree, target):
            # بررسی سطح فعلی
            if target in tree:
                # پیدا کردن entity مورد نظر
                entity = tree[target]
                if "children" in entity and entity["children"]:
                    # جمع‌آوری نام فرزندان مستقیم
                    for child_name in entity["children"].keys():
                        children_names.append(child_name)
                        # جمع‌آوری فرزندان فرزندان
                        recursive_collect(entity["children"], child_name)
                return True
            
            # جستجو در children ها
            for key, value in tree.items():
                if isinstance(value, dict) and "children" in value and value["children"]:
                    if recursive_collect(value["children"], target):
                        return True
            return False
        
        recursive_collect(data, entity_name)
        return children_names

    def __find_entity_path(self , data, entity_name, current_path=None):
        """
        پیدا کردن مسیر یک entity
        """
        if current_path is None:
            current_path = []
        
        # بررسی سطح فعلی
        if entity_name in data:
            return current_path + [entity_name]
        
        # جستجو در children ها
        for key, value in data.items():
            if isinstance(value, dict) and "children" in value and value["children"]:
                result = self.__find_entity_path(value["children"], entity_name, current_path + [key, "children"])
                if result:
                    return result
        return None
    
    def __delete_entity_by_name(self, data, entity_name):
        """
        حذف entity با پیدا کردن مسیر آن و برگرداندن نام فرزندان
        """
        # جمع‌آوری نام فرزندان قبل از حذف
        children_names = self.__get_all_children_names(data, entity_name)
        
        # پیدا کردن مسیر
        path = self.__find_entity_path(data, entity_name)
        if not path:
            print(f"entity '{entity_name}' پیدا نشد!")
            return False, []
        
        # حرکت به مسیر پیدا شده
        current = data
        for key in path[:-1]:
            current = current[key]
        
        # حذف entity
        last_key = path[-1]
        if last_key in current:
            del current[last_key]
            print(f"entity '{entity_name}' با موفقیت حذف شد")
            if children_names:
                for name in children_names:
                    if name in self.data["__names__"]:
                        self.data["__names__"].remove(name)
                        print(f"removes {name}")
                print(f"فرزندان حذف شده: {children_names}")
            if entity_name in self.data["__names__"]:
                self.data["__names__"].remove(entity_name)
            return True, children_names
        else:
            print(f"entity '{entity_name}' پیدا نشد!")
            return False, []

    def clear_data(self):
        self.data = {
            "__names__" : []
        }

    def save_data(self):
        print(f"-------------------------- start operation saveing data ------------------------------")
        print(f"Path = {self.path}")
        names = self.data["__names__"].copy()
        self.data["__names__"].clear()
        with open(self.path , 'w' , encoding='utf-8') as file:
            json.dump(self.data , file , ensure_ascii=False , indent=4)
        self.data["__names__"] = names.copy()
        del names
        ############ create source of scene
        if self.source_path:
            if not os.path.exists(self.source_path):
                msgbox(title="Field at creat scene script" , msg = f"{self.source_path} is not exists")
                return False
            ScriptManager.save_path = self.source_path
            scn_name = str(Path(self.path).stem)
            if scn_name.endswith(".scn"):
                scn_name = scn_name.replace(".scn", '')
            ScriptManager.create_scene_script(Scene_Name = scn_name , scene_data = self.data)
            ScriptManager.remove_unavalable_ents_folder(path = f"{self.source_path}/Source/{scn_name}" , avalable_entities = self.data["__names__"])
            return True
        else:
            msgbox(title="Field at creat scene script" , msg = f"self.save_path has not ben set")
            return False


            
    
    def load_scene(self):
        loading_obj = SceneManager()
        loading_obj.load_new_scene(details = self.data)
        # ScriptManager.save_path = status["project_path"]
        # ScriptManager.create_entity_script(SceneName = scene_name , scene_dict = self.data)
        # ScriptManager.create_scene_script(SceneName = scene_name , scene_data = self.data)
        print(self.data)
        print(f"Scene was cleared and loaded new scenc\n{json.dumps(self.data , ensure_ascii=False , indent=4)}")
        
    
    
    def __call__(self, *args, **kwds):
        return json.dumps(self.data , indent=4 , ensure_ascii=False)

ProjectData = ProjectDataManager()

# from ursina import *
# app = Ursina()

# e1 = Entity(model = 'cube' , name = 'e1')
# e2 = Entity(model = 'cube' , name = 'e2')
# e3 = Entity(model = 'cube' , name = 'e3')
# e4 = Entity(model = 'cube' , name = 'e4')
# e5 = Entity(model = 'cube' , name = 'e5')
# ProjectData = ProjectDataManager()
# ProjectData.add_entity_to_dict(e1 , "test")
# ProjectData.add_children("e1" , "e2" , {"color" : tuple(e2.color) , "position" : tuple(e2.position) , "children" : {}})
# ProjectData.add_children("e2" , "e3" , {"color" : tuple(e3.color) , "position" : tuple(e3.position) , "children" : {}})
# ProjectData.add_children("e2" , "e4" , {"color" : tuple(e3.color) , "position" : tuple(e3.position) , "children" : {}})
# ProjectData.add_children("e4" , "e5" , {"color" : tuple(e3.color) , "position" : tuple(e3.position) , "children" : {}})
# print(ProjectData())
# print("-----------------------------")
# ProjectData.rename_key("e4" , "new_e4")
# ProjectData.rename_key("e1" , "new_e1")
# ProjectData.rename_key("e3" , "new_e3")
# # ProjectData.set_value("e2" , "position" , (0.1 , 0.5 , 0.3))
# # ProjectData.set_values("e3" , {
# #     "color" : tuple(Vec3(0.1 , 0.1 , 0.1)) ,
# #     "position" : tuple(Vec3(0.2 , 0.2 , 0.2))
# # })
# print(ProjectData())
# print("-----------------------------")
# ProjectData.remove_entity("new_e3")
# ProjectData.remove_entity("e1")
# print(ProjectData())
# app.run()
