# try:
#     from UI_classes import *
#     print("✅ ایمپورت موفقیت‌آمیز بود!")
# except ModuleNotFoundError as e:
#     print(f"❌ فایل پیدا نشد: {e}")
#     print("مسیر جاری:", __file__)
    
#     import os
#     print("فایل‌های موجود در مسیر:")
#     for file in os.listdir('.'):
#         print(f"  - {file}")

###############################
#from ursina import *

################### creat menu
# from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

# app = Ursina()
# DropdownMenu('File', buttons=(
#     DropdownMenuButton('New'),
#     DropdownMenuButton('Open'),
#     DropdownMenu('Reopen Project', buttons=(
#         DropdownMenuButton('Project 1'),
#         DropdownMenuButton('Project 2'),
#         )),
#     DropdownMenuButton('Save'),
#     DropdownMenu('Options', buttons=(
#         DropdownMenuButton('Option a'),
#         DropdownMenuButton('Option b'),
#         )),
#     DropdownMenuButton('Exit'),
#     ))

# app.run()

######################### creat windowpanel
# '''
# WindowPanel is an easy way to create UI. It will automatically layout the content.
# '''
# from ursina import *
# from ursina import Ursina, ButtonGroup
# app = Ursina()
# wp = WindowPanel(
#     title='Custom Window',
#     content=(
#         Text('Name:'),
#         InputField(name='name_field'),
#         Button(text='Submit', color=color.azure),
#         Slider(),
#         Slider(),
#         ButtonGroup(('test', 'eslk', 'skffk'))
#         ),
#     popup=True
#     )
# wp.y = wp.panel.scale_y / 2 * wp.scale_y    # center the window panel
# wp.layout()

# def input(key):
#     if key == 'space':
#         wp.enabled = True

# app.run()


# from ursina import *
# from ursina.prefabs.window_panel import WindowPanel

# app = Ursina()

# # متغیرهای رنگ
# r_value = 255
# g_value = 100
# b_value = 50

# # پیش‌نمایش
# preview = None

# # تابع بروزرسانی رنگ
# def update_color():
#     if preview:
#         preview.color = color.rgb(r_value, g_value, b_value)

# # توابع تغییر اسلایدر
# def on_red_changed():
#     global r_value
#     r_value = int(red_slider.value)
#     update_color()

# def on_green_changed():
#     global g_value
#     g_value = int(green_slider.value)
#     update_color()

# def on_blue_changed():
#     global b_value
#     b_value = int(blue_slider.value)
#     update_color()

# # ساخت WindowPanel
# wp = WindowPanel(
#     title='RGB Color Picker',
#     content=(
#         Text('Red (R)', scale=1.2),
#         red_slider := Slider(min=0, max=255, default=r_value, step=1, on_value_changed=on_red_changed),
        
#         Text('Green (G)', scale=1.2),
#         green_slider := Slider(min=0, max=255, default=g_value, step=1, on_value_changed=on_green_changed),
        
#         Text('Blue (B)', scale=1.2),
#         blue_slider := Slider(min=0, max=255, default=b_value, step=1, on_value_changed=on_blue_changed),
        
#         Text(''),  # فاصله
        
#         # دکمه نمایش رنگ (پیش‌نمایش)
#         Button(
#             text='',
#             scale=(0.65, 0.45),
#             color=color.rgb(r_value, g_value, b_value),
#             highlight_color=color.rgb(r_value, g_value, b_value),   # ← مهم: نباید None باشد
#             pressed_color=color.rgb(r_value, g_value, b_value)
#         )
#     ),
#     popup=True
# )

# wp.y = wp.panel.scale_y / 2 * wp.scale_y
# wp.layout()

# # دسترسی به پیش‌نمایش
# preview = wp.content[-1]
# print (f"Panel content ==> {wp.content}")

# # بروزرسانی اولیه
# update_color()

# def input(key):
#     if key == 'space':
#         wp.enabled = not wp.enabled

# app.run()
#########################################################################
# from ursina import *
# from ursina import ButtonGroup
# from ursina.prefabs.window_panel import WindowPanel


# class create_entity_winPanel:
#     def __init__(self):
#         self.name_winPanel = None
#         self.transform_winPanel = None
#         self.SetColor_winPanel = None
    
#     def show_name_panel(self):
#         destroy(self.transform_winPanel)
#         destroy(self.SetColor_winPanel)
#         self.name_winPanel = WindowPanel(title='Create entity')
#         self.name_winPanel.content = (
#         InputField(name='name_field' , default_value="Entity Name") ,
#         Button(text="Set transform" , on_click = self.show_transform_panel) ,
#         Button(text="Set color" , on_click = self.show_color_panel) ,
#         Button(text="Creat Entity" , on_click = lambda : print("Entity created")),
#         Button(text="Cancel" , on_click = lambda : destroy(self.name_winPanel))
#         )
#         self.name_winPanel.layout()
#         # self.btn_set_transform = self.name_winPanel.content[-3]
#         # self.btn_set_color = self.name_winPanel.content[-2]
#         # self.btn_creat_entity = self.name_winPanel.content[-1]

#         # self.btn_set_transform.scale_x =  0.4
#         # self.btn_set_transform.text_entity.scale_x /=  0.4
#         # self.btn_set_transform.x = -0.25

#         # self.btn_set_color.scale_x =  0.4
#         # self.btn_set_color.text_entity.scale_x /=  0.4
#         # self.btn_set_color.x = 0.2
#         # self.btn_set_color.y = -3

#         # self.btn_creat_entity.scale_x =  0.4
#         # self.btn_creat_entity.text_entity.scale_x /=  0.4
#         # self.btn_creat_entity.x = -0.01

#         # self.btn_group.value = 'my default value is empty'
#         # print(self.btn_group.value)
#         # 
#         # self.btn_group.scale = self.btn_group.get_scale() * 0.8
#         #self.btn_set_transform.on_click = lambda : self.transform_content()

    
#     def show_transform_panel(self):
#         destroy(self.name_winPanel)
#         destroy(self.SetColor_winPanel)
#         self.transform_winPanel = WindowPanel(title='Transform')
#         print('clicked')
#         self.transform_winPanel.content = (
#             InputField(name='Position_x' , default_value='0.0' , limit_content_to='-+.0123456789') , 
#             InputField(name='Position_y' , default_value='0.0' , limit_content_to='-+0123456789') ,
#             InputField(name='Position_z' , default_value='0.0' , limit_content_to='-+0123456789') ,

#             Button(text="Back to set Name" , on_click = self.show_name_panel) ,
#             Button(text="Set color" , on_click = self.show_color_panel) ,
#             Button(text="Creat Entity" , on_click = lambda : print("Entity created"))
#         )
#         self.transform_winPanel.layout()
#         # #Transform
#         # self.position_x_field = InputField(name='Position_x' , default_value='0.0' , limit_content_to='-+.0123456789')
#         # self.position_y_field = InputField(name='Position_y' , default_value='0.0' , limit_content_to='-+0123456789')
#         # self.position_z_field = InputField(name='Position_z' , default_value='0.0' , limit_content_to='-+0123456789')

#         # self.rotation_x_field = InputField(name='Rotation_x' , default_value='0.0' , limit_content_to='-+0123456789')
#         # self.rotation_y_field = InputField(name='Rotation_y' , default_value='0.0' , limit_content_to='-+0123456789')
#         # self.rotation_z_field = InputField(name='Rotation_z' , default_value='0.0' , limit_content_to='-+0123456789')

#         # self.scale_x_field = InputField(name='Position_x' , default_value='0' , limit_content_to='-+0123456789')
#         # self.scale_y_field = InputField(name='Position_x' , default_value='0' , limit_content_to='-+0123456789')
#         # self.scale_z_field = InputField(name='Position_x' , default_value='0' , limit_content_to='-+0123456789')

#         # return (
#         #         self.position_x_field ,
#         #         self.position_y_field ,
#         #         self.position_z_field ,
#         #         self.rotation_x_field ,
#         #         self.rotation_y_field ,
#         #         self.rotation_z_field ,
#         #         self.scale_x_field ,
#         #         self.scale_y_field ,
#         #         self.scale_z_field ,
#         #     )
    
#     def show_color_panel(self):
#         destroy(self.name_winPanel)
#         destroy(self.transform_winPanel)
#         self.SetColor_winPanel = WindowPanel(title='Set color')
#         self.SetColor_winPanel.content = (
#         Slider(min=0, max=100, default=0, step=1, on_value_changed=self.color_update) , 
#         Slider(min=0, max=100, default=0, step=1, on_value_changed=self.color_update) , 
#         Slider(min=0, max=100, default=0, step=1, on_value_changed=self.color_update) ,
#         Sprite(model = 'quad' , scale=(0.65, 0.45), color=color.red) ,

#         Button(text="Back to set Name" , on_click = self.show_name_panel) ,
#         Button(text="Set transform" , on_click = self.show_color_panel) ,
#         Button(text="Creat Entity" , on_click = lambda : print("Entity created"))
#         )
#         self.SetColor_winPanel.layout()

#     def color_update(self):
#         self.color_preview.color = color.rgb(self.slider_red.value / 100 , self.slider_green.value / 100, self.slider_blue.value / 100)
#         print(f"color updated ==> {self.color_preview.color}")
    
#     def clear_panel(self):
#         for child in list(self.children):  # لیست کپی بگیریم چون حین حذف تغییر می‌کنه
#             if child != self.panel:        # پنل background رو حذف نکنیم
#                 destroy(child)
                
            
# app = Ursina()
# c = create_entity_winPanel()
# c.show_name_panel()
# app.run()
from ursina import *

app = Ursina()

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


# استفاده از کلاس
x = ScrollableInputField(
    name='Position_y',
    default_value='0.0',
    limit_content_to='-+0123456789.',
    active=True
)

Text(text="روی InputField اسکرول کنید", y=0.35, scale=1.5)
Text(text="(تعداد ارقام اعشار step را تعیین می‌کند)", y=0.28, scale=1.2)

app.run()
# wp = WindowPanel(
#     title='RGB Color Picker',
#     content=(
#         InputField(name='Position_x' , default_value='0.0' , limit_content_to='-+.0123456789') , 
#             InputField(name='Position_y' , default_value='0.0' , limit_content_to='-+0123456789') ,
#             InputField(name='Position_z' , default_value='0.0' , limit_content_to='-+0123456789') ,

#             InputField(name='Rotation_x' , default_value='0.0' , limit_content_to='-+.0123456789') , 
#             InputField(name='Rotation_y' , default_value='0.0' , limit_content_to='-+0123456789') ,
#             InputField(name='Rotation_z' , default_value='0.0' , limit_content_to='-+0123456789') ,

#             InputField(name='Scale_x' , default_value='0.0' , limit_content_to='-+.0123456789') , 
#             InputField(name='Scale_y' , default_value='0.0' , limit_content_to='-+0123456789') ,
#             InputField(name='Scale_z' , default_value='0.0' , limit_content_to='-+0123456789') ,


#             Button(text="Back to set Name") ,
#             Button(text="Set color") ,
#             Button(text="Creat Entity")
#     ),
#     popup=True,
#     min_width=400
# )
# #LVecBase3f(0.5, 0.05, 1)
# btn_group = wp.content[-1]
# print(f"Button group : {btn_group.get_position()}")
# wp.y = wp.panel.scale_y / 2 * wp.scale_y
# wp.layout()
# btn_group.x = -0.4
# btn_group.scale = btn_group.get_scale() * 0.8
#app.run()
