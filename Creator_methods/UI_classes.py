from ursina import *
from ursina import Entity, Slider, color, Button, camera, Quad, copy, Color
from ursina.prefabs.dropdown_menu import DropdownMenu , DropdownMenuButton
import importlib.util
import sys


def execute_file_module(file_path , *args, **kwargs):
    """
    اجرای فایل پایتون به صورت ماژول
    مناسب برای فایل‌هایی که کلاس یا تابع مشخص دارند
    """
    try:
        # تبدیل مسیر به نام ماژول
        module_name = os.path.basename(file_path).replace('.py', '')
        
        # لود کردن ماژول از فایل
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(module)
        
        # پیدا کردن و اجرای تابع main یا execute اگر وجود داشته باشد
        if hasattr(module, 'main'):
            if args:
                module.main(*args, **kwargs)
            else :
                module.main()
            print(f"✅ تابع main از {file_path} اجرا شد")
        elif hasattr(module, 'execute'):
            if args:
                module.execute(*args, **kwargs)
            else:
                module.execute()
            print(f"✅ تابع execute از {file_path} اجرا شد")
        else:
            print(f"⚠️ فایل {file_path} اجرا شد ولی تابع main یا execute پیدا نشد")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در اجرای ماژول: {e}")
        return False

menu_cache = {}
def create_menus(path , *args, **kwargs):
    # اگر قبلاً این مسیر را پردازش کرده‌ایم، منوهای ذخیره شده را برگردان
    menu_cache = {}
    if path in menu_cache:
        return menu_cache[path]
    
    menus = []
    check_update_menu_created = False
    try:
        items = sorted(os.listdir(path))
        
        for item in items:
            if '__' in item : continue
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                item_name = item.split('_')[1] if '_' in item else item
                # بررسی می‌کنیم که آیا این پوشه قبلاً منوی خود را ساخته است
                if item_path in menu_cache:
                    # از منوی ذخیره شده استفاده کن
                    button = DropdownMenu(text=item_name, name=item_name, buttons=menu_cache[item_path])
                else:
                    # منوی جدید بساز
                    sub_menus = create_menus(item_path)
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
    menu_cache[path] = menus
    return menus

class Sort_menus():
    def __init__(self , menus : list[DropdownMenu]):
        self.menu = menus
        self.x_position = window.left.x + 0.0
        for menu in self.menu:
            menu.parent = camera.ui
            menu.y = window.top.y
            menu.x = self.x_position
            self.x_position += 0.25  # فاصله بین منوها (می‌توانید تنظیم کنید)
    
    def __call__(self, *args, **kwds):
        return tuple(self.menu)

class catch_menus():
    def __init__(self , path = ''):
        self.path = path
        self.menu_list = create_menus(self.path)

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
    

'''
This will make target entity move up or down when you hover the entity/its children
while scrolling the scroll wheel.
'''

# app = Ursina()
# p = Button(model='quad', scale=(.4, .8), collider='box')
# # for i in range(8):
# #     Button(parent=p , scale_y=.05, text=f'giopwjoigjwr{i}', origin_y=.5, y=.5-(i*.05))

# p.add_script(Scrollable())
# app.run()