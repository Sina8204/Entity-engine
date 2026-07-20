from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

app = Ursina()

class MyEntity(Entity):
    def __init__(self):
        super().__init__(
            model='cube',
            color=color.orange,
            scale=2,
            collider='box'
        )
        self.dropdown_menu = None

    def input(self, key):
        # بررسی کلیک راست روی این Entity
        if key == 'right mouse down' and mouse.hovered_entity == self:
            self.show_dropdown()
        # بررسی کلیک در جای دیگر (چپ یا راست)
        elif key in ('left mouse down', 'right mouse down') and mouse.hovered_entity != self:
            self.hide_dropdown()

    def show_dropdown(self):
        # حذف منوی قبلی اگر وجود دارد
        self.hide_dropdown()
        
        # ایجاد منوی جدید در موقعیت ماوس
        self.dropdown_menu = DropdownMenu(
            text='New',
            position=mouse.position,
            parent=camera.ui
        )
        
        # اضافه کردن آیتم‌ها به منو
        for option in ['Option 1', 'Option 2', 'Option 3', 'Exit']:
            button = DropdownMenuButton(text=option, parent=self.dropdown_menu)
            if option == 'Exit':
                button.on_click = Func(print, f'{option} quit')
            else:
                button.on_click = Func(print, f'{option} selected')

        # تنظیم موقعیت منو به صورت نسبی
        self.dropdown_menu.position = mouse.position

    def hide_dropdown(self):
        if self.dropdown_menu:
            destroy(self.dropdown_menu)
            self.dropdown_menu = None

# ایجاد Entity
e = MyEntity()

# برای نمایش بهتر، یک پس‌زمینه اضافه می‌کنیم
Entity(model='quad', scale=100, color=color.white, z=1)

# توضیح در کنسول
print("روی مکعب کلیک راست کنید تا منو ظاهر شود.")
print("برای بستن منو، در جای دیگری از صفحه کلیک کنید.")

app.run()