from ursina import *
from ursina import Entity, Slider, color, Button, camera, Quad, copy, Color
from ursina.prefabs.dropdown_menu import DropdownMenu , DropdownMenuButton
import importlib.util
import sys

import tkinter as tk
from tkinter import filedialog , messagebox
import os
from pathlib import Path


def execute_file_module(file_path , *args, **kwargs):
    """
    اجرای فایل پایتون به صورت ماژول
    مناسب برای فایل‌هایی که کلاس یا تابع مشخص دارند
    """
    # try:
    # تبدیل مسیر به نام ماژول
    module_name = os.path.basename(file_path).replace('.py', '')
    
    # لود کردن ماژول از فایل
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    print(module)
    
    # پیدا کردن و اجرای تابع main یا execute اگر وجود داشته باشد
    if hasattr(module, 'main'):
        if args or (len(kwargs.keys()) > 0):
            return (module.main(*args, **kwargs))
        else :
            module.main()
        print(f"✅ تابع main از {file_path} اجرا شد")
    else:
        print(f"⚠️ فایل {file_path} اجرا شد ولی تابع main یا execute پیدا نشد")
    
    return True
        
    # except Exception as e:
    #     print(f"❌ خطا در اجرای ماژول: {e}")
    #     return False

class ScrollableInputField(InputField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min_value = kwargs.get('min_value', None)
        self.max_value = kwargs.get('max_value', None)
        self._update_step()  # تنظیم اولیه step

    def _update_step(self):
        """محاسبه step بر اساس تعداد ارقام اعشار فعلی"""
        try:
            text = self.text.strip()
            if '.' in text:
                decimal_places = len(text.split('.')[1])
                self.step = 10 ** (-decimal_places)
            else:
                self.step = 1.0  # عدد صحیح
        except:
            self.step = 0.1  # مقدار پیش‌فرض

    def input(self, key):
        super().input(key)

        if mouse.hovered_entity == self and self.active:
            if key not in ('scroll up', 'scroll down'):
                # اگر کاربر دستی تایپ کرد، step را بروزرسانی کن
                self._update_step()
                return

            try:
                current = float(self.text)
            except ValueError:
                current = 0.0

            if key == 'scroll up':
                new_value = current + self.step
            else:  # scroll down
                new_value = current - self.step

            # اعمال محدودیت
            if self.min_value is not None:
                new_value = max(self.min_value, new_value)
            if self.max_value is not None:
                new_value = min(self.max_value, new_value)

            # رفع مشکل دقت اعشاری (مهم‌ترین بخش)
            # round به تعداد ارقام مناسب
            decimal_places = len(str(self.step).split('.')[-1]) if '.' in str(self.step) else 0
            new_value = round(new_value, decimal_places)

            self.text = str(new_value)

            # بروزرسانی step بعد از تغییر
            self._update_step()

            # اگر تابعی برای تغییر مقدار داری
            if hasattr(self, 'on_value_changed') and callable(self.on_value_changed):
                self.on_value_changed()
    
    @property
    def value(self):
        try:
            return float(self.text)
        except Exception as e:
            return 0.0

class desimal_inputfield(InputField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.accept = 'numbers'  # فقط اعداد را قبول می‌کند
        self.text = '0.0'  # مقدار اولیه
        self.access_change = False  # فلگ دسترسی
        self.is_hovered = False
        self.mouse_start_x = 0  # موقعیت اولیه موس هنگام کلیک
        self.current_decimal = 0.0  # مقدار اعشار فعلی
        
    def input(self, key):
        if key == 'left mouse down' and self.is_hovered:
            # همگام‌سازی current_decimal با مقدار فعلی متن
            try:
                self.current_decimal = float(self.text)
            except:
                self.current_decimal = 0.0
                
            self.access_change = True
            self.mouse_start_x = mouse.x  # ذخیره موقعیت اولیه موس
            print("left click pressed")
        elif key == 'left mouse up':
            self.access_change = False
            print('left click released')
    
    def update(self):
        # اگر دسترسی تغییر فعال باشد و موس روی فیلد باشد
        if self.access_change:
            # محاسبه تغییر موقعیت موس
            mouse_delta = mouse.x - self.mouse_start_x
            
            # اگر موس به سمت راست حرکت کرد (افزایش)
            if mouse_delta > 0.02:  # آستانه حرکت برای جلوگیری از لرزش
                self.current_decimal += 0.1
                self.mouse_start_x = mouse.x  # بازنشانی موقعیت
                self.update_text()
            
            # اگر موس به سمت چپ حرکت کرد (کاهش)
            elif mouse_delta < -0.02:  # آستانه حرکت برای جلوگیری از لرزش
                self.current_decimal -= 0.1
                self.mouse_start_x = mouse.x  # بازنشانی موقعیت
                self.update_text()
    
    def update_text(self):
        # بروزرسانی متن فیلد با مقدار اعشاری جدید
        self.text = f"{self.current_decimal:.1f}"
        print(f"Decimal value: {self.current_decimal:.1f}")
    
    def on_mouse_enter(self):
        self.is_hovered = True
        print("mouse entered")
        return super().on_mouse_enter()
    
    def on_mouse_exit(self):
        self.is_hovered = False
        #self.access_change = False  # غیرفعال کردن تغییرات هنگام خروج موس
        print("mouse exited")
        return super().on_mouse_exit()
    
    @property
    def value(self):
        try:
            return float(self.text)
        except Exception as e:
            return 0.0

class menu_creator:
    def __init__(self , path = '' , *args, **kwargs):
        self.path = path
        self.menu_cache = {}
    def create_menus(self , path , *args, **kwargs):
        # اگر قبلاً این مسیر را پردازش کرده‌ایم، منوهای ذخیره شده را برگردان
        if path in self.menu_cache:
            return self.menu_cache[path]
        
        menus = []
        try:
            items = sorted(os.listdir(path))
            
            for item in items:
                if item.startswith("__") : continue
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    item_name = item.split('_')[1] if '_' in item else item
                    # بررسی می‌کنیم که آیا این پوشه قبلاً منوی خود را ساخته است
                    if item_path in self.menu_cache:
                        # از منوی ذخیره شده استفاده کن
                        button = DropdownMenu(text=item_name, name=item_name, buttons=self.menu_cache[item_path])
                    else:
                        # منوی جدید بساز
                        sub_menus = self.create_menus(item_path)
                        file_items = sorted(os.listdir(item_path))
                        if len(file_items)>0:
                            for file in file_items:
                                file_path = os.path.join(item_path, file)
                                if not os.path.isdir(file_path):
                                    file_name = file.split('.')[0]
                                    file_name = file_name.split('_')[-1] if '_' in file_name else file_name
                                    sub_menus.append(DropdownMenuButton(text=file_name , name = file_name , on_click = lambda f = file_path: execute_file_module(f , *args, **kwargs)))
                        button = DropdownMenu(text=item_name, name=item_name, buttons=sub_menus)
                    
                    menus.append(button)
                    
        except Exception as e:
            print(f'Error: {e}')
        
        # ذخیره منوهای ساخته شده در کش
        self.menu_cache[path] = menus
        return menus
    
    def get_buttons_menu(self , path , *args, **kwargs):
        button_menus = []
        try:
            items = sorted(os.listdir(path))

            for item in items:
                if '__' in item : continue
                item_path = os.path.join(path, item)
                if not os.path.isdir(item_path):
                    item_name = item.split('_')[1] if '_' in item else item
                    button_menus.append(DropdownMenuButton(text=item_name , name = item_name , on_click = lambda f = item_path : execute_file_module(f , *args , **kwargs)))
        except Exception as e:
            print(f'Error: {e}')
        
        return button_menus
    
    def __call__(self, *args, **kwds):
        return {
            "menu" : self.create_menus(self.path , *args, **kwds) , 
            "buttons" : self.get_buttons_menu(self.path , *args, **kwds)
        }
    

class Sort_menus():
    def __init__(self , menus : list[DropdownMenu] , menus_x_pos = 0.0 , menus_between_space = 0.25):
        try :
            self.menu = menus
            self.menus_x_pos = menus_x_pos
            self.menus_between_space = menus_between_space
            self.x_position = window.left.x + self.menus_x_pos
            for menu in self.menu:
                menu.parent = camera.ui
                menu.y = window.top.y
                menu.x = self.x_position
                self.x_position += self.menus_between_space  # فاصله بین منوها (می‌توانید تنظیم کنید)
        except Exception as e:
            print(f"menus ==> {self.menu}")
            print(f"Error : \n{e}")
    
    def __call__(self, *args, **kwds):
        return tuple(self.menu)

get_menu = menu_creator()
class catch_menus():
    def __init__(self , path = '' , **keywargs):
        self.path = path
        self.menu_list = get_menu.create_menus(self.path , kwargs = keywargs)
        print(f"Some arguments are in all menus ===> {keywargs}")

    def __call__(self, *args, **kwds):
        return self.menu_list


class Entity_tree_menu :
    def __init__(self, key, value, parent, x, y, level=0):
        self.key = key
        self.value = value
        self.parent = parent
        self.level = level
        self.children = []
        self.is_expanded = False
        self.is_leaf = len(value) == 0  # کلید نهایی (بدون زیرمجموعه)
        
        # ایجاد دکمه اصلی
        color_btn = color.rgb(60, 160, 120) if self.is_leaf else color.rgb(50, 100, 200)
        self.button = Button(
            text=key,
            parent=camera.ui,
            position=(x, y),
            scale=(0.25, 0.045),
            origin=(0, 0)
        )
        
        # نشانگر برای زیرمجموعه‌ها
        if not self.is_leaf:
            self.indicator = Text(
                text= '>', #'▶'
                parent=camera.ui,
                position=(x - 0.15, y),
                scale=1.2,
                color=color.white
            )
        else:
            self.indicator = None
        
        # تابع کلیک
        self.button.on_click = self.toggle
        
        # اگر کلید نهایی باشد، اطلاعات را چاپ می‌کند
        if self.is_leaf:
            pass
        else:
            self.button.on_click = self.toggle
        
        #self.button.add_script(PrintScript('hello world'))
        
        
    
    def get_full_path(self):
        """دریافت مسیر کامل از ریشه تا کلید فعلی"""
        if self.parent:
            return f"{self.parent.get_full_path()}.{self.key}"
        return self.key
    
    def toggle(self):
        if self.is_expanded:
            self.collapse()
        else:
            self.expand()
    
    def expand(self):
        if self.is_leaf:
            return
        
        self.is_expanded = True
        if self.indicator:
            self.indicator.text = '\/'#'▼'
        
        # ایجاد زیرمجموعه‌ها
        y_offset = 0
        for child_key, child_value in self.value.items():
            if child_key == 'scr' : continue
            child = Entity_tree_menu(
                key=child_key,
                value=child_value,
                parent=self,
                x=self.button.x + 0.05, # X indentation
                y=self.button.y - 0.05 - y_offset,
                level=self.level + 1,
            )
            
            self.children.append(child)
            y_offset += 0.05
        
        # جابجایی دکمه‌های پایین‌تر
        if self.parent:
            self.parent.shift_buttons_down(y_offset)
    
    def collapse(self):
        self.is_expanded = False
        if self.indicator:
            self.indicator.text = '>' #'▶'
        
        # حذف زیرمجموعه‌ها
        for child in self.children:
            child.destroy()
        self.children.clear()
        
        # جابجایی دکمه‌های پایین‌تر به بالا
        if self.parent:
            self.parent.shift_buttons_up(len(self.children) * 0.07)
    
    def shift_buttons_down(self, amount):
        """جابجایی دکمه‌های بعدی به پایین"""
        if self.parent:
            index = self.parent.children.index(self) if self in self.parent.children else -1
            for child in self.parent.children[index+1:]:
                child.button.y -= amount
                if child.indicator:
                    child.indicator.y -= amount
                for subchild in child.children:
                    subchild.shift_down(amount)
    
    def shift_buttons_up(self, amount):
        """جابجایی دکمه‌های بعدی به بالا"""
        if self.parent:
            index = self.parent.children.index(self) if self in self.parent.children else -1
            for child in self.parent.children[index+1:]:
                child.button.y += amount
                if child.indicator:
                    child.indicator.y += amount
                for subchild in child.children:
                    subchild.shift_up(amount)
    
    def shift_down(self, amount):
        self.button.y -= amount
        if self.indicator:
            self.indicator.y -= amount
        for child in self.children:
            child.shift_down(amount)
    
    def shift_up(self, amount):
        self.button.y += amount
        if self.indicator:
            self.indicator.y += amount
        for child in self.children:
            child.shift_up(amount)
    
    def destroy(self):
        destroy(self.button)
        if self.indicator:
            destroy(self.indicator)
        for child in self.children:
            child.destroy()

class ColorPicker(Entity):
    default_values = dict(parent=camera.ui)

    def __init__(self, dynamic=True, show_exit_button=False, **kwargs):
        super().__init__(**(__class__.default_values | kwargs))

        # Background
        self.bg = Entity(parent=self, z=.01, model=Quad(aspect=.5/.2), 
                        scale=[.5, .225], origin=[0, .5], color=color.black66)

        # متد _calculate_color را زودتر تعریف می‌کنیم (برای جلوگیری از خطا)
        self.on_value_changed = None

        # ساخت اسلایدرها
        self.h_slider = Slider(parent=self, max=360, step=1, dynamic=dynamic, 
                              on_value_changed=self._calculate_color)
        self.h_slider.bg.texture = 'rainbow'

        self.s_slider = Slider(parent=self, max=100, step=1, dynamic=dynamic, 
                              on_value_changed=self._calculate_color)
        self.s_slider.overlay = Entity(parent=self.s_slider.bg, model=copy(self.s_slider.bg.model), 
                                      z=-.01, texture='horizontal_gradient', color=color.gray)

        self.v_slider = Slider(parent=self, max=100, step=1, dynamic=dynamic, 
                              on_value_changed=self._calculate_color)
        self.v_slider.bg.color = color.black
        self.v_slider.overlay = Entity(parent=self.v_slider.bg, model=copy(self.s_slider.bg.model), 
                                      z=-.01, texture='horizontal_gradient', color=color.black)

        self.a_slider = Slider(parent=self, max=100, default=100, step=1, dynamic=dynamic, 
                              on_value_changed=self._calculate_color)

        # تنظیمات مشترک اسلایدرها
        for i, slider in enumerate((self.h_slider, self.s_slider, self.v_slider, self.a_slider)):
            slider.knob.model.mode = 'line'
            slider.knob.model.thickness = 2
            slider.knob.model.generate()
            slider.knob.color = color.white
            slider.bg.color = color.white
            slider.y = -.05 - (i * .03)
            slider.scale = .8
            slider.x = -.25 + .05

        # Preview
        self.preview = Button(parent=self, scale=(.5 * .84, .05), origin=[0, .5], 
                             y=self.a_slider.y - .02, color=color.white)

        # Exit button
        self.exit_button = Button(parent=self, scale=.05, position=(.25 - .01, -.01), 
                                 model='circle', color=color.red.tint(-.25), text='x', 
                                 on_click=self.disable, enabled=show_exit_button)

        # محاسبه اولیه رنگ
        self._calculate_color()

        # اعمال kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    # متد محاسبه رنگ (حالا قبل از فراخوانی در __init__ قرار گرفته)
    def _calculate_color(self):
        self.color = color.hsv(
            self.h_slider.value, 
            self.s_slider.value / 100, 
            self.v_slider.value / 100, 
            self.a_slider.value / 100
        )
        self.preview.color = self.color
        self.preview.highlight_color = self.color
        self.preview.pressed_color = self.color

        self.s_slider.bg.color = color.hsv(self.h_slider.value, 1, 1)

        if self.on_value_changed:
            self.on_value_changed()

    @property
    def value(self):
        return color.hsv(
            self.h_slider.value,
            self.s_slider.value / 100,
            self.v_slider.value / 100,
            self.a_slider.value / 100
        )

    @value.setter
    def value(self, value: Color):
        value = value.hsv
        self.h_slider.value = value[0]
        self.s_slider.value = value[1] * 100
        self.v_slider.value = value[2] * 100
        self.a_slider.value = value[3] * 100

    # برای WindowPanel بهتر کار کند
    @property
    def scale_y(self):
        return 0.34   # می‌توانید این عدد را بین 0.28 تا 0.38 تنظیم کنید
    
class show_message():
    def __init__(self, win_title = 'Message', message = 'This is a message'):
        super().__init__()
        self.show_error = WindowPanel(title = win_title , content=(
                 Text(text = message),
                 Button(text='Close' , on_click = lambda : destroy(self.show_error))
             ))
        self.show_error.content[0].x += 0.15

            
class PanelManager:
    def __init__(self , **shared_values):
        self.shared_values = shared_values
        self.panels = {}
    
    def add_panels(self , **panels : WindowPanel):
        """
        The input arguments should be as follows : panel_name = WindowPanel(title = str , content(UI_class1 , UI_class2 , ...) , enabled = False)
        - Tip :
                Arguments WindowPanel 'enabeled' value must be 'False'
        + For exampel ) A panel manager with 'name' , 'age' & 'city' panels :
                panel_manager = PanelManager()
                panel_manager.add_panels(
                                        name = WindowPanel(title="Panel name" , content = (
                                                            Text(name = "name_text" , text = "panel name") , 
                                                            Button( name = 'panel_age' , text = 'Go to age panel') , 
                                                            Button( name = 'panel_city' , text = 'Go to city panel')
                                                            ) , enabled = False
                                                        ) ,
                                        age = WindowPanel(title= "Panel age" , content = (
                                                            Button( name = 'panel_name' , text = 'Go to name panel') ,
                                                            Text(name = "age_text" , text = "panel age"),
                                                            Button( name = 'panel_city' , text = 'Go to city panel')
                                                            ) , enabled = False
                                                        ) ,
                                        city = WindowPanel(title= "Panel city" , content = (
                                                            Button( name = 'panel_name' , text = 'Go to name panel') ,
                                                            Button( name = 'panel_age' , text = 'Go to age panel') ,
                                                            Text(name = "city_text" , text ="panel city")
                                                            ) , enabled = False
                                                        )
                                        )
                panel_manager.enabel_panel('name') # At first , active and show panel 'name'
        """
        for key , value in list(panels.items()):
            if not isinstance(value , WindowPanel):
                raise ValueError(f"Argument value type shuld be 'WindowPanel'. But you enterd {key} = {value} and {value} type is {type(value)}")
            self.panels.update({key : value})
    
    def connect_panel_buttons(self , **ButtonName_TargetPanel):
        """
        Panels have buttons to navigate to other panels
        So you can use this method to connect buttons to their panel.
        Just pass arguments to this method like this : Button_name = 'panel_name'

        - Tip : 
                panel_name is the argument name that you creat WindowPanel by method add_panels.

        * Attention : 
                The name of a button attached to a panel , must be the same in all panels.
                Otherwise , you will encounter a logic error.
        + For exampel:
                panel_manager.connect_panel_buttons(panel_name = 'name' , panel_age = 'age' , panel_city = 'city')
        """
        for current_panel in list(self.panels.keys()):
            for btn_name , target_panel in list(ButtonName_TargetPanel.items()):
                if self._isthere(current_panel , Button , btn_name):
                    btn_index = self._get_widget_index(name = btn_name , panel_name=current_panel , widget_type=Button)
                    if btn_index != None : 
                        self.button_connection(current_panel , target_panel , btn_index)
                        print(f"{current_panel} : {btn_name}({btn_index}) --> {target_panel}")
    
    def enabel_panel(self , panel_name : str):
        """
        By use this method , you can show a panel. Just input panel_name as 'str'
        """
        self.hide_panels()
        self.panels[panel_name].enabled = True
    
    def set_position(self , x = 0.0 , y = 0.0 , mode = "custom"):
        """
        You shuld use this method for set position of the panel.
        By 'mode' argument you can set position at center:
                    mode = 'y_center' : sets the panel position on the vertical axis to the center.
                    mode = 'x_center' : sets the panel position on the horizontal axis to the center.
        + example :
            1) 'custom'   : panel_manager.set_position(x = 0.55 , y = 0.45)
            2) 'y_center' : panel_manager.set_position(x = 0.6 , mode='y_center')
            3) 'x_center' : panel_manager.set_position(y = 0.5 , mode='x_center')
        """
        match (mode):
            case "custom": 
                for key , value in list(self.panels.items()):
                    self.panels[key].position = (x , y)
                    self.panels[key].layout()
            case "y_center":
                for key , value in list(self.panels.items()):
                    self.panels[key].y = self.panels[key].panel.scale_y / 2 * self.panels[key].scale_y
                    self.panels[key].x = x
                    self.panels[key].layout()
            case "x_center":
                for key , value in list(self.panels.items()):
                    self.panels[key].position = (0 , y)
                    self.panels[key].layout()
    
    def set_content_attr(self , panel_name = '' , index_of_content = None , content = None , attr = '' , value = None):
        """
        You shuld use 'set_content_attr' method when you want change 
        value of a panel widget attribute like '.text' , '.name' , 'position' and etc.
        - guid :
                1) At first select widget panel name by argument 'panel_name' as str.
                2) you can use one of the arguments 'index_of_content' and 'content' for choose your widget :
                        - index_of_content : when you want choose your widget by its index at the tuple of WindowPanel content. 
                        - content : when you want choose your widget by its 'name' and 'ui class'.
                    * Attention : 
                                content type mest be a tuple with two index like '('widget_name' , widget_class)'.
                                if index_of_content and content , content becomes None and index_of_content is considered.
                3) Choose your attribute by argument 'attr' as a str.
                4) input your value by argument 'value'
        
        + example :
                    # Choose content by index_of_content :
                        panel_manager.set_content_attr(
                                                        panel_name = 'age' , 
                                                        index_of_content = 1 , 
                                                        attr='text' , 
                                                        value="Here is age panel"
                                                    )
                    # Choose content by its name and ui class :
                        panel_manager.set_content_attr(
                                                        panel_name = 'city' , 
                                                        content=('city_text' , Text) , 
                                                        attr='text' , 
                                                        value="Here is panel city"
                                                    )
        """
        error = "One of the arguments index_of_content and content must have value!!"
        help1 = "content must be a tuple like ('content_name' , content_class)"
        help2 = "index_of_content must be integer"
        help3 = "if index_of_content and content , content becomes None and index_of_content is considered"

        if index_of_content is not None and content is not None:
            content = None
        if index_of_content is None and content is None:
            raise ValueError(f"{error} Use this guid :\n\t1){help1}\n\t2){help2} \n\t3){help3}")
        if index_of_content is None and not isinstance(content , tuple):
            raise ValueError(f"{help1}. But you enterd {content} that type is {type(content)}")
        if not isinstance(index_of_content , int) and content is None:
            raise ValueError(f"{help2}. But you enterd {content} that type is {type(content)}")
        if isinstance(content , tuple):
            if len(content) > 2 or len(content) < 2:
                raise ValueError(f"content must have 2 index like ('content_name' , content_class)")
            if not isinstance(content[0] , str):
                raise ValueError(f"content first index type must be 'str' but you entered object with type ({type(content[0])})")

        
        if index_of_content is None and content is not None:
            if self._isthere(panel_name , content[1] , content[0]):
                index_of_content = self._get_widget_index(content[0] , panel_name , content[1])
            else:
                raise ValueError(f"In {panel_name} panel there is not any {content[1]} class with name '{content[0]}'")
        if hasattr(self.panels[panel_name].content[index_of_content] , attr):
            setattr(self.panels[panel_name].content[index_of_content], attr , value)
        else:
            raise AttributeError(f"type '{self.panels[panel_name].content[index_of_content]}' don't have attribute with name '{attr}'")

    def set_content_event(self , panel_name = '' , index_of_content = None , content = None , event = '' , handler = None):
        """
        You should use this method when you want to assign an
        event-driven value to an event-driven property of widgets.
        events like '.on_click' , '.on_value_changed' and etc.
        * How to use :
                    The method of using this method is the same as the 'set_content_attr' method, 
                    except that instead of entering a 'attr', you must enter a 'handler' that is a function.
        """
        error = "One of the arguments index_of_content and content must have value!!"
        help1 = "content must be a tuple like ('content_name' , content_class)"
        help2 = "index_of_content must be integer"
        help3 = "if index_of_content and content , content becomes None and index_of_content is considered"

        if index_of_content is not None and content is not None:
            content = None
        if index_of_content is None and content is None:
            raise ValueError(f"{error} Use this guid :\n\t1){help1}\n\t2){help2} \n\t3){help3}")
        if index_of_content is None and not isinstance(content , tuple):
            raise ValueError(f"{help1}. But you enterd {content} that type is {type(content)}")
        if not isinstance(index_of_content , int) and content is None:
            raise ValueError(f"{help2}. But you enterd {content} that type is {type(content)}")
        if isinstance(content , tuple):
            if len(content) > 2 or len(content) < 2:
                raise ValueError(f"content must have 2 index like ('content_name' , content_class)")
            if not isinstance(content[0] , str):
                raise ValueError(f"content first index type must be 'str' but you entered object with type ({type(content[0])})")

        if index_of_content is None and content is not None:
            if self._isthere(panel_name , content[1] , content[0]):
                index_of_content = self._get_widget_index(content[0] , panel_name , content[1])
            else:
                raise ValueError(f"In {panel_name} panel there is not any {content[1]} class with name '{content[0]}'")

        if hasattr(self.panels[panel_name].content[index_of_content] , event):
            setattr(self.panels[panel_name].content[index_of_content], event , handler)
        else:
            raise AttributeError(f"type '{self.panels[panel_name].content[index_of_content]}' don't have attribute with name '{event}'")

    def button_connection(self , button_panel : str , target_panel : str , button_index):
        if button_index == None : return
        self.panels[button_panel].content[button_index].on_click = lambda : self.enabel_panel(target_panel)

    def get_widget_value(self , Panel_name : str , widget_name : str , widget_class , attr = ""):
        index = self._get_widget_index(name = widget_name , panel_name = Panel_name , widget_type = widget_class)
        if index is not None:
            if hasattr(self.panels[Panel_name].content[index] , attr):
                return getattr(self.panels[Panel_name].content[index] , attr)
    
    def hide_panels(self):
        for key in list(self.panels.keys()):
            self.panels[key].enabled = False
    
    def destroy_panels(self):
        for key , value in list(self.panels.items()):
            destroy(self.panels[key])
    
    def _isthere(self , panel_name , widget_type , widget_name):
        for value in list(self.panels[panel_name].content):
            if not isinstance(value , widget_type) :  continue
            if value.name == widget_name : return True
            else : continue
        return False
    
    def _get_widget_index(self , name , panel_name , widget_type = None):
        for index , value in enumerate(list(self.panels[panel_name].content)):
            if widget_type != None:
                if not isinstance(value , widget_type): continue
            if value.name == name:
                return index


class Customization_filedialog:
    def __init__(self):
        pass

    def asksaveasfilename_box(self , 
                    title = None , 
                    msg = None , 
                    defult_path = None ,
                    defult_name = None ,
                    filetypes = None , 
                    TypeErrorTitle = None, 
                    TypeErrorMessage = None , 
                    FileExistsErrorTitle = None, 
                    FileExistsErrorMessage = None ,
                    open_exists_file = True):
        root = tk.Tk()
        root.withdraw()  # مخفی کردن پنجره اصلی
        box_title = title if not title is None else ''
        box_msg = msg if not msg is None else ''
        box_filetypes = filetypes if not filetypes is None else [("All Files", "*.*")]
        try :
            path = filedialog.asksaveasfilename(
                confirmoverwrite = False ,
                title=f"{box_title} - {box_msg}",
                initialdir = defult_path ,
                initialfile = defult_name ,
                filetypes=box_filetypes
            )
            if os.path.exists(path):
                raise FileExistsError
            root.destroy()
            return {"name" : str(Path(path).stem) , "path" : path}
        except FileExistsError as fee:
            if not open_exists_file:
                error_title = FileExistsErrorTitle if not FileExistsErrorTitle is None else "File exists error"
                error_message = FileExistsErrorMessage if not FileExistsErrorMessage is None else "A file with the same name as the one you selected already exists in this path. Please choose a different name or path."
                messagebox.showerror(title = f"{error_title}" , message = f"{error_message}")
                root.destroy()
                return self.asksaveasfilename_box(title = box_title , msg = box_msg , filetypes = box_filetypes)
            else :
                return {"name" : str(Path(path).stem) , "path" : path}
        except TypeError as te:
            error_title = TypeErrorTitle if not TypeErrorTitle is None else "Type error"
            error_message = TypeErrorMessage if not TypeErrorMessage is None else f"{te}"
            messagebox.showerror(title = f"{error_title}" , message = f"{error_message}") #Script file creation operation has been canceled.
            root.destroy()
            return None
    
    def openfile(self, 
                title = None , 
                msg = None , 
                defult_path = None ,
                defult_name = None ,
                filetypes = None , 
                TypeErrorTitle = None, 
                TypeErrorMessage = None):
        root = tk.Tk()
        root.withdraw()  # مخفی کردن پنجره اصلی
        box_title = title if not title is None else ''
        box_msg = msg if not msg is None else ''
        box_filetypes = filetypes if not filetypes is None else [("All Files", "*.*")]
        try :
            path = filedialog.askopenfile(
                title=f"{box_title} - {box_msg}",
                initialdir = defult_path ,
                initialfile = defult_name ,
                filetypes=box_filetypes
            )
            root.destroy()
            if path and os.path.exists(str(path.name)):
                return str(path.name)
            else:
                return None
        except TypeError as te:
            error_title = TypeErrorTitle if not TypeErrorTitle is None else "Type error"
            error_message = TypeErrorMessage if not TypeErrorMessage is None else f"{te}"
            messagebox.showerror(title = f"{error_title}" , message = f"{error_message}") #Script file creation operation has been canceled.
            root.destroy()
            return None
    
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
    
class Entity_scripts_args_manager(tk.Tk):
    def __init__(self, args : list , kwargs : dict ):
        super().__init__()
        self.geometry("500x400")

        self.top_btns_frame = tk.Frame(self)
        self.top_btns_frame.pack(fill="x", expand=True)  

        self.attrs_frame = tk.Frame(self)
        self.attrs_frame.pack(fill="both", expand=True)  
        
        # self.bottom_btns_frame = tk.Frame(self)
        # self.bottom_btns_frame.pack(fill="x", pady=5)  

        self.btn_add_arg = tk.Button(self.top_btns_frame, text="Add argument" , command = lambda : self.add_arg(new=True))
        self.btn_add_arg.pack(side="left", fill="both", expand=True)
        self.btn_add_key_argument = tk.Button(self.top_btns_frame, text="Add key argument" , command = self.add_kwargs)
        self.btn_add_key_argument.pack(side="left", fill="both", expand=True)
        self.btn_update_canvas = tk.Button(self.top_btns_frame, text="Update" , command = self.update_attrs)
        self.btn_update_canvas.pack(side="left", fill="both", expand=True)
        
        # self.btn_put_attrs = tk.Button(self.bottom_btns_frame, text="Insert values")
        # self.btn_put_attrs.pack(side="left", fill="both", expand=True)  
        # self.btn_cancel = tk.Button(self.bottom_btns_frame, text="Cancel")
        # self.btn_cancel.pack(side="left", fill="both", expand=True)
        
        self.kwargs = kwargs
        self.args = args if isinstance(args , list) else list(args)
        self.create_canvas()
    
    def update_attrs(self):
        self.canvas.destroy()
        self.scrollbar.destroy()
        self.create_canvas()
    def create_canvas(self):
        # Create a Canvas as the main scrolling platform
        self.canvas = tk.Canvas(self.attrs_frame, borderwidth=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.attrs_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Putting Canvas and Scrollbar Together
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create an inner frame that the content fits inside.
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw", width=self.canvas.winfo_width())

        # Bind the internal frame resize event to update the scroll range.
        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        # Bind Canvas resize event to adjust content width
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Enable scrolling with mouse (wheel or trackpad)
        self._bind_mousewheel()

        for i , arg in enumerate(self.args):
            self.add_arg(entry_text=arg , index=i)

        for key , value in list(self.kwargs.items()):
            self.add_kwargs(key , value)

    def _on_frame_configure(self, event):
        """Update scroll range when resizing inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Set the width of the content inside the Canvas to the width of the Canvas itself"""
        self.canvas.itemconfig(1, width=event.width)

    def _bind_mousewheel(self):
        """Enable scrolling with mouse wheel and trackpad"""
        def on_mousewheel(event):
            # For Windows and Linux
            if event.delta:
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            else:  # For Mac (event.num)
                if event.num == 4:
                    self.canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    self.canvas.yview_scroll(1, "units")

        # Connecting different events for different operating systems
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)      # Windows/Linux
        self.canvas.bind_all("<Button-4>", on_mousewheel)        # Mac (scroll up)
        self.canvas.bind_all("<Button-5>", on_mousewheel)        # Mac (scroll down)

    def _on_button_arg_click(self , var_available : tk.BooleanVar , btn : tk.Button , arg , index : tk.IntVar , is_new : tk.BooleanVar):
        """Button Function: Display the value of the corresponding Entry"""
        print(arg)
        match(var_available.get()):
            case True :
                var_available.set(False)
                btn.config(text="Add again")
                if arg in self.args:
                    self.args.remove(arg)
            case False :
                var_available.set(True)
                btn.config(text="Remove")
                if is_new.get():
                    self.args.append(arg)
                else:
                    if index.get() < len(self.args):
                        self.args.insert(index.get() , arg)
                    else :
                        self.args.append(arg)
        print(f"Removed arg :\nvar_available : {var_available.get()}\nargs : {self.args}")
    
    def add_arg(self , entry_text = '' , index = 0 , new = False):
        # Each row in a separate frame for better layout
        row_frame = tk.Frame(self.inner_frame)
        row_frame.pack(fill="x", padx=5, pady=2)
        check_available = tk.BooleanVar(row_frame , value=True if entry_text and entry_text in self.args else False)
        check_new = tk.BooleanVar(row_frame , value=new)
        arg_index = tk.IntVar(row_frame , value = index)
        # Create Entry (Text Field)
        entry = tk.Entry(row_frame, width=30)
        entry.pack(side="left", padx=(0, 5))
        entry.insert(tk.END , entry_text)

        # Create a button next to Entry
        btn_text = ''
        if entry_text:
            if entry_text in self.args:
                btn_text = "Remove"
            else:
                btn_text = "Add"
        else:
            btn_text = "Add"
        btn = tk.Button(row_frame, text=btn_text)
        btn.pack(side="left")
        btn.config(command = lambda available = check_available , button = btn , index = arg_index: self._on_button_arg_click(var_available = available ,btn = button , arg=entry.get() , index = index , is_new = check_new))

    def _on_button_kwarg_click(self , var_available : tk.BooleanVar , key , value , btn : tk.Button):
        match(var_available.get()):
            case True:
                var_available.set(False)
                if key in list(self.kwargs.keys()):
                    self.kwargs.pop(key)
                btn.config(text="Add again")
            case False:
                var_available.set(True)
                if key and value:
                    self.kwargs.update({key : value})
                btn.config(text="Remove")
        print(f"Removed kwarg :\nvar_available : {var_available.get()}\nkwargs : {self.kwargs}")
    def add_kwargs(self , key = '' , value = ''):
        # Each row in a separate frame for better layout
        row_frame = tk.Frame(self.inner_frame)
        row_frame.pack(fill="x", padx=5, pady=2)

        check_available = tk.BooleanVar(row_frame , value=True if (key , value) in list(self.kwargs.items()) else False)

        # Create Entry (Text Field)
        entry_key = tk.Entry(row_frame , width=20)
        entry_key.pack(side="left", padx=(0, 5))
        entry_key.insert(tk.END , str(key))

        entry_value = tk.Entry(row_frame , width=20)
        entry_value.pack(side="left", padx=(0, 5))
        entry_value.insert(tk.END , str(value))

        # Create a button next to Entry
        btn_text = ''
        if key or value:
            if (key , value) in list(self.kwargs.items()):
                btn_text = "Remove"
            else:
                btn_text = "Add"
        else :
            btn_text = "Add"
        btn = tk.Button(row_frame, text=btn_text)
        btn.pack(side="left")
        btn.config(command = lambda : self._on_button_kwarg_click(var_available = check_available , key = entry_key.get() , value = entry_value.get() , btn = btn))

    def get_all_values(self):
        return {
            "args" : self.args ,
            "kwargs" : self.kwargs
        }

    def __call__(self, *args, **kwds):
        return {
            "args" : tuple(self.args) ,
            "kwargs" : self.kwargs
        }


custom_fd = Customization_filedialog()

# app = Ursina()
# p = Button(model='quad', scale=(.4, .8), collider='box')
# # for i in range(8):
# #     Button(parent=p , scale_y=.05, text=f'giopwjoigjwr{i}', origin_y=.5, y=.5-(i*.05))

# p.add_script(Scrollable())
# app.run()