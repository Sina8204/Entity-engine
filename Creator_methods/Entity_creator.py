from ursina import *
from .UI_classes import ColorPicker
from .UI_classes import PanelManager , menu_creator , execute_file_module , desimal_inputfield , custom_fd , Entity_scripts_args_manager , Sort_menus , catch_menus , ScrollableInputField
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from .tree_button import entity_buttons
from .tree_projects_entity import rename_key_in_tree
from AppData import ProjectData
from .File_browser import Browser
import copy , json , easygui , shutil

ent_script_source = """from ursina import *
class --name--:
    def __init__(self):
        pass
    
    def input(self , key):
        print(f"'{key}' clicked")
    
    def update(self):
        pass"""
#app = Ursina()         

class tree_button():
    def __init__(self):
        pass

class entity_tools(Entity):
    # متغیر کلاس برای نگهداری Entity انتخاب شده
    selected_entity = None
    def __init__(self, add_to_scene_entities=True, enabled=True , **kwargs):
        super().__init__(add_to_scene_entities, enabled , **kwargs)
        self.inspector = PanelManager()
        
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
        self.menu_childs = menu_creator()
        self.get_menu_childes = self.menu_childs.get_buttons_menu('Menus/3_Entity/2_3D entity' , parent = self)
        self.get_menu_childes.append(DropdownMenuButton(text='Destroy' , on_click = self.destroy_WinPanel))
        self.add_child_menu = DropdownMenu('Add child or destroy' , buttons=self.get_menu_childes , parent = camera.ui , enabled = False)

        self.destroy_window = None
        self.select_button = None

        self.details_entity = None
    
    def destroy_WinPanel(self):
        self.destroy_window = WindowPanel(title = 'Destroy entity', content=(
            Text(f'Are you sure to destroy {self.name} entity') ,
            Button(text='Destroy') ,
            Button(text='Cancel')
        ))
        self.destroy_window.y = self.destroy_window.panel.scale_y / 2 * self.destroy_window.scale_y    # center the window panel
        self.destroy_window.layout()
        self.destroy_window.content[-1].on_click = lambda : destroy(self.destroy_window)
        self.destroy_window.content[-2].on_click = self.destroy_entity
    
    def destroy_entity(self):
        ProjectData.remove_entity(self.name)
        destroy(self)
        destroy(self.group_gismo)
        self.inspector.destroy_panels()
        destroy(self.destroy_window)
        destroy(self.add_child_menu)
        for i in self.get_menu_childes:
            destroy(i)
        if self.select_button:
            self.select_button.remove()
        get_win_panel = [win_panel for win_panel in scene.entities if type(win_panel) is WindowPanel]
        for win_panel in get_win_panel:
            print(f"Removing {win_panel.name}")
            destroy(win_panel)

    def set_name(self):
        try:
            entity_name = self.inspector.get_widget_value(
                Panel_name = 'name' , 
                widget_name = 'name_field' , 
                widget_class = InputField ,
                attr='text')
            entity_name = entity_name if entity_name not in ProjectData.data["__names__"] else f"New_{entity_name}"
            current_name = self.name
            self.name = entity_name
            self.select_button.button.text = self.name
            ProjectData.rename_key(current_name , self.name)
            print(f'Name ==> {self.name}')
        except Exception as e:
            pass

    def set_color(self):
        try:
            self.color = self.inspector.get_widget_value(
                Panel_name = 'Color' , 
                widget_name = 'color_value' , 
                widget_class = ColorPicker ,
                attr='value')
            ProjectData.set_value(self.name , "color" , tuple(self.color))
            print(f'Color : {self.color}')
        except Exception as e:
            pass
    
    def set_scale_x(self):
        try:
            self.scale_x = self.inspector.get_widget_value(
                Panel_name = 'Scale' , 
                widget_name = 'Scale_x' , 
                widget_class = desimal_inputfield ,
                attr='value')
            ProjectData.set_value(self.name , "scale" , tuple(self.scale))
            print(f'scale x seted : {self.scale_x}')
        except Exception as e:
            pass
    
    def set_scale_y(self):
        try:
            self.scale_y = self.inspector.get_widget_value(
                Panel_name = 'Scale' , 
                widget_name = 'Scale_y' , 
                widget_class = desimal_inputfield ,
                attr='value')
            ProjectData.set_value(self.name , "scale" , tuple(self.scale))
            print(f'scale x seted : {self.scale_y}')
        except Exception as e:
            pass
    
    def set_scale_z(self):
        try:
            self.scale_z = self.inspector.get_widget_value(
                Panel_name = 'Scale' , 
                widget_name = 'Scale_z' , 
                widget_class = desimal_inputfield ,
                attr='value')
            print(f'scale x seted : {self.scale_z}')
            ProjectData.set_value(self.name , "scale" , tuple(self.scale))
        except Exception as e:
            pass

    def set_rot_x(self):
        try:
            self.rotation_x = self.inspector.get_widget_value(
                Panel_name = 'Rotation' , 
                widget_name = 'Rotation_x' , 
                widget_class = desimal_inputfield ,
                attr='value')
            ProjectData.set_value(self.name , "rotation" , tuple(self.rotation))
            print(f'rot x seted : {self.rotation_x}')
        except Exception as e:
            pass
    
    def set_rot_y(self):
        try:
            self.rotation_y = self.inspector.get_widget_value(
                Panel_name = 'Rotation' , 
                widget_name = 'Rotation_y' , 
                widget_class = desimal_inputfield ,
                attr='value')
            ProjectData.set_value(self.name , "rotation" , tuple(self.rotation))
            print(f'rot y seted : {self.rotation_y}')
        except Exception as e:
            pass
    
    def set_rot_z(self):
        try:
            self.rotation_z = self.inspector.get_widget_value(
                Panel_name = 'Rotation' , 
                widget_name = 'Rotation_z' , 
                widget_class = desimal_inputfield ,
                attr='value')
            ProjectData.set_value(self.name , "rotation" , tuple(self.rotation))
            print(f'rot z seted : {self.rotation_z}')
        except Exception as e:
            pass

    def set_pos_x(self):
        try:
            x = self.inspector.get_widget_value(
                Panel_name = 'Position' , 
                widget_name = 'Position_x' , 
                widget_class = desimal_inputfield ,
                attr='value')
            self.position = (x , self.y , self.z)
            ProjectData.set_value(self.name , "position" , tuple(self.position))
            print(f'pos x seted : {self.position}')
        except Exception as e:
            pass
    
    
    def set_pos_y(self):
        try:
            y = self.inspector.get_widget_value(
                Panel_name = 'Position' , 
                widget_name = 'Position_y' , 
                widget_class = desimal_inputfield ,
                attr='value')
            self.position = (self.x , y , self.z)
            ProjectData.set_value(self.name , "position" , tuple(self.position))
            print(f'pos x seted : {self.position}')
        except Exception as e:
            pass
    
    
    def set_pos_z(self):
        try:
            z = self.inspector.get_widget_value(
                Panel_name = 'Position' , 
                widget_name = 'Position_z' , 
                widget_class = desimal_inputfield ,
                attr='value')
            self.position = (self.x , self.y , z)
            ProjectData.set_value(self.name , "position" , tuple(self.position))
            print(f'pos x seted : {self.position}')
        except Exception as e:
            pass
    
    def make_script(self):
        if not Browser.project_path :
            custom_fd.show_msg('warnning' , box_title='Field at create script' , msg = 'Create or open a project before creating script')
            return
        script_path = custom_fd.asksaveasfilename_box(title = "Make script" , msg = "Select a path and a name for the script" , filetypes=[("Python file" , "*.py")] , defult_path = f'{Browser.project_path}/{Browser.assets_folder_name}')
        if script_path is None :
            return
        
        scr_class_name = script_path["name"].replace(".", "_")
        scr_path = script_path["path"]

        if not os.path.exists(scr_path):
            with open (scr_path , "w+" , encoding = "utf-8") as script:
                script.write(ent_script_source.replace("--name--", scr_class_name))
        
        print(f"Created script : \n\tpath : '{scr_path}'\n\tname : '{scr_class_name}'")
        script_dict = {
            "name" : str(scr_class_name) , 
            "source_path" : scr_path , 
            "args" : () , 
            "kwargs" : {}
            }
        self.details_entity.update({"script" : script_dict})
        ProjectData.set_value(self.name , 'script' , script_dict)
        print(self.details_entity["script"])


    def add_attrs_to_ent_script(self):
        if self.details_entity["script"] is None:
            custom_fd.show_msg(type = 'warnning' , box_title = "Unknown script" , msg = "First create a script.")
            return
        if not os.path.exists(self.details_entity["script"]["source_path"]):
            path = self.details_entity["script"]["source_path"]
            custom_fd.show_msg(type = 'error' , box_title = "Script path not found" , msg = f"The path you selected is not found : \n\t'{path}'\nMake a new script")
            return
        args_manager = Entity_scripts_args_manager(args = self.details_entity["script"]["args"] , kwargs = self.details_entity["script"]["kwargs"])
        args_manager.mainloop()
        args = args_manager()['args']
        kwargs = args_manager()['kwargs']
        self.details_entity["script"]["args"] = args
        self.details_entity["script"]["kwargs"] = kwargs
        ProjectData.set_value(self.name , 'script' , self.details_entity["script"])

    def set_texture(self):
        texture_path = custom_fd.openfile(title="texture path" , msg="Select texture" , defult_path=f'{Browser.project_path}/{Browser.assets_folder_name}')
        if os.path.exists(str(texture_path)):
            if texture_path.startswith(f"{Browser.project_path}/{Browser.assets_folder_name}"):
                shutil.copyfile(texture_path , f"{Browser.project_path}/Source/__{Browser.assets_folder_name}/{os.path.basename(texture_path)}")
                texture_path = texture_path.replace(f"{Browser.project_path}/{Browser.assets_folder_name}", '')
                self.texture = load_texture(texture_path)
                ProjectData.set_value(self.name , 'texture' , texture_path)
        print(f"Texture path : {texture_path}")
        print(f"Project path : {Browser.project_path}/{Browser.assets_folder_name}")

        

    def toggle_selection(self):
        """تغییر وضعیت انتخاب"""
        if self.is_selected:
            self.deselect()
        else:
            self.select()

    def select(self):
        """انتخاب Entity و Deselect کردن سایرین"""
        # اگر Entity دیگری انتخاب شده است، آن را Deselect کن
        try:
            if entity_tools.selected_entity is not None and entity_tools.selected_entity != self:
                entity_tools.selected_entity.deselect()
        except Exception as e:
            pass
        
        # انتخاب این Entity
        self.is_selected = True
        self.group_gismo.enabled = True  # نمایش گیزموها
        entity_tools.selected_entity = self  # ذخیره به عنوان Entity انتخاب شده
        print(f"Entity {self} selected")
        self._creat_panel()
        self.inspector.enabel_panel('name')

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
        if entity_tools.selected_entity == self:
            entity_tools.selected_entity = None
        self.inspector.destroy_panels()
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
        elif key in ('left mouse down', 'right mouse down') : #and mouse.hovered_entity != self:
            self.hide_menu_childe()
    
    def show_menu_childe(self):
        self.add_child_menu.enabled = True
        self.add_child_menu.position = mouse.position
        #Sort_menus(self.child_menu())
        print(f'show menu ==> {self.add_child_menu}' )
    
    def hide_menu_childe(self):
        if self.add_child_menu :
            self.add_child_menu.enabled = False
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
                #self.x += mouse_delta.x * move_speed
                self.world_x += mouse_delta.x * move_speed
                ProjectData.set_value(self.name , "position" , tuple(self.position))
                self.inspector.set_content_attr(
                    panel_name = 'Position' ,
                    content = ('Position_x' , desimal_inputfield) ,
                    attr = 'text' ,
                    value = str(self.x)
                    )
                # if self.panel_position != None and self.panel_position:
                #     self.panel_position.content[2].text = str(self.x)
                    
            elif self.drag_axis == 'y':
                # حرکت در محور Y
                #self.y += mouse_delta.y * move_speed
                self.world_y += mouse_delta.y * move_speed
                ProjectData.set_value(self.name , "position" , tuple(self.position))
                self.inspector.set_content_attr(
                    panel_name = 'Position' ,
                    content = ('Position_y' , desimal_inputfield) ,
                    attr = 'text' ,
                    value = str(self.y)
                    )
                # if self.panel_position != None and self.panel_position:
                #     self.panel_position.content[4].text = str(self.y)
                    
            elif self.drag_axis == 'z':
                # حرکت در محور Z
                #self.z += mouse_delta.x * move_speed
                self.world_z += mouse_delta.x * move_speed
                ProjectData.set_value(self.name , "position" , tuple(self.position))
                self.inspector.set_content_attr(
                    panel_name = 'Position' ,
                    content = ('Position_z' , desimal_inputfield) ,
                    attr = 'text' ,
                    value = str(self.z)
                    )
                # if self.panel_position != None and self.panel_position:
                #     self.panel_position.content[6].text = str(self.z)
            
            # به‌روزرسانی موقعیت آخرین موس
            self.last_mouse_position = mouse.position
    
    def _creat_panel(self):
        self.inspector.add_panels(
            name = WindowPanel(title="Set name" , content=(
                InputField(name = "name_field") ,
                Button(name = 'panel_transform' , text = "Set transform"),
                Button(name = 'panel_color' , text = "Set color"),
                Button(name = 'panel_texture' , text = "Set texture"),
                Button(name = 'panel_script' , text="Script")
            ) , enabled = False) ,

            Position = WindowPanel(title="Set position" , content=(
                Button(name = 'panel_name' , text = "set name") ,
                Text("Position X:") ,
                desimal_inputfield(name='Position_x' , default_value=str(0.0) , limit_content_to='-+.0123456789') , 
                Text('Position Y :'),
                desimal_inputfield(name='Position_y' , default_value=str(0.0) , limit_content_to='-+.0123456789') ,
                Text('Position Z :'),
                desimal_inputfield(name='Position_z' , default_value=str(0.0) , limit_content_to='-+.0123456789') ,
                Button(name = "panel_rotation" , text = 'Rotation') ,
                Button(name = "panel_scale" , text = 'Scale'),
                Button(name = "panel_color" , text = 'Color'),
                Button(name = 'panel_texture' , text = "Set texture"),
                Button(name = 'panel_script' , text="Script")
            ) , enabled = False) ,

            Rotation = WindowPanel(title="Set Rotation" , content=(
                Button(name = 'panel_name' , text = "set name") ,
                Button(name = 'panel_position' , text = "Position") ,
                Text("Rotation X:") ,
                desimal_inputfield(name='Rotation_x' , default_value=str(0.0) , limit_content_to='-+.0123456789') , 
                Text('Rotation Y :'),
                desimal_inputfield(name='Rotation_y' , default_value=str(0.0) , limit_content_to='-+.0123456789') ,
                Text('Rotation Z :'),
                desimal_inputfield(name='Rotation_z' , default_value=str(0.0) , limit_content_to='-+.0123456789') ,
                Button(name = "panel_scale" , text = 'Scale'),
                Button(name = "panel_color" , text = 'Color'),
                Button(name = 'panel_texture' , text = "Set texture"),
                Button(name = 'panel_script' , text="Script")
            ) , enabled = False) ,

            Scale = WindowPanel(title="Set scale" , content=(
                Button(name = 'panel_name' , text = "set name") ,
                Button(name = 'panel_position' , text = "Position") ,
                Button(name = "panel_rotation" , text = 'Rotation') ,
                Text("Scale X:") ,
                desimal_inputfield(name='Scale_x' , default_value=str(0.0) , limit_content_to='-+.0123456789') , 
                Text('Scale Y :'),
                desimal_inputfield(name='Scale_y' , default_value=str(0.0) , limit_content_to='-+.0123456789') ,
                Text('Scale Z :'),
                desimal_inputfield(name='Scale_z' , default_value=str(0.0) , limit_content_to='-+.0123456789') ,
                Button(name = "panel_color" , text = 'Color') ,
                Button(name = 'panel_texture' , text = "Set texture"),
                Button(name = 'panel_script' , text="Script")
            ) , enabled = False) ,
            Color = WindowPanel(title="Set color" , content=(
                Button(name = 'panel_name' , text = "set name") ,
                Button(name = 'panel_transform' , text = "Set transform"),
                ColorPicker(name = 'color_value') ,
                Button(name = 'panel_texture' , text = "Set texture"),
                Button(name = 'panel_script' , text="Script")
            ) , enabled = False) ,

            Texture_panel = WindowPanel(title="Set texture" , content=(
                Button(name = 'panel_name' , text = "set name") ,
                Button(name = 'panel_transform' , text = "Set transform"),
                Button(name = "panel_color" , text = 'Color'),
                Space(1),
                Button(name = "add_texture" , text="Set texture"),
                Sprite(),
                Space(1),
                Button(name = 'panel_script' , text="Script")
            ) , enabled = False) ,

            Script = WindowPanel(title = "Add script" , content=(
                Button(name = 'panel_name' , text = "set name") ,
                Button(name = 'panel_transform' , text = "Set transform"),
                Button(name = "panel_color" , text = 'Color'),
                Button(name = 'panel_texture' , text = "Set texture"),
                Space(1),
                Button(name = "add_script" , text="Add script") ,
                Button(name = "set_attr" , text='Set attributes')
            ))
        )
        self.inspector.set_position(mode="y_center" , x = 0.6)
        self.inspector.connect_panel_buttons(
                                            panel_name = 'name' , 
                                            panel_transform = 'Position' ,
                                            panel_position = 'Position' ,
                                            panel_rotation = 'Rotation' ,
                                            panel_scale = 'Scale' ,
                                            panel_color = 'Color' ,
                                            panel_script = 'Script' ,
                                            panel_texture = 'Texture_panel'
                                        )
        
        #################### Set text_fields value ####################

        self.inspector.set_content_attr( panel_name = 'name' , content = ('name_field' , InputField) , attr = 'text' , value = self.name)

        self.inspector.set_content_attr( panel_name = 'Position' , content = ('Position_x' , InputField) , attr = 'text' , value = str(self.x))
        self.inspector.set_content_attr( panel_name = 'Position' , content = ('Position_y' , InputField) , attr = 'text' , value = str(self.y))
        self.inspector.set_content_attr( panel_name = 'Position' , content = ('Position_z' , InputField) , attr = 'text' , value = str(self.z))

        self.inspector.set_content_attr( panel_name = 'Rotation' , content = ('Rotation_x' , InputField) , attr = 'text' , value = str(self.rotation_x))
        self.inspector.set_content_attr( panel_name = 'Rotation' , content = ('Rotation_y' , InputField) , attr = 'text' , value = str(self.rotation_y))
        self.inspector.set_content_attr( panel_name = 'Rotation' , content = ('Rotation_z' , InputField) , attr = 'text' , value = str(self.rotation_z))

        self.inspector.set_content_attr( panel_name = 'Scale' , content = ('Scale_x' , InputField) , attr = 'text' , value = str(self.scale_x))
        self.inspector.set_content_attr( panel_name = 'Scale' , content = ('Scale_y' , InputField) , attr = 'text' , value = str(self.scale_y))
        self.inspector.set_content_attr( panel_name = 'Scale' , content = ('Scale_z' , InputField) , attr = 'text' , value = str(self.scale_z))

        self.inspector.set_content_attr( panel_name = 'Color' , content = ('color_value' , ColorPicker) , attr = 'value' , value = self.color)

        #################### Set text_fields value ####################

        #################### Set text_fields events ####################

        self.inspector.set_content_event( panel_name = 'name' , content=('name_field' , InputField) , event='on_value_changed' , handler = self.set_name)
        
        self.inspector.set_content_event( panel_name = 'Position' ,content=('Position_x' , desimal_inputfield) ,event='on_value_changed' ,handler = self.set_pos_x)
        self.inspector.set_content_event( panel_name = 'Position' ,content=('Position_y' , desimal_inputfield) ,event='on_value_changed' ,handler = self.set_pos_y)
        self.inspector.set_content_event( panel_name = 'Position' ,content=('Position_z' , desimal_inputfield) ,event='on_value_changed' ,handler = self.set_pos_z)
        
        self.inspector.set_content_event( panel_name = 'Rotation' ,content=('Rotation_x' , desimal_inputfield) ,event='on_value_changed' ,handler = self.set_rot_x)
        self.inspector.set_content_event( panel_name = 'Rotation' ,content=('Rotation_y' , desimal_inputfield) ,event='on_value_changed' ,handler = self.set_rot_y)
        self.inspector.set_content_event( panel_name = 'Rotation' ,content=('Rotation_z' , desimal_inputfield) ,event='on_value_changed' ,handler = self.set_rot_z)
        
        self.inspector.set_content_event( panel_name = 'Scale' ,content=('Scale_x' , desimal_inputfield) ,event='on_value_changed' ,handler = self.set_scale_x)
        self.inspector.set_content_event( panel_name = 'Scale' ,content=('Scale_y' , desimal_inputfield) ,event='on_value_changed' ,handler = self.set_scale_y)
        self.inspector.set_content_event( panel_name = 'Scale' ,content=('Scale_z' , desimal_inputfield) ,event='on_value_changed' ,handler = self.set_scale_z)
        
        self.inspector.set_content_event( panel_name = 'Color' ,content=('color_value' , ColorPicker) ,event='on_value_changed' ,handler = self.set_color)

        self.inspector.set_content_event( panel_name = 'Texture_panel' , content=('add_texture' , Button) , event='on_click' , handler = self.set_texture)

        self.inspector.set_content_event( panel_name = 'Script' , content=("add_script" , Button) , event="on_click" , handler = self.make_script)
        self.inspector.set_content_event( panel_name = 'Script' , content=("set_attr" , Button) , event="on_click" , handler = self.add_attrs_to_ent_script)

        
        #################### Set text_fields events ####################

class create_entity(entity_tools):
    def __init__(self, 
                 add_to_scene_entities=True, 
                 enabled=True, 
                 model_path = None ,
                 Model = None , 
                 Script = None , 
                 Parent = None, 
                 Name = None , 
                 Color = color.gray , 
                 Position = (0 , 0 , 0) , 
                 Rotation = (0 , 0 , 0) , 
                 Scale = (1 , 1 , 1) ,
                 Texture = None,
                 **kwargs):
        super().__init__(add_to_scene_entities, enabled, **kwargs)
        self.model=Model
        counter = 1
        while (Name in ProjectData.data["__names__"]):
            Name = f"{Name}{counter}"
            counter+=1
        
        self.name = Name if Name else self.name
        self.position = Position
        self.rotation = Rotation
        self.scale = Scale
        self.color= Color
        if Texture and os.path.exists(Texture):
            self.texture = load_texture(Texture)
        #self.scale=(0.5, 0.5, 0.5)
        self.details_entity = {
                "model_path" : model_path if model_path and os.path.exists(model_path) else 'unset path value',
                "model" : f"{Model}" if not Model is None else None,
                "color" : tuple(self.color) ,
                "position" : tuple(self.position) ,
                "rotation" : tuple(self.rotation),
                "scale" : tuple(self.scale),
                "texture" : str(self.texture) ,
                "script" : Script ,
                "children" : {}
        }
        if Parent:
            self.parent = Parent
            #self.scale=(1, 1 , 1)
            self.group_gismo.parent = self.parent
            self.group_gismo.scale = (1 , 1 , 1)
            self.group_gismo.world_rotation = (0 , 0, 0)
            self.select_button = Parent.select_button.add_child(self.name, color=color.rgb(0.3, 0.6, 0.8) , new_job = self.select_button_job)
            print(f'Parent ====> {self.group_gismo.rotation}')
            #details = add_entity_to_dict(self , "Menus/3_Entity/2_3D entity/1_cube.py")
            ProjectData.add_children(self.parent.name , self.name , self.details_entity)
        else:
            self.select_button = entity_buttons.add_child(self.name, color=color.rgb(0.3, 0.6, 0.8) , new_job = self.select_button_job)
            ProjectData.add_entity_to_dict(self , **self.details_entity)
        
        # test = json.dumps(ProjectData.data , ensure_ascii= False , indent=4)
        # print(f'{self.name} entity created ====> {test}')
    
    def select_button_job(self):
        if self.is_selected:
            self.deselect()
        else:
            self.select()
  
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