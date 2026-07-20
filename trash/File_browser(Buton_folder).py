# from ursina import *
# from AppData import ProjectData , status
# from ursina.prefabs.file_browser import FileBrowser
# from ursina.prefabs.file_browser_save import FileBrowserSave , FileButton
# from Creator_methods.Scene_manager import SceneManager
# from Creator_methods import show_message
# import os , json

# class FileButtonSave(FileButton):
#     def on_click(self):
#         if len([e for e in self.parent.children if e.selected]) >= self.load_menu.selection_limit and not self.selected:
#             for e in self.parent.children:  # clear selection
#                 e.selected = False

#         self.selected = True
#         self.load_menu.file_name_field.text = str(self.path.name)


#     def on_double_click(self):
#         if self.path.is_dir():
#             self.load_menu.path = self.path
#         else:
#             self.selected = True
#             self.load_menu.open()


# @generate_properties_for_class()
# class FileBrowserOpen(FileBrowser):
#     def __init__(self, **kwargs):
#         super().__init__(file_button_class=FileButtonSave)
#         self.browser_open_mode = kwargs["mode"]

#         self.save_button = self.open_button
#         self.save_button.color = color.azure
#         self.save_button.text = 'Select this path'
#         match (self.browser_open_mode):
#             case "new" : self.save_button.on_click = self._new
#             case "open" : self.save_button.on_click = self._open
#             case "save" : self.save_button.on_click = self._save
#             case _ : self.save_button.on_click = lambda : print(f"{self.browser_open_mode} is not created")
        
#         self.file_name_field = InputField(parent=self, scale_x=.75, scale_y=self.save_button.scale_y, y=self.save_button.y)
#         self.save_button.y -= .075
#         self.cancel_button.y -= .075
#         self.file_name_field.text_field.text = ''
#         self.project_name = ''
#         self.project_path = ''
#         self.file_type = '' # to save as
#         self.show_error = None

#         self.last_saved_file = None     # gets set when you save a file
#         self.overwrite_prompt = WindowPanel(
#             content=(
#                 Text('Overwrite?'),
#                 Button('Yes', color=color.azure, on_click=self._save),
#                 Button('Cancel')
#             ), z=-1, popup=True, enabled=False)

#         for key, value in kwargs.items():
#             setattr(self, key ,value)


#     def file_type_setter(self, value):
#         self._file_type = value
#         self.file_types = (value, )


#     def on_enable(self):
#         super().on_enable()
#         self.file_name_field.active = True

#     def on_disable(self):
#         self.file_name_field.active = False

#     def _new(self):
#         scene_clear = SceneManager()
#         scene_clear.clear_scene()
        
#         file_name = self.file_name_field.text_field.text.strip()
#         self.project_name = file_name
        
#         if not file_name:
#             self.show_error = show_message(
#                 win_title='Field to make project',
#                 message='Select a name for your project'
#             )
#             return

#         path = self.path / file_name
        
#         # بررسی وجود overwrite_prompt قبل از استفاده
#         if path.exists() and hasattr(self, 'overwrite_prompt'):
#             try:
#                 # ابتدا مطمئن شوید که موجودیت معتبر است
#                 if self.overwrite_prompt and not self.overwrite_prompt.is_empty():
#                     self.overwrite_prompt.enabled = True
#                 else:
#                     # اگر موجودیت نامعتبر است، دوباره ایجاد کنید
#                     self.create_overwrite_prompt()  # متد ساخت prompt
#             except Exception as e:
#                 print(f"Error setting overwrite prompt: {e}")
#                 # در صورت خطا، prompt را دوباره بسازید
#                 self.create_overwrite_prompt()
        
#         self.project_path = path
        
#         # ادامه کد...
#         json_path = self.create_project(path=self.project_path, name=self.project_name)
#         if json_path:
#             status["is_saved"] = True
#             status["project_path"] = f"{self.project_path}/{self.project_name}.json"
#             ProjectData.clear_data()
#             ProjectData.path = status["project_path"]
#             ProjectData.save_data()
#             print(f"Project path ==> {json_path}")
#         else:
#             return
        
#         self.last_saved_file = path
        
#         # ایمن‌سازی تنظیم enabled = False
#         if hasattr(self, 'overwrite_prompt') and self.overwrite_prompt:
#             try:
#                 if not self.overwrite_prompt.is_empty():
#                     self.overwrite_prompt.enabled = False
#             except:
#                 pass  # اگر خطا رخ داد، نادیده بگیرید
        
#         self.close()
#         self.on_submit(path)
        

#     def _open(self):
#         scene_clear = SceneManager()
#         scene_clear.clear_scene()
#         ProjectData.data.clear()
        
#         file_name = self.file_name_field.text_field.text.strip()
#         self.project_name = file_name

#         path = self.path / file_name
        
#         # بررسی وجود overwrite_prompt قبل از استفاده
#         if path.exists() and hasattr(self, 'overwrite_prompt'):
#             try:
#                 # ابتدا مطمئن شوید که موجودیت معتبر است
#                 if self.overwrite_prompt and not self.overwrite_prompt.is_empty():
#                     self.overwrite_prompt.enabled = True
#                 else:
#                     # اگر موجودیت نامعتبر است، دوباره ایجاد کنید
#                     self.create_overwrite_prompt()  # متد ساخت prompt
#                     if self.overwrite_prompt:
#                         self.overwrite_prompt.enabled = True
#             except Exception as e:
#                 print(f"Error setting overwrite prompt in _open: {e}")
#                 # در صورت خطا، prompt را دوباره بسازید
#                 self.create_overwrite_prompt()
        
#         self.project_path = path
        
#         ############ insert Project data to details_project ############
#         status["is_saved"] = True
#         status["project_path"] = self.project_path
#         ProjectData.path = status["project_path"]
#         print(f"Project path ==> {ProjectData.path}\n--------------------------")
        
#         try:
#             with open(ProjectData.path, 'r', encoding='utf-8') as file:
#                 ProjectData.data = json.load(file)
#             ProjectData.load_scene()
#         except Exception as e:
#             print(f"Error loading project: {e}")
#             self.show_error = show_message(
#                 win_title='Error Loading Project',
#                 message=f'Could not load project: {e}'
#             )
#             return
        
#         ############ insert Project data to details_project ############
#         self.last_saved_file = path
        
#         # ایمن‌سازی تنظیم enabled = False
#         if hasattr(self, 'overwrite_prompt') and self.overwrite_prompt:
#             try:
#                 if not self.overwrite_prompt.is_empty():
#                     self.overwrite_prompt.enabled = False
#             except Exception as e:
#                 print(f"Error disabling overwrite_prompt: {e}")
#                 # اگر موجودیت نامعتبر است، نادیده بگیرید
        
#         self.close()
#         self.on_submit(path)

#     def _save(self):
#         file_name = self.file_name_field.text_field.text.strip()
#         self.project_name = file_name
        
#         if not file_name:
#             self.show_error = show_message(
#                 win_title='Field to make project',
#                 message='Select a name for your project'
#             )
#             return

#         path = self.path / file_name
        
#         # بررسی وجود overwrite_prompt قبل از استفاده
#         if path.exists() and hasattr(self, 'overwrite_prompt'):
#             try:
#                 # ابتدا مطمئن شوید که موجودیت معتبر است
#                 if self.overwrite_prompt and not self.overwrite_prompt.is_empty():
#                     self.overwrite_prompt.enabled = True
#                 else:
#                     # اگر موجودیت نامعتبر است، دوباره ایجاد کنید
#                     self.create_overwrite_prompt()  # متد ساخت prompt
#                     if self.overwrite_prompt:
#                         self.overwrite_prompt.enabled = True
#             except Exception as e:
#                 print(f"Error setting overwrite prompt in _save: {e}")
#                 # در صورت خطا، prompt را دوباره بسازید
#                 self.create_overwrite_prompt()
        
#         self.project_path = path
        
#         try:
#             json_path = self.create_project(self.project_path, self.project_name)
            
#             ############ insert Project data to details_project ############
#             status["is_saved"] = True
#             status["project_path"] = json_path
#             ProjectData.path = status["project_path"]
#             ProjectData.save_data()
#             ############ insert Project data to details_project ############
            
#         except Exception as e:
#             print(f"Error saving project: {e}")
#             self.show_error = show_message(
#                 win_title='Error Saving Project',
#                 message=f'Could not save project: {e}'
#             )
#             return
        
#         self.last_saved_file = path
        
#         # ایمن‌سازی تنظیم enabled = False
#         if hasattr(self, 'overwrite_prompt') and self.overwrite_prompt:
#             try:
#                 if not self.overwrite_prompt.is_empty():
#                     self.overwrite_prompt.enabled = False
#             except Exception as e:
#                 print(f"Error disabling overwrite_prompt: {e}")
#                 # اگر موجودیت نامعتبر است، نادیده بگیرید
        
#         self.close()
#         self.on_submit(path)

#     def on_submit(self, path):  # implement .on_submit to handle saving
#         print('save to path:', path, 'please implement .on_submit to handle saving')
    
#     def create_project(self , path , name = ''):
#         try:
#             os.mkdir(path)
#             json_path = f"{path}/{name}.json"
#             with open(json_path , 'w+' , encoding='utf-8') as file:
#                 json.dump({} , file , indent=2 , ensure_ascii=False)
#             print(f"Sucessfully at create folder '{path}'")
#             return json_path
#         except FileExistsError:
#             print(f"Field at create folder '{path}'")
#             self.show_error = show_message(win_title = 'Field at create folder' , message = 'There is a folder with name you entered')
#             return
#         except Exception as e:
#             print(f"Error at create folder : {e}")
#             self.show_error = show_message(win_title = 'Field at create folder' , message = 'See the terminal to read the error')
#             return

#     def close(self):
#         """Override close method to also close error panel"""
#         # بستن پنل خطا اگر وجود داشته باشد
#         if hasattr(self, 'show_error') and self.show_error is not None:
#             try:
#                 destroy(self.show_error)
#                 self.show_error = None
#             except:
#                 pass  # اگر پنل قبلاً بسته شده باشد
        
#         # فراخوانی متد close کلاس والد
#         super().close()
    
#     def create_overwrite_prompt(self):
#         """ایجاد یا بازسازی prompt برای تایید بازنویسی فایل"""
#         try:
#             # اگر قبلاً وجود دارد و معتبر است، حذف کنید
#             if hasattr(self, 'overwrite_prompt') and self.overwrite_prompt:
#                 try:
#                     if not self.overwrite_prompt.is_empty():
#                         self.overwrite_prompt.destroy()
#                 except:
#                     pass
            
#             # ایجاد prompt جدید
#             # این بخش باید بر اساس ساختار UI شما پیاده‌سازی شود
#             # مثال:
#             from ursina import Text, Entity
            
#             self.overwrite_prompt = Entity(
#                 model='quad',
#                 color=color.rgba(0, 0, 0, 0.8),
#                 scale=(0.6, 0.3),
#                 position=(0, 0, -1),
#                 enabled=False
#             )
            
#             # اضافه کردن دکمه‌های Yes/No
#             # ... کد مربوط به دکمه‌ها ...
            
#             return self.overwrite_prompt
            
#         except Exception as e:
#             print(f"Error creating overwrite prompt: {e}")
#             return None
        
#     def __call__(self, *args, **kwargs):
#         return {
#             "path" : self.project_path ,
#             "name" : self.project_name
#         }

########################################################################################3

from ursina import *
from AppData import ProjectData , status
from ursina.prefabs.file_browser import FileBrowser
from ursina.prefabs.file_browser_save import FileBrowserSave , FileButton
from Creator_methods.Scene_manager import SceneManager
from Creator_methods import show_message
import os , json

class FileButtonSave(FileButton):
    def on_click(self):
        if len([e for e in self.parent.children if e.selected]) >= self.load_menu.selection_limit and not self.selected:
            for e in self.parent.children:  # clear selection
                e.selected = False

        self.selected = True
        self.load_menu.file_name_field.text = str(self.path.name)

    def on_double_click(self):
        if self.path.is_dir():
            self.load_menu.path = self.path
        else:
            self.selected = True
            self.load_menu.open()

@generate_properties_for_class()
class FileBrowserOpen(FileBrowser):
    def __init__(self, **kwargs):
        super().__init__(file_button_class=FileButtonSave)
        self.browser_open_mode = kwargs["mode"]
        
        self.save_button = self.open_button
        self.save_button.color = color.azure
        self.save_button.text = 'Select this path'
        match (self.browser_open_mode):
            case "new" : 
                self.save_button.on_click = self._new
                self.title_bar.text = "Go to your path and enter a name for your project"
            case "open" : 
                self.save_button.on_click = self._open
                self.title_bar.text = "Select *.json project file to open that"
            case "save" : 
                self.save_button.on_click = self._save
                self.title_bar.text = "Save path: Go to your path and enter a name for your project"
            case _ : self.save_button.on_click = lambda : print(f"{self.browser_open_mode} is not created")
        
        self.file_name_field = InputField(parent=self, scale_x=.75, scale_y=self.save_button.scale_y, y=self.save_button.y)
        self.save_button.y -= .075
        self.cancel_button.y -= .075
        self.file_name_field.text_field.text = ''
        self.project_name = ''
        self.project_path = ''
        self.file_type = '' # to save as
        self.show_error = None

        self.last_saved_file = None     # gets set when you save a file

        self._created_entities = []
        self.overwrite_prompt = WindowPanel(
            content=(
                Text('Overwrite?'),
                Button('Yes', color=color.azure),
                Button('Cancel')
            ), z=-1, popup=True, enabled=False)
        match (self.browser_open_mode):
            case "new" : 
                self.overwrite_prompt = WindowPanel(
                    content=(
                        Text("The path you selected is already exists.\nPlease select an empty path with\n diffrent name"),
                        Button('Ok', color=color.azure , on_click = self.hide_overwrite_promt)
                    ), z=-1, popup=True, enabled=False)
            case "open" : 
                self.overwrite_prompt = WindowPanel(
                    content=(
                        Text("The path you selected is not exists.\nPlease select an exists path"),
                        Button('Ok', color=color.azure , on_click = self.hide_overwrite_promt)
                    ), z=-1, popup=True, enabled=False)
            case "save" : 
                self.overwrite_prompt = WindowPanel(
                    content=(
                        Text("The path you selected is already exists.\nThat file might have important details.\nPlease create project with diffrent name"),
                        Button('Ok', color=color.azure , on_click = self.hide_overwrite_promt)
                    ), z=-1, popup=True, enabled=False)
        self._created_entities.append(self.overwrite_prompt)

        for key, value in kwargs.items():
            setattr(self, key ,value)

    def file_type_setter(self, value):
        self._file_type = value
        self.file_types = (value, )

    def on_enable(self):
        super().on_enable()
        self.file_name_field.active = True

    def on_disable(self):
        self.file_name_field.active = False

    def hide_overwrite_promt(self):
        if hasattr(self, 'overwrite_prompt'):
            self.overwrite_prompt.enabled = None
    def _new(self):
        scene_clear = SceneManager()
        scene_clear.clear_scene()
        
        file_name = self.file_name_field.text_field.text.strip()
        self.project_name = file_name
        
        if not file_name:
            self.show_error = show_message(
                win_title='Field to make project',
                message='Select a name for your project'
            )
            self._created_entities.append(self.show_error)  # ✅ اضافه شد
            return

        path = self.path / file_name
        if path.exists() and hasattr(self, 'overwrite_prompt'):
            try:
                if self.overwrite_prompt and not self.overwrite_prompt.is_empty():
                    self.overwrite_prompt.enabled = True
                    return
                else:
                    self.create_overwrite_prompt()
            except Exception as e:
                print(f"Error setting overwrite prompt: {e}")
                self.create_overwrite_prompt()
        
        self.project_path = path
        
        json_path = self.create_project(path=self.project_path, name=self.project_name)
        if json_path:
            status["is_saved"] = True
            status["project_path"] = f"{self.project_path}/{self.project_name}.json"
            ProjectData.clear_data()
            ProjectData.path = status["project_path"]
            ProjectData.save_data()
            print(f"Sucssfully at creat new project :\n\t Project path : '{json_path}'")
        else:
            self.show_error = show_message(win_title="Field at creat new project" , message="The path you selected is not exist\nsee the terminal")
            print(f"Error : \n\tpath '{json_path}' is not exist")
        self.last_saved_file = path
        
        if hasattr(self, 'overwrite_prompt') and self.overwrite_prompt:
            try:
                if not self.overwrite_prompt.is_empty():
                    self.overwrite_prompt.enabled = False
            except:
                pass
        
        self.close()
        #self.on_submit(path)

    def _open(self):
        scene_clear = SceneManager()
        scene_clear.clear_scene()
        # ProjectData.data.clear()
        
        file_name = self.file_name_field.text_field.text.strip()
        self.project_name = file_name

        path = self.path / file_name
        
        if not path.exists() and hasattr(self, 'overwrite_prompt'):
            try:
                if self.overwrite_prompt and not self.overwrite_prompt.is_empty():
                    self.overwrite_prompt.enabled = True
                else:
                    self.create_overwrite_prompt()
                    if self.overwrite_prompt:
                        self.overwrite_prompt.enabled = True
                return
            except Exception as e:
                print(f"Error setting overwrite prompt in _open: {e}")
                self.create_overwrite_prompt()
        
        self.project_path = path
        
        status["is_saved"] = True
        status["project_path"] = self.project_path
        ProjectData.path = status["project_path"]
        print(f"Project path ==> {ProjectData.path}\n--------------------------")
        
        try:
            if not os.path.isdir(ProjectData.path):
                with open(ProjectData.path, 'r', encoding='utf-8') as file:
                    with open("AppData/last_data.json", 'w', encoding='utf-8') as current_file:
                        json.dump(ProjectData.data , current_file , ensure_ascii=False , indent=4)
                    ProjectData.data = json.load(file)
                ProjectData.load_scene()
                if hasattr(self, 'overwrite_prompt') and self.overwrite_prompt:
                    try:
                        if not self.overwrite_prompt.is_empty():
                            self.overwrite_prompt.enabled = False
                    except Exception as e:
                        print(f"Error disabling overwrite_prompt: {e}")
                self.close()
                #self.on_submit(path)
            else :
                try:
                    if self.overwrite_prompt and not self.overwrite_prompt.is_empty():
                        self.overwrite_prompt.content[0].text = "The path you selected is a directory.\nPlease select an true json file \nthat have true details."
                        self.overwrite_prompt.enabled = True
                    else:
                        self.create_overwrite_prompt()
                        if self.overwrite_prompt:
                            self.overwrite_prompt.enabled = True
                except Exception as e:
                    print(f"Error setting overwrite prompt in _open: {e}")
                    self.create_overwrite_prompt()
            return
        #except IsADirectoryError as e:   
        except Exception as e:
            with open("AppData/last_data.json", 'r', encoding='utf-8') as current_file:
                ProjectData.data = json.load(current_file)
            print(f"Error loading project: {e}")
            self.show_error = show_message(
                win_title='Error Loading Project',
                message=f'Could not load project: {e}'
            )
            self._created_entities.append(self.show_error)  # ✅ اضافه شد
        
        self.last_saved_file = path

    def _save(self):
        file_name = self.file_name_field.text_field.text.strip()
        self.project_name = file_name
        
        if not file_name:
            self.show_error = show_message(
                win_title='Field to make project',
                message='Select a name for your project'
            )
            self._created_entities.append(self.show_error)  # ✅ اضافه شد
            return

        path = self.path / file_name
        
        if path.exists() and hasattr(self, 'overwrite_prompt'):
            try:
                if self.overwrite_prompt and not self.overwrite_prompt.is_empty():
                    self.overwrite_prompt.enabled = True
                else:
                    self.create_overwrite_prompt()
                    if self.overwrite_prompt:
                        self.overwrite_prompt.enabled = True
                return
            except Exception as e:
                print(f"Error setting overwrite prompt in _save: {e}")
                self.create_overwrite_prompt()
        self.project_path = path
        
        try:
            json_path = self.create_project(self.project_path, self.project_name)
            
            status["is_saved"] = True
            status["project_path"] = json_path
            ProjectData.path = status["project_path"]
            ProjectData.save_data()
            if hasattr(self, 'overwrite_prompt') and self.overwrite_prompt:
                try:
                    if not self.overwrite_prompt.is_empty():
                        self.overwrite_prompt.enabled = False
                except Exception as e:
                    print(f"Error disabling overwrite_prompt: {e}")
            self.close()
        except Exception as e:
            print(f"Error saving project: {e}")
            self.show_error = show_message(
                win_title='Error Saving Project',
                message=f'Could not save project: {e}'
            )
            self._created_entities.append(self.show_error)  # ✅ اضافه شد
            return
        
        self.last_saved_file = path
        
        #self.on_submit(path)

    def on_submit(self, path):
        try :
            match (self.browser_open_mode):
                case "new" : self._new()
                case "open" : self._open()
                case "save" : 
                    self._save()
                    print("____________________________ i entered on_submit _____________________________")
                case "_" : print('save to path:', path, 'please implement .on_submit to handle saving')
        except Exception as e:
            print('save to path:', path, 'please implement .on_submit to handle saving')
            print(f"Error :\n\t{e}")
        
    
    def create_project(self, path, name=''):
        try:
            os.mkdir(path)
            json_path = f"{path}/{name}.json"
            with open(json_path, 'w+', encoding='utf-8') as file:
                json.dump({}, file, indent=2, ensure_ascii=False)
            print(f"Successfully created folder '{path}'")
            return json_path
        except FileExistsError:
            print(f"Failed to create folder '{path}'")
            self.show_error = show_message(
                win_title='Failed to create folder',
                message='There is a folder with the name you entered'
            )
            self._created_entities.append(self.show_error)
            return
        except Exception as e:
            print(f"Error creating folder: {e}")
            self.show_error = show_message(
                win_title='Failed to create folder',
                message='See the terminal to read the error'
            )
            self._created_entities.append(self.show_error)  # ✅ اضافه شد
            return
    
    def _destroy_entity_safe(self, entity):
        """Safe destroy method with proper None checking"""
        try:
            # ✅ بررسی کامل‌تر
            if entity is None:
                return
            
            # ✅ بررسی اینکه entity هنوز وجود دارد و active است
            if hasattr(entity, 'active') and entity.active is not None:
                # فقط اگر active وجود داشت و boolean بود
                if isinstance(entity.active, bool):
                    entity.active = False
            
            # ✅ destroy کردن با try-except
            try:
                destroy(entity)
            except Exception as e:
                print(f"Error destroying entity: {e}")
                
        except Exception as e:
            print(f"Error in _destroy_entity_safe: {e}")
    
    def close(self):
        """Override close method to properly destroy all entities"""
        try:
            # ✅ گام ۱: غیرفعال کردن entityهای خودمان
            for attr_name in ['overwrite_prompt', 'show_error', 'file_name_field', 
                            'save_button', 'cancel_button']:
                if hasattr(self, attr_name):
                    entity = getattr(self, attr_name)
                    if entity is not None and hasattr(entity, 'active'):
                        try:
                            entity.active = False
                        except:
                            pass
            
            # ✅ گام ۲: صدا زدن super().close() با try-except مخصوص
            try:
                super().close()
            except Exception as e:
                error_msg = str(e)
                if "'NoneType' object has no attribute 'active'" in error_msg:
                    print("Super().close() encountered None active attribute - continuing")
                else:
                    print(f"Unexpected error in super().close(): {e}")
            
            # ✅ گام ۳: destroy کردن entityها
            entities_to_destroy = []
            
            # جمع‌آوری entityها
            for attr_name in ['show_error', 'overwrite_prompt', 'file_name_field', 
                            'save_button', 'cancel_button']:
                if hasattr(self, attr_name):
                    entity = getattr(self, attr_name)
                    if entity is not None:
                        entities_to_destroy.append(entity)
                        setattr(self, attr_name, None)
            
            if hasattr(self, '_created_entities'):
                entities_to_destroy.extend(self._created_entities[:])
                self._created_entities.clear()
            
            # destroy کردن entityها
            for entity in entities_to_destroy:
                if entity is not None:
                    try:
                        # غیرفعال کردن قبل از destroy
                        if hasattr(entity, 'active'):
                            try:
                                entity.active = False
                            except:
                                pass
                        destroy(entity)
                    except Exception as e:
                        print(f"Error destroying entity: {e}")
            
            # ✅ گام ۴: پاک کردن children
            if hasattr(self, 'children'):
                try:
                    self.children.clear()
                except:
                    pass
            
            # ✅ گام ۵: garbage collection
            import gc
            gc.collect()
            
            print("FileBrowserOpen closed successfully.")
            
        except Exception as e:
            print(f"Error in close method: {e}")
            # تلاش نهایی برای بستن
            try:
                super().close()
            except:
                pass
    
    def create_overwrite_prompt(self):
        """ایجاد یا بازسازی prompt برای تایید بازنویسی فایل"""
        try:
            if hasattr(self, 'overwrite_prompt') and self.overwrite_prompt:
                try:
                    if not self.overwrite_prompt.is_empty():
                        self._destroy_entity_safe(self.overwrite_prompt)
                except:
                    pass
            
            self.overwrite_prompt = WindowPanel(
                content=(
                    Text('Overwrite?'),
                    Button('Yes', color=color.azure, on_click=self._save),
                    Button('Cancel')
                ), 
                z=-1, 
                popup=True, 
                enabled=False
            )
            self._created_entities.append(self.overwrite_prompt)
            return self.overwrite_prompt
            
        except Exception as e:
            print(f"Error creating overwrite prompt: {e}")
            return None
        
    def __call__(self, *args, **kwargs):
        return {
            "path": self.project_path,
            "name": self.project_name
        }