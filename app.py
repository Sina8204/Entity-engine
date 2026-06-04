from ursina import *


class CameraController(Entity):
    def __init__(self, rotate_speed=80, pan_speed=5, zoom_speed=5):
        super().__init__()

        self.rotate_speed = rotate_speed
        self.pan_speed = pan_speed
        self.zoom_speed = zoom_speed

        # تنظیمات اولیه دوربین
        camera.position = (0, 0, -10)

    def update(self):
        # --- چرخش با غلطک (Middle Mouse) ---
        if mouse.middle and mouse.moving:
            camera.rotation_y -= mouse.velocity.x * self.rotate_speed
            camera.rotation_x -= mouse.velocity.y * self.rotate_speed

        # --- حرکت (Pan) با راست‌کلیک ---
        if mouse.right and mouse.moving:
            right = camera.right
            up    = camera.up

            camera.position += right * mouse.velocity.x * self.pan_speed
            camera.position += up * (-mouse.velocity.y) * self.pan_speed

    def input(self, key):
        # --- زوم با اسکرول ---
        if key == 'scroll up':
            camera.position += camera.forward * self.zoom_speed

        if key == 'scroll down':
            camera.position -= camera.forward * self.zoom_speed



app = Ursina()

# صحنه‌ی تست
ground = Entity(model='plane', scale=20, texture='white_cube', texture_scale=(20, 20))
cube   = Entity(model='cube', color=color.azure, y=1)

# فعال‌سازی کنترلر
controller = CameraController()

app.run()
