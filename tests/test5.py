# from ursina import *

# app = Ursina()

# class desimal_inputfield(InputField):
#     def __init__(self):
#         super().__init__()
#         self.accept = 'numbers'  # فقط اعداد را قبول می‌کند
#         self.text = ''  # مقدار اولیه
#         self.access_change = False  # فلگ دسترسی
#         self.is_hovered = False 
    
#     def input(self , key):
#         if key == 'left mouse down' and self.is_hovered:
#             self.access_change = True
#             print("left click pressed")
#         elif key == 'left mouse up' and self.is_hovered:
#             self.access_change = False
#             print('left click released')
        
    
#     def on_mouse_enter(self):
#         self.is_hovered = True
#         print("mouse entered")
#         return super().on_mouse_enter()

#     def on_mouse_exit(self):
#         self.is_hovered = False
#         print("mouse exited")
#         return super().on_mouse_exit()

# desimal_inputfield()

# app.run()


from ursina import *

app = Ursina()

class desimal_inputfield(InputField):
    def __init__(self):
        super().__init__()
        self.accept = 'numbers'  # فقط اعداد را قبول می‌کند
        self.text = '0.0'  # مقدار اولیه
        self.access_change = False  # فلگ دسترسی
        self.is_hovered = False
        self.mouse_start_x = 0  # موقعیت اولیه موس هنگام کلیک
        self.current_decimal = 0.0  # مقدار اعشار فعلی
    
    def input(self, key):
        if key == 'left mouse down' and self.is_hovered:
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

# ایجاد نمونه از کلاس
decimal_input = desimal_inputfield()
decimal_input.position = (0, 0)  # قرار دادن در مرکز صفحه

app.run()