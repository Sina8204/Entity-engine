from ursina import *
from .UI_classes import ColorPicker
from .UI_classes import Sort_menus , catch_menus , create_menus , execute_file_module
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
import copy


#app = Ursina()
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

class Add_child_menu:
    def __init__(self):
        self.menu_cache = {}

    def create_menus(self , path , *args, **kwargs):
        # اگر قبلاً این مسیر را پردازش کرده‌ایم، منوهای ذخیره شده را برگردان
        if path in self.menu_cache:
            return self.menu_cache[path]
        
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
                    if item_path in self.menu_cache:
                        # از منوی ذخیره شده استفاده کن
                        button = DropdownMenu(text=item_name, name=item_name, buttons=self.menu_cache[item_path])
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
        self.menu_cache[path] = menus
        return menus

class parent_panel():
    def __init__(self):
        self.panel_name = None
        self.panel_position = None
        self.panel_rotation = None
        self.panel_scale = None
        self.panel_color = None
    
    def window_panel_name(self , **func):
        self.hide_panels()
        self.panel_name = WindowPanel('Name')
        self.panel_name.content = (
        InputField(name='name_field' , default_value="Entity Name") ,
        Button(text="Set transform" , on_click = lambda : self.window_panel_position(**func)) ,
        Button(text="Set color" , on_click = lambda : self.window_panel_color(**func))
        )
        self.panel_name.layout()
        self.panel_name.y = self.panel_name.panel.scale_y / 2 * self.panel_name.scale_y
        self.panel_name.x = 0.6
        self.panel_name.content[0].on_value_changed = lambda : func['func_name'](str(self.panel_name.content[0].text))
        self.panel_name.content[0].text = func['obj'].name
    
    def window_panel_position(self , **func):
        self.hide_panels()
        self.panel_position = WindowPanel('Transform')
        self.panel_position.content = (
            Button(text='Name' , on_click = lambda : self.window_panel_name(**func)),
            Text('Position X :'),
            desimal_inputfield(name='Position_x' , default_value=str(0.0) , limit_content_to='-+.0123456789') , 
            Text('Position Y :'),
            desimal_inputfield(name='Position_y' , default_value=str(0.0) , limit_content_to='-+.0123456789') ,
            Text('Position Z :'),
            desimal_inputfield(name='Position_z' , default_value=str(0.0) , limit_content_to='-+.0123456789') ,
            Button('Rotation' , on_click = lambda : self.window_panel_rotation(**func)) ,
            Button('Scale' , on_click = lambda : self.window_panel_scale(**func)),
            Button('Color' , on_click = lambda : self.window_panel_color(**func))
        )
        self.panel_position.layout()
        self.panel_position.y = self.panel_position.panel.scale_y / 2 * self.panel_position.scale_y
        self.panel_position.x = 0.6

        self.panel_position.content[2].on_value_changed = lambda: func['func_pos_x'](float(self.panel_position.content[2].value))
        self.panel_position.content[2].text = str(func['obj'].x)
        self.panel_position.content[4].on_value_changed = lambda: func['func_pos_y'](float(self.panel_position.content[4].value))
        self.panel_position.content[4].text = str(func['obj'].y)
        self.panel_position.content[6].on_value_changed = lambda: func['func_pos_z'](float(self.panel_position.content[6].value))
        self.panel_position.content[6].text = str(func['obj'].z)
    
    def window_panel_rotation(self , **func):
        self.hide_panels()
        self.panel_rotation = WindowPanel('Transform')
        self.panel_rotation.content = (
            Button(text='Name' , on_click = lambda : self.window_panel_name(**func)),
            Button(text='Position' , on_click = lambda : self.window_panel_position(**func)) ,
            Text('Rotatoin X :'),
            desimal_inputfield(name='Rotation_x' , default_value=str(0.0) , limit_content_to='-+.0123456789') , 
            Text('Rotatoin Y :'),
            desimal_inputfield(name='Rotation_y' , default_value=str(0.0) , limit_content_to='-+.0123456789') ,
            Text('Rotatoin Z :'),
            desimal_inputfield(name='Rotation_z' , default_value=str(0.0) , limit_content_to='-+.0123456789') ,
            Button('Scale' , on_click = lambda : self.window_panel_scale(**func)),
            Button('Color', on_click = lambda : self.window_panel_color(**func))
        )
        self.panel_rotation.layout()
        self.panel_rotation.y = self.panel_rotation.panel.scale_y / 2 * self.panel_rotation.scale_y
        self.panel_rotation.x = 0.6

        self.panel_rotation.content[3].on_value_changed = lambda: func['func_rot_x'](float(self.panel_rotation.content[3].value))
        self.panel_rotation.content[3].text = str(func['obj'].rotation_x)
        self.panel_rotation.content[5].on_value_changed = lambda: func['func_rot_y'](float(self.panel_rotation.content[5].value))
        self.panel_rotation.content[5].text = str(func['obj'].rotation_y)
        self.panel_rotation.content[7].on_value_changed = lambda: func['func_rot_z'](float(self.panel_rotation.content[7].value))
        self.panel_rotation.content[7].text = str(func['obj'].rotation_z)

    def window_panel_scale(self , **func):
        self.hide_panels()
        self.panel_scale = WindowPanel('Transform')
        self.panel_scale.content = (
            Button(text = 'Name' , on_click = lambda : self.window_panel_name(**func)),
            Button(text = 'Position' , on_click = lambda : self.window_panel_position(**func)) ,
            Button(text = 'Rotation' , on_click = lambda : self.window_panel_rotation(**func)) ,
            Text('Scale X :'),
            desimal_inputfield(name='Scale_x' , default_value=str(0.0) , limit_content_to='-+.0123456789') , 
            Text('Scale Y :'),
            desimal_inputfield(name='Scale_y' , default_value=str(0.0) , limit_content_to='-+.0123456789') ,
            Text('Scale Z :'),
            desimal_inputfield(name='Scale_z' , default_value=str(0.0) , limit_content_to='-+.0123456789') ,
            Button('Color' , on_click = lambda : self.window_panel_color(**func))
        )
        self.panel_scale.layout()
        self.panel_scale.y = self.panel_scale.panel.scale_y / 2 * self.panel_scale.scale_y
        self.panel_scale.x = 0.6

        self.panel_scale.content[4].on_value_changed = lambda: func['func_scale_x'](float(self.panel_scale.content[4].value))
        self.panel_scale.content[4].text = str(func['obj'].scale_x)
        self.panel_scale.content[6].on_value_changed = lambda: func['func_scale_y'](float(self.panel_scale.content[6].value))
        self.panel_scale.content[6].text = str(func['obj'].scale_y)
        self.panel_scale.content[8].on_value_changed = lambda: func['func_scale_z'](float(self.panel_scale.content[8].value))
        self.panel_scale.content[8].text = str(func['obj'].scale_z)
    
    def window_panel_color(self , **func):
        self.hide_panels()
        self.panel_color = WindowPanel('Color')
        self.panel_color.content = (
        Button(text = 'Name' , on_click = lambda : self.window_panel_name(**func)) ,
        Button(text="Set transform" , on_click = lambda : self.window_panel_position(**func)) ,
        ColorPicker()
        )
        self.panel_color.layout()
        self.panel_color.y = self.panel_color.panel.scale_y / 2 * self.panel_color.scale_y
        self.panel_color.x = 0.6

        self.panel_color.content[-1].on_value_changed = lambda : func['func_color'](self.panel_color.content[-1].value)
        self.panel_color.content[-1].value = func['obj'].color

    def hide_panels(self):
        destroy(self.panel_name)
        destroy(self.panel_position)
        destroy(self.panel_color)
        destroy(self.panel_rotation)
        destroy(self.panel_scale)
    
    def Field_pos_x(self):
        return self.panel_transform.content

class create_entity(Entity , parent_panel):
    # متغیر کلاس برای نگهداری Entity انتخاب شده
    selected_entity = None
    def __init__(self, add_to_scene_entities=True, enabled=True , **kwargs):
        super().__init__(add_to_scene_entities, enabled, **kwargs)
        parent_panel.__init__(self)
        self.name_panel = None
        # متغیرهای وضعیت انتخاب
        self.is_selected = False
        
        # ایجاد گروه گیزموها
        self.group_gismo = Entity()
        
        # ایجاد گیزموها
        self.x_gis = Entity(
            model='cube', 
            scale=Vec3(10, 0.1, 0.1), 
            color=color.red,
            parent=self.group_gismo
        )
        self.y_gis = Entity(
            model='cube', 
            scale=Vec3(0.1, 10, 0.1), 
            color=color.green,
            parent=self.group_gismo
        )
        self.z_gis = Entity(
            model='cube', 
            scale=Vec3(0.1, 0.1, 10), 
            color=color.blue,
            parent=self.group_gismo
        )
        
        # اضافه کردن collider به گیزموها
        self.x_gis.collider = 'box'
        self.y_gis.collider = 'box'
        self.z_gis.collider = 'box'
        
        # مخفی کردن گیزموها در ابتدا
        self.group_gismo.enabled = False

        # متغیرهای وضعیت درگ
        self.is_dragging = False
        self.drag_axis = None
        self.last_mouse_position = None
        
        # ایجاد جسم اصلی (خود Entity)
        self.model = 'cube'
        self.color = color.white
        self.scale = 0.5
        self.collider = 'box'  # برای تشخیص کلیک روی خود Entity
        
        # اتصال رویدادهای کلیک روی گیزموها
        self.x_gis.on_click = self.start_drag_x
        self.y_gis.on_click = self.start_drag_y
        self.z_gis.on_click = self.start_drag_z
        
        # اتصال رویداد کلیک روی خود Entity
        self.on_click = self.toggle_selection
        self.add_child_menu = DropdownMenu('Add child' , buttons=create_menus('Menus/3_Entity/2_3D entity') , parent = camera.ui , enabled = False)
        print(f"menu ===> {create_menus('Menus/3_Entity/2_3D entity')}")
        #self.add_child_menu = None
    
    def set_name(self , entity_name):
        try:
            self.name = entity_name
            print(f'Name ==> {self.name}')
        except Exception as e:
            pass

    def set_color(self , v):
        try:
            self.color = v
            print(f'Color : {self.color}')
        except Exception as e:
            pass
    
    def set_scale_x(self , x):
        try:
            self.scale_x = x
            print(f'scale x seted : {self.scale_x}')
        except Exception as e:
            pass
    
    def set_scale_y(self , y):
        try:
            self.scale_y = y
            print(f'scale x seted : {self.scale_y}')
        except Exception as e:
            pass
    
    def set_scale_z(self , z):
        try:
            self.scale_z = z
            print(f'scale x seted : {self.scale_z}')
        except Exception as e:
            pass

    def set_rot_x(self , x):
        try:
            self.rotation_x = x
            print(f'rot x seted : {self.rotation_x}')
        except Exception as e:
            pass
    
    def set_rot_y(self , y):
        try:
            self.rotation_y = y
            print(f'rot y seted : {self.rotation_y}')
        except Exception as e:
            pass
    
    def set_rot_z(self , z):
        try:
            self.rotation_z = z
            print(f'rot z seted : {self.rotation_z}')
        except Exception as e:
            pass

    def set_pos_x(self , x):
        try:
            self.position = (x , self.y , self.z)
            print(f'pos x seted : {self.position}')
        except Exception as e:
            pass
    
    
    def set_pos_y(self , y):
        try:
            self.position = (self.x , y , self.z)
            print(f'pos x seted : {self.position}')
        except Exception as e:
            pass
    
    
    def set_pos_z(self , z):
        try:
            self.position = (self.x , self.y , z)
            print(f'pos x seted : {self.position}')
        except Exception as e:
            pass

    def toggle_selection(self):
        """تغییر وضعیت انتخاب"""
        if self.is_selected:
            self.deselect()
        else:
            self.select()

    def select(self):
        """انتخاب Entity و Deselect کردن سایرین"""
        # اگر Entity دیگری انتخاب شده است، آن را Deselect کن
        if create_entity.selected_entity is not None and create_entity.selected_entity != self:
            create_entity.selected_entity.deselect()
        
        # انتخاب این Entity
        self.is_selected = True
        self.group_gismo.enabled = True  # نمایش گیزموها
        create_entity.selected_entity = self  # ذخیره به عنوان Entity انتخاب شده
        print(f"Entity {self} selected")
        self.window_panel_name(
            func_pos_x = self.set_pos_x ,
            func_pos_y = self.set_pos_y , 
            func_pos_z = self.set_pos_z ,
            func_rot_x = self.set_rot_x ,
            func_rot_y = self.set_rot_y ,
            func_rot_z = self.set_rot_z ,
            func_scale_x = self.set_scale_x ,
            func_scale_y = self.set_scale_y ,
            func_scale_z = self.set_scale_z ,
            func_color = self.set_color ,
            func_name = self.set_name ,
            obj = self
            )

    def deselect(self):
        """عدم انتخاب Entity"""
        self.is_selected = False
        self.group_gismo.enabled = False  # مخفی کردن گیزموها
        
        # غیرفعال کردن حالت درگ اگر فعال بود
        if self.is_dragging:
            self.is_dragging = False
            self.drag_axis = None
            self.last_mouse_position = None
        
        # اگر این Entity همان Entity انتخاب شده در کلاس است، آن را پاک کن
        if create_entity.selected_entity == self:
            create_entity.selected_entity = None
        self.hide_panels()
        print(f"Entity {self} deselected")

    def start_drag_x(self):
        """شروع کشیدن در محور X"""
        if self.is_selected and not self.is_dragging:
            self.is_dragging = True
            self.drag_axis = 'x'
            self.last_mouse_position = mouse.position
            print("Start dragging on X axis")

    def start_drag_y(self):
        """شروع کشیدن در محور Y"""
        if self.is_selected and not self.is_dragging:
            self.is_dragging = True
            self.drag_axis = 'y'
            self.last_mouse_position = mouse.position
            print("Start dragging on Y axis")

    def start_drag_z(self):
        """شروع کشیدن در محور Z"""
        if self.is_selected and not self.is_dragging:
            self.is_dragging = True
            self.drag_axis = 'z'
            self.last_mouse_position = mouse.position
            print("Start dragging on Z axis")

    def input(self, key):
        """مدیریت ورودی‌ها"""
        if key == 'left mouse down':
            # اگر کلیک روی گیزمو نبود، هیچ کاری نکن
            pass
            
        elif key == 'left mouse up':
            # وقتی دکمه چپ موس رها می‌شود
            if self.is_dragging:
                self.is_dragging = False
                self.drag_axis = None
                self.last_mouse_position = None
                print("Position changed")
        # بررسی کلیک راست روی این Entity
        if key == 'right mouse down' and mouse.hovered_entity == self:
            self.show_menu_childe()
        # بررسی کلیک در جای دیگر (چپ یا راست)
        elif key in ('left mouse down', 'right mouse down') and mouse.hovered_entity != self:
            self.hide_menu_childe()
    
    def show_menu_childe(self):
        self.add_child_menu.enabled = True
        self.add_child_menu.position = mouse.position
        #Sort_menus(self.child_menu())
        print(f'show menu ==> {self.add_child_menu}' )
    
    def hide_menu_childe(self):
        if self.add_child_menu :
            self.add_child_menu.enabled = False
            #self.add_child_menu = None
        else :
            pass
        print('hide menu')

    def update(self):
        """به‌روزرسانی هر فریم"""
        # همگام‌سازی موقعیت گیزموها با Entity
        self.group_gismo.position = self.position
        
        if self.is_dragging and self.last_mouse_position is not None:
            # محاسبه حرکت موس نسبت به موقعیت قبلی
            mouse_delta = mouse.position - self.last_mouse_position
            move_speed = 3  # سرعت حرکت
            
            if self.drag_axis == 'x':
                # حرکت در محور X
                self.x += mouse_delta.x * move_speed
                if self.panel_position != None and self.panel_position:
                    self.panel_position.content[2].text = str(self.x)
                    
            elif self.drag_axis == 'y':
                # حرکت در محور Y
                self.y += mouse_delta.y * move_speed
                if self.panel_position != None and self.panel_position:
                    self.panel_position.content[4].text = str(self.y)
                    
            elif self.drag_axis == 'z':
                # حرکت در محور Z
                self.z += mouse_delta.x * move_speed
                if self.panel_position != None and self.panel_position:
                    self.panel_position.content[6].text = str(self.z)
            
            # به‌روزرسانی موقعیت آخرین موس
            self.last_mouse_position = mouse.position

# # ایجاد نمونه
# test = create_entity(position=(0, 0, 0))
# test2 = create_entity(position=(2, 0, 0))
# test3 = create_entity(position=(-2, 0, 0))
# test4 = create_entity(position=(0, 0, 2))
# test5 = create_entity(position=(0, 0, -2))

# # اضافه کردن زمین برای سهولت در دید


# # تنظیم دوربین
# camera.position = (5, 5, 5)
# camera.look_at(Vec3(0, 0, 0))

# # اضافه کردن راهنما
# def input(key):
#     if key == 'escape':
#         # Deselect همه
#         if create_entity.selected_entity is not None:
#             create_entity.selected_entity.deselect()

# print("Controls:")
# print("- Click on an entity to select it (only one can be selected at a time)")
# print("- Click on selected entity again to deselect it")
# print("- When selected, click and drag on red/green/blue gizmo to move")
# print("- Press ESC to deselect all")

# app.run()