from ursina import *
from ursina.prefabs.button import Button

class TreeButton:
    def __init__(self, text='', position=(0,0,0), parent_node=None,
                 color=color.azure, text_color=color.white,
                 scale=(0.3, 0.05), expandable=True , job = None):

        self.text = text
        self.position = position
        self.parent_node = parent_node   # 👈 والد درختی
        self.color = color
        self.text_color = text_color
        self.scale = scale
        self.expandable = expandable
        self.job = job
        self.expanded = False
        self.children = []
        self.button = None
        self.toggle_button = None
        self.level = 0
        self.is_hidden = False

        # اگر والد درختی دارد، سطح را از روی آن حساب کن
        if self.parent_node is not None:
            self.level = self.parent_node.level + 1

        # ایجاد دکمه اصلی
        self.create_button()

        # ثبت این دکمه در والد درختی
        if self.parent_node is not None:
            self.parent_node.register_child(self)
            
    def register_child(self, child):
        """ثبت فرزند در والد برای مدیریت موقعیت"""
        if child not in self.children:
            self.children.append(child)
            
    def create_button(self):
        # محاسبه موقعیت بر اساس سطح
        x_offset = self.level * 0.05
        pos = (self.position[0] + x_offset, self.position[1], self.position[2])

        # والد گرافیکی: اگر ریشه است → camera.ui
        # اگر فرزند است → دکمه‌ی والدش
        
        ui_parent = camera.ui 

        self.button = Button(
            text=self.text,
            position=pos,
            color=self.color,
            text_color=self.text_color,
            scale=self.scale,
            parent=ui_parent
        )

        if self.expandable:
            self.create_toggle_button()

        self.button.on_click = self.on_click
        
    def create_toggle_button(self):
        """ایجاد دکمه کوچک برای expand/collapse"""
        # محاسبه موقعیت دکمه toggle
        toggle_pos = (
            self.button.x - self.button.scale_x/2 - 0.025,
            self.button.y,
            self.button.z
        )
        
        self.toggle_button = Button(
            text='+',
            position=toggle_pos,
            color=color.gray,
            text_color=color.white,
            scale=(0.025, 0.025),
            parent=camera.ui
        )
        
        # event handler برای toggle
        self.toggle_button.on_click = self.toggle_expand
        
    def toggle_expand(self):
        """تغییر وضعیت expand/collapse"""
        if self.expanded:
            self.collapse()
        else:
            self.expand()
            
    def expand(self):
        """گسترش دادن دکمه و نمایش فرزندان"""
        if not self.expandable:
            return
            
        self.expanded = True
        if self.toggle_button:
            self.toggle_button.text = '-'
            
        # نمایش همه فرزندان
        for child in self.children:
            child.show()
            
        # به‌روزرسانی موقعیت تمام دکمه‌های بعدی
        self.update_positions()
            
    def collapse(self):
        """جمع کردن دکمه و مخفی کردن فرزندان"""
        if not self.expandable:
            return
            
        self.expanded = False
        if self.toggle_button:
            self.toggle_button.text = '+'
            
        # مخفی کردن همه فرزندان
        for child in self.children:
            child.hide()
            
        # به‌روزرسانی موقعیت تمام دکمه‌های بعدی
        self.update_positions()
            
    def add_child(self, text, color=None , new_job = None):
        if color is None:
            color = color.rgb(0.3, 0.6, 0.9)

        child = TreeButton(
            text=text,
            position=(self.position[0], self.position[1] - 0.06, self.position[2]),
            parent_node=self,          # 👈 والد درختی
            color=color,
            text_color=self.text_color,
            scale= self.scale , #(self.scale[0] * 0.9, self.scale[1] * 0.9),
            expandable=True
        )
        if new_job:
            child.job = new_job

        # اینجا register_child در __init انجام شده، ولی اگر خواستی:
        # self.register_child(child)

        if not self.expanded:
            child.hide()

        self.update_positions()
        return child
    
    def get_visible_children(self):
        """دریافت فرزندانی که قابل مشاهده هستند"""
        visible = []
        for child in self.children:
            if not child.is_hidden and child.button.visible:
                visible.append(child)
        return visible
        
    def get_linear_tree(self):
        """
        ساخت یک لیست خطی از کل درخت به ترتیب نمایش
        """
        result = [self]
        if self.expanded:
            for child in self.children:
                if not child.is_hidden:
                    result.extend(child.get_linear_tree())
        return result


    def update_positions(self):
        # پیدا کردن ریشه
        root = self
        while root.parent_node is not None:
            root = root.parent_node

        ordered = root.get_linear_tree()

        current_y = root.position[1]
        spacing = 0.065

        for btn in ordered:

            # --- تنظیم Y ---
            btn.button.y = current_y
            if btn.toggle_button:
                btn.toggle_button.y = current_y

            # --- تنظیم X بر اساس level ---
            x_offset = btn.level * 0.05
            btn.button.x = root.position[0] + x_offset

            # --- تنظیم X دکمه toggle ---
            if btn.toggle_button:
                btn.toggle_button.x = btn.button.x - btn.button.scale_x/2 - 0.025

            current_y -= spacing
                
    def get_all_visible_buttons(self):
        """دریافت تمام دکمه‌های قابل مشاهده در کل درخت"""
        buttons = []
        if self.button.visible and not self.is_hidden:
            buttons.append(self)
            if self.expanded:
                for child in self.children:
                    buttons.extend(child.get_all_visible_buttons())
        return buttons
        
    def on_click(self):
        """عملیات هنگام کلیک روی دکمه"""
        print(f"Clicked: {self.text}")
        if self.job:
            self.job()
        
    def hide(self):
        self.is_hidden = True
        self.button.visible = False
        if self.toggle_button:
            self.toggle_button.visible = False
        for child in self.children:
            child.hide()

        self.update_positions()


    def show(self):
        self.is_hidden = False
        self.button.visible = True
        if self.toggle_button:
            self.toggle_button.visible = True

        if self.expanded:
            for child in self.children:
                child.show()

        self.update_positions()
                
    # def remove(self):
    #     """حذف کامل دکمه و فرزندان"""
    #     destroy(self.button)
    #     if self.toggle_button:
    #         destroy(self.toggle_button)
    #     for child in self.children:
    #         child.remove()
    #     self.children.clear()
    #     self.update_positions()
    def remove(self):
        """حذف کامل دکمه و فرزندان"""
        # ذخیره والد برای استفاده بعدی
        parent = self.parent_node
        
        # ابتدا همه فرزندان را حذف کن
        for child in self.children[:]:  # از کپی لیست استفاده کن
            child.remove()
        
        # حالا لیست فرزندان را پاک کن
        self.children.clear()
        
        # حذف دکمه toggle اگر وجود دارد
        if self.toggle_button:
            if hasattr(self.toggle_button, 'parent') and self.toggle_button.parent:
                self.toggle_button.parent = None
            destroy(self.toggle_button)
            self.toggle_button = None
        
        # حذف دکمه اصلی
        if self.button:
            if hasattr(self.button, 'parent') and self.button.parent:
                self.button.parent = None
            destroy(self.button)
            self.button = None
        
        # اگر این دکمه فرزند است، از لیست فرزندان والد حذف کن
        if parent:
            if self in parent.children:
                parent.children.remove(self)
        
        # به‌روزرسانی موقعیت‌ها از ریشه
        root = parent
        while root and root.parent_node is not None:
            root = root.parent_node
        
        if root:
            root.update_positions()

app = Ursina()

entity_buttons = TreeButton(
            text='Scene',
            position=(-0.67, 0.4, 0),
            color=color.rgb(0.2, 0.4, 0.6),
            scale= (0.3 , 0.05) #(0.4, 0.06)
        )

# test = TreeButton(
#             text='Root',
#             position=(0, 0.4, 0),
#             color=color.rgb(0.2, 0.4, 0.6),
#             scale=(0.4, 0.06),
#             job=lambda : print('hello')
#         )

# child1 = test.add_child('Child 1', color=color.rgb(0.3, 0.6, 0.8) , new_job=lambda : print('hello world'))
# grandchild1 = child1.add_child('Grandchild 1.1', color=color.rgb(0.4, 0.7, 0.9))

# app.run()