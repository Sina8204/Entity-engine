from ursina import *
from ursina.prefabs.file_browser import FileBrowser
from ursina.prefabs.file_browser_save import FileBrowserSave , FileButton
import os , json

class show_message():
    def __init__(self, win_title = 'Message', message = 'This is a message'):
        super().__init__()
        self.show_error = WindowPanel(title = win_title , content=(
                 Text(text = message),
                 Button(text='Close' , on_click = lambda : destroy(self.show_error))
             ))
        self.show_error.content[0].x += 0.15
        

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

        self.save_button = self.open_button
        self.save_button.color = color.azure
        self.save_button.text = 'Select this path'
        self.save_button.on_click = self._save
        self.file_name_field = InputField(parent=self, scale_x=.75, scale_y=self.save_button.scale_y, y=self.save_button.y)
        self.save_button.y -= .075
        self.cancel_button.y -= .075
        self.file_name_field.text_field.text = ''
        self.file_type = '' # to save as
        self.show_error = None

        self.last_saved_file = None     # gets set when you save a file
        self.overwrite_prompt = WindowPanel(
            content=(
                Text('Overwrite?'),
                Button('Yes', color=color.azure, on_click=self._save),
                Button('Cancel')
            ), z=-1, popup=True, enabled=False)

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


    def _save(self):
        file_name = self.file_name_field.text_field.text
        file_name = file_name.strip()
        if file_name:
            pass
        else:
             self.show_error = show_message(win_title = 'Field to make project' , message = 'Select a name for your project')
             return
    
        # if not file_name.endswith(self.file_type):
        #     file_name += self.file_type

        path = self.path / file_name
        if path.exists() and not self.overwrite_prompt.enabled:
            # print('overwrite file?')
            self.overwrite_prompt.enabled = True
        
        self.create_project(path)

        self.last_saved_file = path
        self.overwrite_prompt.enabled = False
        self.close()
        self.on_submit(path)


    def on_submit(self, path):  # implement .on_submit to handle saving
        print('save to path:', path, 'please implement .on_submit to handle saving')
    
    def create_project(self , path):
        try:
            os.mkdir(path)
            with open(f"{path}/details.json" , 'w+' , encoding='utf-8') as file:
                json.dump({} , file , indent=2 , ensure_ascii=False)
            print(f"Sucessfully at create folder '{path}'")
            return True
        except FileExistsError:
            print(f"Field at create folder '{path}'")
            self.show_error = show_message(win_title = 'Field at create folder' , message = 'There is a folder with name you entered')
            return
        except Exception as e:
            print(f"Error at create folder : {e}")
            self.show_error = show_message(win_title = 'Field at create folder' , message = 'See the terminal to read the error')
            return

    def close(self):
        """Override close method to also close error panel"""
        # بستن پنل خطا اگر وجود داشته باشد
        if hasattr(self, 'show_error') and self.show_error is not None:
            try:
                destroy(self.show_error)
                self.show_error = None
            except:
                pass  # اگر پنل قبلاً بسته شده باشد
        
        # فراخوانی متد close کلاس والد
        super().close()


def main():
    FileBrowserOpen(file_types=('.json',), enabled=True)
