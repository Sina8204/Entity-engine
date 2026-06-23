# def on_mouse_enter(self):
#     # تغییر ظاهر هنگام هاور
#     #self.color = color.rgb(200, 200, 255)
#     pass
    
# def on_mouse_exit(self):
#     # بازگرداندن ظاهر عادی
#     #self.color = color.white
#     # اگر ماوس خارج شد و در حال کشیدن بودیم، کشیدن را متوقف کن
#     if self.is_dragging:
#         self.is_dragging = False
    
# def on_click(self):
#     # کلیک چپ: شروع کشیدن
#     if mouse.left:
#         self.is_dragging = True
#         self.last_mouse_x = mouse.x
#         # ذخیره مقدار فعلی برای محاسبات
#         self.drag_start_value = self.numeric_value



from ursina import *

app = Ursina()
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

#t = desimal_inputfield()

e = Entity(model = 'cube' , color = color.red)
e.scale_x = 10
print(e.scale_x)

def set_color(v):
    e.color = v
col = ColorPicker()
col.value = e.color
col.on_value_changed = lambda : set_color(col.value) 
app.run()