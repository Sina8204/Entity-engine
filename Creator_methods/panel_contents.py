from ursina import *
from ursina.prefabs.window_panel import WindowPanel
from .UI_classes import ColorPicker
from .Entity_creator import create_entity

class ScrollableInputField(InputField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collider = 'box'
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
        return float(self.text)

class create_entity_winPanel:
    def __init__(self):
        self.name_winPanel = None
        self.transform_winPanel = None
        self.SetColor_winPanel = None
        self.model = ''
        self.entity_details = {
            'model' : self.model , 
            'position' : {
                'x' : 0.0 ,
                'y' : 0.0 ,
                'z' : 0.0
            } ,
            'rotation' : {
                'x' : 0.0 ,
                'y' : 0.0 ,
                'z' : 0.0
            } ,
            'scale' : {
                'x' : 1.0 ,
                'y' : 1.0 ,
                'z' : 1.0
            } ,
            'color' : color.random_color()
        }

    
    def show_name_panel(self , model):
        destroy(self.transform_winPanel)
        destroy(self.SetColor_winPanel)
        self.model = model
        self.entity_details['model'] = self.model
        self.name_winPanel = WindowPanel(title='Create entity')
        self.name_winPanel.content = (
        InputField(name='name_field' , default_value="Entity Name") ,
        Button(text="Set transform" , on_click = self.show_transform_panel) ,
        Button(text="Set color" , on_click = self.show_color_panel) ,
        Button(text="Creat Entity" , on_click = self.create_entity),
        Button(text="Cancel" , on_click = lambda : destroy(self.name_winPanel))
        )
        self.name_winPanel.layout()
        self.name_winPanel.y = self.name_winPanel.panel.scale_y / 2 * self.name_winPanel.scale_y
    
    def position_panel(self):
        destroy(self.transform_winPanel)
        self.position_winPanel = WindowPanel(title='Transform')
        self.position_winPanel.content =(
            Text('Position X :'),
            ScrollableInputField(name='Position_x' , default_value='0.0' , limit_content_to='-+.0123456789') , 
            Text('Position Y :'),
            ScrollableInputField(name='Position_y' , default_value='0.0' , limit_content_to='-+.0123456789') ,
            Text('Position Z :'),
            ScrollableInputField(name='Position_z' , default_value='0.0' , limit_content_to='-+.0123456789') ,

            Button(text="Set position" , on_click = lambda : self.set_position()) ,
            Button(text="Cancel" , on_click = lambda : (destroy(self.position_winPanel) , self.show_transform_panel()))
        )
        self.position_winPanel.layout()
        self.position_winPanel.y = self.position_winPanel.panel.scale_y / 2 * self.position_winPanel.scale_y
    
    def rotation_panel(self):
        destroy(self.transform_winPanel)
        self.rotation_winPanel = WindowPanel(title='Transform')
        self.rotation_winPanel.content =(
            Text('Rotation X :'),
            ScrollableInputField(name='Rotation_x' , default_value='0.0' , limit_content_to='-+.0123456789') , 
            Text('Rotation Y :'),
            ScrollableInputField(name='Rotation_y' , default_value='0.0' , limit_content_to='-+.0123456789') ,
            Text('Rotation Z :'),
            ScrollableInputField(name='Rotation_z' , default_value='0.0' , limit_content_to='-+.0123456789') ,

            Button(text="Set Rotation" , on_click = self.set_rotation) ,
            Button(text="Cancel" , on_click = lambda : (destroy(self.rotation_winPanel) , self.show_transform_panel()))
        )
        self.rotation_winPanel.layout()
        self.rotation_winPanel.y = self.rotation_winPanel.panel.scale_y / 2 * self.rotation_winPanel.scale_y
    
    def scale_panel(self):
        destroy(self.transform_winPanel)
        self.scale_winPanel = WindowPanel(title='Transform')
        self.scale_winPanel.content =(
            Text('Scale X :'),
            ScrollableInputField(name='Scale_x' , default_value='0.0' , limit_content_to='-+.0123456789') , 
            Text('Scale Y :'),
            ScrollableInputField(name='Scacle_y' , default_value='0.0' , limit_content_to='-+.0123456789') ,
            Text('Scale Z :'),
            ScrollableInputField(name='Scale_z' , default_value='0.0' , limit_content_to='-+.0123456789') ,

            Button(text="Set Scale" , on_click = self.set_scale) ,
            Button(text="Cancel" , on_click = lambda : (destroy(self.scale_winPanel) , self.show_transform_panel()))
        )
        self.scale_winPanel.layout()
        self.scale_winPanel.y = self.scale_winPanel.panel.scale_y / 2 * self.scale_winPanel.scale_y

    def show_transform_panel(self):
        destroy(self.name_winPanel)
        destroy(self.SetColor_winPanel)
        self.transform_winPanel = WindowPanel(title='Transform')
        print('clicked')
        self.transform_winPanel.content = (
            Button(text="Position" , on_click = self.position_panel) ,
            Button(text="Rotation" , on_click = self.rotation_panel) ,
            Button(text="Scale" , on_click = self.scale_panel) ,
            Text(' '),
            Button(text="Back to set Name" , on_click = lambda : self.show_name_panel(self.model)) ,
            Button(text="Set color" , on_click = self.show_color_panel) ,
            Button(text="Creat Entity" , on_click = lambda : print("Entity created"))
        )
        self.transform_winPanel.layout()
        self.transform_winPanel.y = self.transform_winPanel.panel.scale_y / 2 * self.transform_winPanel.scale_y
        print(f"transform panel ==> {self.transform_winPanel.content[0]}")
    
    def show_color_panel(self):
        destroy(self.name_winPanel)
        destroy(self.transform_winPanel)
        self.SetColor_winPanel = WindowPanel(title='Set color')
        self.SetColor_winPanel.content = (
            ColorPicker(),
            # Slider(min=0, max=100, default=0, step=1, on_value_changed=self.color_update) , 
            # Slider(min=0, max=100, default=0, step=1, on_value_changed=self.color_update) , 
            # Slider(min=0, max=100, default=0, step=1, on_value_changed=self.color_update) ,
            # Sprite(model = 'quad' , scale=(1, 0.6), color=color.red) ,
            Space(5),
            Button(text="Back to set Name" , on_click = lambda : self.show_name_panel(self.model)) ,
            Button(text="Set transform" , on_click = self.show_transform_panel) ,
            Button(text="Set color")
        )
        self.SetColor_winPanel.layout()
        self.SetColor_winPanel.y = self.SetColor_winPanel.panel.scale_y / 2 * self.SetColor_winPanel.scale_y
        self.SetColor_winPanel.content[-1].on_click = self.set_color

    def set_color(self):
        self.entity_details['color'] = self.SetColor_winPanel.content[0].value
        print(f"Color : {self.entity_details['color']}")
    
    def set_position(self):
        self.entity_details['position']['x'] = self.position_winPanel.content[1].value
        self.entity_details['position']['y'] = self.position_winPanel.content[3].value
        self.entity_details['position']['z'] = self.position_winPanel.content[5].value
        print(f"postion seted ==> x:{self.entity_details['position']['x']}, y:{self.entity_details['position']['y']} , z:{self.entity_details['position']['z']}")
        
    
    def set_rotation(self):
        self.entity_details['rotation']['x'] = self.rotation_winPanel.content[1].value
        self.entity_details['rotation']['y'] = self.rotation_winPanel.content[3].value
        self.entity_details['rotation']['z'] = self.rotation_winPanel.content[5].value
        print(f"rotation seted ==> x:{self.entity_details['rotation']['x']}, y:{self.entity_details['rotation']['y']} , z:{self.entity_details['rotation']['z']}")
    
    def set_scale(self):
        self.entity_details['scale']['x'] = self.scale_winPanel.content[1].value
        self.entity_details['scale']['y'] = self.scale_winPanel.content[3].value
        self.entity_details['scale']['z'] = self.scale_winPanel.content[5].value
        print(f"scale seted ==> x:{self.entity_details['scale']['x']}, y:{self.entity_details['scale']['y']} , z:{self.entity_details['scale']['z']}")

    def create_entity(self):
        create_entity(
            model = self.entity_details['model'] ,
            position = Vec3(self.entity_details['position']['x'] , self.entity_details['position']['y'] , self.entity_details['position']['z']) ,
            rotation = (self.entity_details['rotation']['x'] , self.entity_details['rotation']['y'] , self.entity_details['rotation']['z']) ,
            scale = (self.entity_details['scale']['x'] , self.entity_details['scale']['y'] , self.entity_details['scale']['z']) ,
            color = self.entity_details['color']
        )
        destroy(self.name_winPanel)
        destroy(self.transform_winPanel)
        destroy(self.SetColor_winPanel)

    
    def clear_panel(self):
        for child in list(self.children):  # لیست کپی بگیریم چون حین حذف تغییر می‌کنه
            if child != self.panel:        # پنل background رو حذف نکنیم
                destroy(child)
    

            
# app = Ursina()
# c = create_entity_winPanel()
# c.show_name_panel('cube')
# app.run()

