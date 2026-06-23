from ursina import *
from Camera_controller import CameraController
from Creator_methods.Entity_creator import create_entity
from Creator_methods.panel_contents import create_entity_winPanel
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from Creator_methods.UI_classes import Menu

app = Ursina()

def print_dict_tree(d: dict, indent: int = 0, prefix: str = ""):
    """
    چاپ کردن دیکشنری به صورت درختی (Tree view)
    
    Args:
        d: دیکشنری ورودی
        indent: سطح تورفتگی فعلی
        prefix: پیشوند برای نمایش شاخه‌ها
    """
    new_prefix = ''
    if not d:
        print(" " * indent + "{} (خالی)")
        return
    
    items = list(d.items())
    for i, (key, value) in enumerate(items):
        # تعیین علامت شاخه (آخرین آیتم یا نه)
        is_last = i == len(items) - 1
        branch = "└── " if is_last else "├── "
        
        print(" " * indent + prefix + branch + str(key))
        
        # اگر مقدار یک دیکشنری باشد، دوباره تابع را فراخوانی کن
        if isinstance(value, dict):
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_dict_tree(value, indent + 4, new_prefix)
        
        # اگر لیست یا تاپل باشد
        elif isinstance(value, (list, tuple)):
            print(" " * (indent + 4) + new_prefix + "└── " + f"[{len(value)} مورد]")
            for j, item in enumerate(value):
                if isinstance(item, dict):
                    list_prefix = new_prefix + ("    " if j == len(value)-1 else "│   ")
                    print(" " * (indent + 8) + list_prefix + f"[{j}]:")
                    print_dict_tree(item, indent + 12, list_prefix)
                else:
                    print(" " * (indent + 8) + new_prefix + f"[{j}]: {item}")
        
        # مقادیر معمولی
        else:
            print(" " * (indent + 4) + new_prefix + "└── " + str(value))

# def create_menus(path):
#     """
#     ساختار درختی پوشه و فایل‌ها را به صورت دیکشنری برمی‌گرداند.
#     """
#     tree = {}
#     try:
#         # لیست تمام آیتم‌های داخل مسیر
#         items = sorted(os.listdir(path))  # مرتب‌سازی برای نمایش زیباتر
#         #print(f'Items : {items}')
        
#         for item in items:
#             item_path = os.path.join(path, item)
#             #print (f'{item} path : {item_path}')
            
#             if os.path.isdir(item_path):
#                 # اگر پوشه بود، به صورت بازگشتی درختش را بساز
#                 #print(f'item : {item}')
#                 item_name = item.split('_')[2]
#                 tree[item_name] = create_menus(item_path)

#             else:
#                 # اگر فایل بود، می‌توانی اطلاعات بیشتری هم ذخیره کنی
#                 tree[item] = 'file' # یا None یا اندازه فایل و ...
        
#     except PermissionError:
#         tree["🚫"] = "دسترسی غیرمجاز"
#     except FileNotFoundError:
#         tree["❌"] = "مسیر یافت نشد"
#     except Exception as e:
#         tree["⚠️"] = f"خطا: {e}"
    
#     return tree

###################################################################################

# def create_menus(path, parent_menu=None):
#     """
#     ساختار درختی پوشه و فایل‌ها را به صورت لیستی از منوها برمی‌گرداند.
#     parent_menu: منوی والد برای اضافه کردن فایل‌ها به آن
#     """
#     menu_items = []  # لیست منوهای این سطح
#     current_menu = parent_menu  # منوی فعلی برای فایل‌ها
    
#     try:
#         items = sorted(os.listdir(path))
        
#         # دسته‌بندی آیتم‌ها به پوشه و فایل
#         folders = []
#         files = []
        
#         for item in items:
#             item_path = os.path.join(path, item)
#             if os.path.isdir(item_path):
#                 folders.append(item)
#             else:
#                 files.append(item)
        
#         # پردازش پوشه‌ها
#         for folder in folders:
#             folder_path = os.path.join(path, folder)
#             # ایجاد منوی جدید برای پوشه
#             folder_name = folder.split('_')[2] if '_' in folder else folder
#             folder_menu = DropdownMenu(text=folder_name)
            
#             # پردازش محتویات پوشه به صورت بازگشتی
#             sub_menus = create_menus(folder_path, folder_menu)
            
#             # اضافه کردن زیرمنوها به منوی پوشه
#             if hasattr(folder_menu, 'add_submenu'):
#                 for sub_menu in sub_menus:
#                     if sub_menu:  # فقط منوهای معتبر را اضافه کن
#                         folder_menu.add_submenu(sub_menu)
            
#             menu_items.append(folder_menu)
#             current_menu = folder_menu  # به‌روزرسانی منوی فعلی برای فایل‌های این پوشه
        
#         # پردازش فایل‌ها
#         if files:
#             # اگر منوی والد وجود دارد، فایل‌ها را به آن اضافه کن
#             if parent_menu is not None:
#                 # اطمینان از وجود لیست buttons
#                 if not hasattr(parent_menu, 'buttons') or parent_menu.buttons is None:
#                     parent_menu.buttons = []
                
#                 # اضافه کردن همه فایل‌ها به منوی والد
#                 for file in files:
#                     button = DropdownMenuButton(text=file)
#                     parent_menu.buttons.append(button)
#             else:
#                 # اگر منوی والد وجود ندارد، یک منوی جدید برای فایل‌ها بساز
#                 file_menu = DropdownMenu(text="فایل‌ها")
#                 file_menu.buttons = []
#                 for file in files:
#                     button = DropdownMenuButton(text=file)
#                     file_menu.buttons.append(button)
#                 menu_items.append(file_menu)
        
#     except PermissionError:
#         print(f"🚫 دسترسی غیرمجاز به {path}")
#     except FileNotFoundError:
#         print(f"❌ مسیر {path} یافت نشد")
#     except Exception as e:
#         print(f"⚠️ خطا در {path}: {e}")
    
#     return menu_items

# کش برای ذخیره منوهای ساخته شده
menu_cache = {}


def create_menus(path):
    # اگر قبلاً این مسیر را پردازش کرده‌ایم، منوهای ذخیره شده را برگردان
    if path in menu_cache:
        return menu_cache[path]
    
    menus = []
    
    try:
        items = sorted(os.listdir(path))
        
        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                # بررسی می‌کنیم که آیا این پوشه قبلاً منوی خود را ساخته است
                if item_path in menu_cache:
                    # از منوی ذخیره شده استفاده کن
                    button = DropdownMenu(text=item, name=item, buttons=menu_cache[item_path])
                else:
                    # منوی جدید بساز
                    sub_menus = create_menus(item_path)
                    file_items = sorted(os.listdir(item_path))
                    if len(file_items)>0:
                        for file in file_items:
                            file_path = os.path.join(item_path, file)
                            if not os.path.isdir(file_path):
                                file_name = file.split('.')[0]
                                sub_menus.append(DropdownMenuButton(text=file_name , name = file_name , on_click = lambda f = file_name: print(f'Click {f}')))
                    button = DropdownMenu(text=item, name=item, buttons=sub_menus)
                
                menus.append(button)
                
                
    except Exception as e:
        print(f'Error: {e}')
    
    # ذخیره منوهای ساخته شده در کش
    menu_cache[path] = menus
    return menus



# file_menu = DropdownMenu('File' , buttons = (
#     DropdownMenuButton('New') ,
#     DropdownMenuButton('Open' , on_click = lambda : print("Open")) ,
#     DropdownMenuButton('Save' , on_click = lambda : print("Save")) ,
#     DropdownMenuButton('Save as' , on_click = lambda : print("Save as")) ,
#     DropdownMenuButton('Save project as' , on_click = lambda : print("Save project as")) ,
#     DropdownMenuButton('Exit' , on_click = lambda : print("Exit"))
# ))

# btn2 = DropdownMenu("entity2" , buttons=(
#     DropdownMenu('test2') ,
#     DropdownMenuButton('test2')
# ))
Menu(create_menus('project/menus'))
app.run()