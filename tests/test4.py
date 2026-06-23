# from ursina import *

# app = Ursina()

# # buttons = {
# #     'player' : {
# #         'camera' : {
# #             'char' : {} ,
# #             'gun' : {
# #                 'bullet' : {},
# #                 'fire_pos' : {}
# #             }
# #         }
# #     }
# # }

# # def print_keys(dictionary, indent=0):
# #     for key, value in dictionary.items():
# #         print('  ' * indent + f'- {key}')
# #         if isinstance(value, dict):
# #             print_keys(value, indent + 1)

# # print_keys(buttons)

# btn = Button(
#     text='Father' , 
#     model='quad' , 
#     scale_x =0.1 , 
#     scale_y = 0.05 , 
#     x = window.left.x + 0.07 , 
#     y = window.top_right.y - 0.05
#     )



# app.run()

##############################################################################

# from ursina import *
# from ursina import camera

# app = Ursina()

# buttons_dict = {
#     'player': {
#         'camera': {
#             'char': {},
#             'gun': {
#                 'bullet': {},
#                 'fire_pos': {}
#             }
#         }
#     }
# }

# class TreeMenu:
#     def __init__(self, data, parent=None, x=-0.5, y=0.4, spacing=0.1):
#         self.buttons = []
#         self.data = data
#         self.parent_menu = parent
#         self.x = x
#         self.y = y
#         self.spacing = spacing
#         self.visible = True
#         self.create_buttons()
    
#     def create_buttons(self):
#         y_offset = 0
#         for key, value in self.data.items():
#             btn = Button(
#                 text=key,
#                 parent=camera.ui,
#                 position=(self.x, self.y - y_offset),
#                 scale=(0.3, 0.05),
#                 origin=(0, 0)
#             )
            
#             # ذخیره اطلاعات در دکمه
#             btn.submenu_data = value
#             btn.submenu_instance = None
#             btn.parent_menu = self
#             btn.key_name = key
            
#             # تابع کلیک
#             def on_click(btn=btn):
#                 self.on_button_click(btn)
            
#             btn.on_click = on_click
#             self.buttons.append(btn)
#             y_offset += self.spacing
    
#     def on_button_click(self, btn):
#         # حذف ساب‌منوی قبلی اگر وجود داشت
#         if hasattr(self, 'current_submenu') and self.current_submenu:
#             self.current_submenu.destroy()
        
#         # اگر دکمه زیرمجموعه دارد
#         if btn.submenu_data and len(btn.submenu_data) > 0:
#             # ایجاد ساب‌منو با موقعیت جدید
#             self.current_submenu = TreeMenu(
#                 btn.submenu_data,
#                 parent=self,
#                 x=self.x + 0.35,
#                 y=btn.y,
#                 spacing=self.spacing
#             )
#             self.current_submenu.visible = True
    
#     def destroy(self):
#         for btn in self.buttons:
#             destroy(btn)
#         if hasattr(self, 'current_submenu') and self.current_submenu:
#             self.current_submenu.destroy()

# # ایجاد منوی اصلی
# main_menu = TreeMenu(buttons_dict)

# # دکمه بازگشت به منوی اصلی (اختیاری)
# def reset_menu():
#     global main_menu
#     if main_menu:
#         main_menu.destroy()
#     main_menu = TreeMenu(buttons_dict)

# reset_btn = Button(
#     text='Reset Menu',
#     parent=camera.ui,
#     position=(0.7, -0.45),
#     scale=(0.2, 0.05),
#     on_click=reset_menu
# )

# # نمایش اطلاعات در کنسول با کلیک روی دکمه نهایی (اختیاری)
# info_text = Text('Click on menu items', position=(-0.8, -0.4), scale=1)

# def update():
#     pass

# app.run()





from ursina import *

app = Ursina()

buttons_dict = {
    'player': {
        'scr' : '' ,
        'camera': {
            'scr' : '' ,
            'char': {
                'scr' : ''
            },
            'gun': {
                'scr' : '' ,
                'bullet': {},
                'fire_pos': {}
            }
        }
    }
}

class TreeMenuItem:
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
            def on_click_final(btn=self.button):
                print(f"✅ Selected: {self.get_full_path()}")
                info_text.text = f"Selected: {self.get_full_path()}"
            self.button.on_click = on_click_final
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
            child = TreeMenuItem(
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

# ایجاد منوی اصلی
root = TreeMenuItem('Show', buttons_dict, None, -0.7, 0.4, 0)
#root.button.visible = False  # ریشه را مخفی می‌کنیم

# نمایش مستقیم کلیدهای سطح اول
# y_pos = 0.4
# for key, value in buttons_dict.items():
#     print(f'key : {key}' , f'\nvalue : {value}')
#     item = TreeMenuItem(key, value, None, -0.7, y_pos, 1)
#     root.children.append(item)
#     y_pos -= 0.07

# متن نمایش اطلاعات
info_text = Text('Click on leaf items to see the path', position=(-0.8, -0.45), scale=1.2, color=color.yellow)

app.run()
