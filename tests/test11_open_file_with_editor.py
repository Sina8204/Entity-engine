# # import subprocess
# # import sys
# # import os

# # def open_file_with_custom_editor(file_path, editor=None):
# #     """
# #     فایل را با ادیتور مشخص یا پیش‌فرض سیستم باز می‌کند
    
# #     پارامترها:
# #     file_path: مسیر فایل
# #     editor: نام ادیتور (مثلاً 'notepad', 'vim', 'code', 'nano')
# #     """
# #     try:
# #         if not os.path.exists(file_path):
# #             raise FileNotFoundError(f"فایل {file_path} وجود ندارد")
            
# #         # اگر ادیتور مشخص نشده، از پیش‌فرض سیستم استفاده کن
# #         if editor is None:
# #             if sys.platform == 'win32':
# #                 os.startfile(file_path)
# #             elif sys.platform == 'darwin':
# #                 subprocess.run(['open', file_path], check=True)
# #             else:
# #                 subprocess.run(['xdg-open', file_path], check=True)
# #         else:
# #             # با ادیتور مشخص شده باز کن
# #             subprocess.run([editor, file_path], check=True)
            
# #         print(f"فایل {file_path} با {editor or 'ادیتور پیش‌فرض'} باز شد")
        
# #     except FileNotFoundError as e:
# #         print(f"خطا: {e}")
# #     except subprocess.CalledProcessError as e:
# #         print(f"خطا در اجرای ادیتور {editor}: {e}")
# #     except Exception as e:
# #         print(f"خطای غیرمنتظره: {e}")

# # # مثال‌های استفاده
# # open_file_with_custom_editor("Data.txt")  # با ادیتور پیش‌فرض
# # open_file_with_custom_editor("Data.txt", "notepad")  # ویندوز - Notepad
# # open_file_with_custom_editor("Data.txt", "code")  # VS Code
# # open_file_with_custom_editor("Data.txt", "vim")  # Vim

# import easygui
# import subprocess
# import os

# def select_editor_with_easygui():
#     """
#     انتخاب ادیتور با استفاده از easygui
#     """
#     # انتخاب فایل با دیالوگ زیبا
#     file_path = easygui.fileopenbox(
#         title="انتخاب ادیتور",
#         default="*.exe",
#         filetypes=["*.exe", "*.com", "*.bat", "*.*"]
#     )
#     return file_path

# def open_file_with_easygui(file_path):
#     """
#     باز کردن فایل با ادیتور انتخاب شده از طریق easygui
#     """
#     try:
#         if not os.path.exists(file_path):
#             easygui.msgbox(f"فایل {file_path} وجود ندارد!", "خطا")
#             return
        
#         # انتخاب ادیتور
#         editor_path = select_editor_with_easygui()
        
#         if not editor_path:
#             easygui.msgbox("هیچ ادیتوری انتخاب نشد", "اطلاع")
#             return
        
#         # باز کردن فایل
#         subprocess.run([editor_path, file_path], check=True)
#         easygui.msgbox(
#             f"فایل با {os.path.basename(editor_path)} باز شد", 
#             "موفقیت"
#         )
        
#     except Exception as e:
#         easygui.msgbox(f"خطا: {e}", "خطا")

# # مثال استفاده
# # open_file_with_easygui("Data.txt")
# import easygui

# # ساده‌ترین شکل استفاده
# # pash = easygui.diropenbox(
# #     msg="here msg" ,
# #     title="here title"
# # )

# # pash = easygui.filesavebox(
# #     msg="here msg" ,
# #     title="here title",
# # )

# # print(f"path = {pash}")

import easygui
import os

# def save_project_with_name():
#     # مرحله ۱: دریافت نام پروژه از کاربر
#     project_name = easygui.enterbox(
#         msg='نام پروژه را وارد کنید:',
#         title='نام پروژه',
#         default='my_project'
#     )
    
#     if not project_name:
#         easygui.msgbox("عملیات لغو شد", "لغو")
#         return None
    
#     # مرحله ۲: انتخاب مسیر ذخیره با نام پیش‌فرض
#     file_path = easygui.diropenbox(
#         msg=f'لطفاً مسیر ذخیره پروژه "{project_name}" را انتخاب کنید:',
#         title='ذخیره پروژه',
#         default=f'{project_name}.py' #,
#         #filetypes=['*.py', '*.txt', '*.json']
#     )
    
#     if file_path:
#         print(f"پروژه {project_name} در مسیر {file_path} ذخیره شد")
#         return file_path
#     else:
#         print("ذخیره لغو شد")
#         return None

# # مثال استفاده
# save_project_with_name()
import tkinter as tk
from tkinter import filedialog , messagebox
import os
from pathlib import Path

class Customization_filedialog:
    def __init__(self):
        pass

    def asksaveasfilename_box(self , 
                    title = None , 
                    msg = None , 
                    filetypes = None , 
                    TypeErrorTitle = None, 
                    TypeErrorMessage = None , 
                    FileExistsErrorTitle = None, 
                    FileExistsErrorMessage = None):
        root = tk.Tk()
        root.withdraw()  # مخفی کردن پنجره اصلی
        box_title = title if not title is None else ''
        box_msg = msg if not msg is None else ''
        box_filetypes = filetypes if not filetypes is None else [("All Files", "*.*")]
        # try :
        path = filedialog.asksaveasfilename(
            title=f"{box_title} - {box_msg}",
            filetypes=box_filetypes ,
            initialfile= 'test'
        )
        # if os.path.exists(path):
        #     raise FileExistsError
        root.destroy()
        return {"name" : str(Path(path).stem) , "path" : path}
        # except FileExistsError as fee:
        #     error_title = FileExistsErrorTitle if not FileExistsErrorTitle is None else "File exists error"
        #     error_message = FileExistsErrorMessage if not FileExistsErrorMessage is None else "A file with the same name as the one you selected already exists in this path. Please choose a different name or path."
        #     messagebox.showerror(title = f"{error_title}" , message = f"{error_message}")
        #     root.destroy()
        #     return self.asksaveasfilename_box(title = box_title , msg = box_msg , filetypes = box_filetypes)
        # except TypeError as te:
        #     error_title = TypeErrorTitle if not TypeErrorTitle is None else "Type error"
        #     error_message = TypeErrorMessage if not TypeErrorMessage is None else f"{te}"
        #     messagebox.showerror(title = f"{error_title}" , message = f"{error_message}") #Script file creation operation has been canceled.
        #     root.destroy()
        #     return None
    
    def show_msg(self , type = 'info' , box_title = '' , msg = ''):
        """type can be : 'info' 'warnning' 'error' 
        Other values are considered 'info'."""
        root = tk.Tk()
        root.withdraw()
        match (type):
            case 'info' : messagebox.showinfo(title = box_title , message = msg)
            case 'warnning' : messagebox.showwarning(title = box_title , message = msg)
            case 'error' : messagebox.showerror(title = box_title , message = msg)
            case _ : messagebox.showinfo(title = box_title , message = msg)
        root.destroy()

# fd = Customization_filedialog()
# path = fd.asksaveasfilename_box(title = "select" , msg="file")
# t = path["path"].split('/')
# t2 = '/'.join(t)
# print(t)
# print(t2)
# print("-------------------------------")
# print(path)
# print(t)
# print(t2)
# print("-------------------------------")


def parse_string_to_list(input_string):
    """
    رشته‌ای مانند "1, 2, 3, 'test', 10.5" را به لیست تبدیل می‌کند.
    اعداد به صورت عدد (int/float) و رشته‌ها به صورت رشته نگهداری می‌شوند.
    """
    # حذف فاصله‌های اضافی و جداسازی بر اساس کاما
    items = [item.strip() for item in input_string.split(',')]
    
    result = []
    for item in items:
        # حذف نقل قول‌های اطراف رشته (اگر وجود داشته باشد)
        if (item.startswith('"') and item.endswith('"')) or \
           (item.startswith("'") and item.endswith("'")):
            result.append(item[1:-1])  # رشته خالص
            continue
        
        # بررسی عدد صحیح
        try:
            if '.' in item:
                result.append(float(item))  # عدد اعشاری
            else:
                result.append(int(item))    # عدد صحیح
        except ValueError:
            # اگر عدد نبود، همان رشته را نگه می‌داریم
            result.append(item)
    
    return result

# import ast
# import re
# from ursina import *
# def dict_to_string_advanced(dictionary):
#     """
#     تبدیل دیکشنری به رشته با استفاده از repr برای حفظ دقیق نوع داده‌ها
#     """
#     items = []
#     for key, value in dictionary.items():
#         # استفاده از repr برای نمایش دقیق مقدار
#         if isinstance(key, str):
#             key_str = f"'{key}'"
#         else:
#             key_str = repr(key)
        
#         # استفاده از repr برای نمایش دقیق مقدار با حفظ نوع
#         value_str = repr(value)
        
#         items.append(f"{key_str}: {value_str}")
    
#     return ', '.join(items)

# def string_to_dict_advanced(input_string):
#     """
#     تبدیل رشته به دیکشنری با استفاده از ast.literal_eval برای امنیت بیشتر
#     """
#     # اضافه کردن آکولاد برای تبدیل به دیکشنری معتبر Python
#     dict_string = '{' + input_string + '}'
    
#     try:
#         # استفاده از literal_eval برای تبدیل امن
#         result = ast.literal_eval(dict_string)
#         return result
#     except (SyntaxError, ValueError) as e:
#         print(f"خطا در تبدیل: {e}")
#         return {}
# app = Ursina()
# kwargs = {
#     'speed' : 0.5 ,
#     'color' : 'color.red' ,
#     'height' : 10
# }

# with open("tests/test_writ.py" , 'w+') as file:
#     file.write("(1 , 2 , 3)")
# from ursina import *

# app = Ursina()

# فعال کردن حالت نمایش کلایدرها
# window.render_mode = 'colliders'  # [citation:1]

# texture_path = load_texture("test_add_script/test_pic.jpg")
# # موجودیت نمونه با یک کلایدر
# ground = Entity(model='cube', scale=(10, 1, 10) , color = color.green ,texture = texture_path)
# ground.collider='box'

# print(f"texture => {ground.texture}")

# app.run()

from ursina import *

app = Ursina()

s = Sprite()
s.scale = (2 , 2)

app.run()