# from ursina import Entity, Slider, color, Button, camera, Quad, copy, Color


# class ColorPicker(Entity):
#     default_values = dict(parent=camera.ui)

#     def __init__(self, dynamic=True, show_exit_button=False, **kwargs):
#         super().__init__(**(__class__.default_values | kwargs))

#         self.bg = Entity(parent=self, z=.01, model=Quad(aspect=.5/.2), scale=[.5,.225], origin=[0,.5], color=color.black66)
#         self.h_slider = Slider(parent=self, max=360, step=1, dynamic=dynamic, on_value_changed=self._calculate_color)
#         self.h_slider.bg.texture = 'rainbow'

#         self.s_slider = Slider(parent=self, max=100, step=1, dynamic=dynamic, on_value_changed=self._calculate_color)
#         self.s_slider.overlay = Entity(parent=self.s_slider.bg, model=copy(self.s_slider.bg.model), z=-.01, texture='horizontal_gradient', color=color.gray)

#         self.v_slider = Slider(parent=self, max=100, step=1, dynamic=dynamic, on_value_changed=self._calculate_color)
#         self.v_slider.bg.color = color.black
#         self.v_slider.overlay = Entity(parent=self.v_slider.bg, model=copy(self.s_slider.bg.model), z=-.01, texture='horizontal_gradient', color=color.black)

#         self.a_slider = Slider(parent=self, max=100, default=100, step=1, dynamic=dynamic, on_value_changed=self._calculate_color)

#         self.on_value_changed = None    # assign a function here

#         for i, slider in enumerate((self.h_slider, self.s_slider, self.v_slider, self.a_slider)):
#             slider.knob.model.mode = 'line'
#             slider.knob.model.thickness = 2
#             slider.knob.model.generate()
#             slider.knob.color = color.white
#             slider.bg.color = color.white
#             slider.y = -.05 - (i*.03)
#             slider.scale = .8
#             slider.x = -.25+.05

#         self.preview = Button(parent=self, scale=(.5*.84,.05), origin=[0,.5], y=slider.y-.02, color=color.white)
#         self.exit_button = Button(parent=self, scale=.05, position=(.25-.01,-.01), model='circle', color=color.red.tint(-.25), text='x', on_click=self.disable, enabled=show_exit_button)
#         self._calculate_color()

#         for key, value in kwargs.items():
#             setattr(self, key, value)

#     @property
#     def value(self):
#         return color.hsv(self.h_slider.value, self.s_slider.value/100, self.v_slider.value/100, self.a_slider.value/100)

#     @value.setter
#     def value(self, value:Color):
#         value = value.hsv
#         self.h_slider.value = value[0]
#         self.s_slider.value = value[1]*100
#         self.v_slider.value = value[2]*100
#         self.a_slider.value = value[3]*100


#     def _calculate_color(self):
#         self.color = color.hsv(self.h_slider.value, self.s_slider.value/100, self.v_slider.value/100, self.a_slider.value/100)
#         self.preview.color = self.color
#         self.preview.highlight_color = self.color
#         self.preview.pressed_color = self.color
#         self.s_slider.bg.color = color.hsv(self.h_slider.value, 1, 1)
#         # self.s_slider.overlay.color = color.hsv(self.h_slider.value, self.s_slider.value/100, 1)
#         # self.v_slider.bg.color = color.hsv(self.h_slider.value, self.s_slider.value/100, 1)

#         if self.on_value_changed:
#             self.on_value_changed()


# if __name__ == '__main__':
#     from ursina import Ursina
#     app = Ursina()
#     ColorPicker()

#     app.run()

# from ursina import *
# app = Ursina()

# box = Entity(model='cube', origin_y=-.5, scale=1, color=color.orange)

# def scale_box():
#     box.scale_y = slider.value
#     print(thin_slider.value)

# slider = Slider(0, 20, default=10, height=Text.size*3, y=-.4, step=1, on_value_changed=scale_box, vertical=True)

# thin_slider = ThinSlider(text='height', dynamic=True, on_value_changed=scale_box)

# thin_slider.label.origin = (0,0)
# thin_slider.label.position = (.25, -.1)

# app.run()
#####################################################
# from ursina import *

# def spinBox_buttons_func(field: InputField, increas_mode=True):
#     if field.text == '':
#         field.text = '0'
#     value = int(field.text) + 1 if increas_mode else int(field.text) - 1
#     field.text = str(value)

# class SpinBox(Entity):
#     def __init__(self , scale_x = None , scale_y = None):
#         super().__init__()

#         self.field_scale_x = 0.4 if scale_x == None else float(scale_x * 0.4)
#         self.field_scale_y = 0.8 if scale_y == None else float(scale_y * 0.8)
#         self.btn_width = self.field_scale_x / 2
#         self.btn_height = self.field_scale_y / 1.6
        
#         self.Field = InputField(default_value='0' , limit_content_to='-+0123456789', scale=(self.field_scale_x, self.field_scale_y))

#         # دریافت ابعاد واقعی
#         self.field_height = self.Field.get_scale().y
#         self.field_width = self.Field.get_scale().x

#         self.increas_btn = Button(
#             model='quad',
#             parent=self.Field,
#             text='+',
#             position=(0.62, (self.btn_height/2) + 0.05),
#             scale=(self.btn_width, self.btn_height),
#             on_click=lambda: spinBox_buttons_func(self.Field)
#         )

#         self.decreas_btn = Button(
#             model='quad',
#             parent=self.Field,
#             text='-',
#             position=(0.62, (-self.btn_height/2) - 0.05),
#             scale=(self.btn_width, self.btn_height),
#             on_click=lambda: spinBox_buttons_func(self.Field, increas_mode=False)
#         )

# app = Ursina()

# SpinBox()

# app.run()

c = 0

b= []

for i in range(3):
    b.append(c)
    c += 1

print (b)