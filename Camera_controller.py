from ursina import *

class CameraController(Entity):
    def __init__(self, rotate_speed=80, pan_speed=5, zoom_speed=3):
        super().__init__()

        self.rotate_speed = rotate_speed
        self.pan_speed = pan_speed
        self.zoom_speed = zoom_speed

        # تنظیمات اولیه دوربین
        camera.position = (0, 0, -10)

    def update(self):
        # --- چرخش با غلطک (Middle Mouse) ---
        if mouse.middle and mouse.moving:
            camera.rotation_y += mouse.velocity.x * self.rotate_speed
            camera.rotation_x -= mouse.velocity.y * self.rotate_speed
            print(camera.rotation)

        # --- حرکت (Pan) با راست‌کلیک ---
        if mouse.right and mouse.moving:
            right = camera.right
            up    = camera.up

            camera.position += right * mouse.velocity.x * self.pan_speed
            camera.position += up * (-mouse.velocity.y) * self.pan_speed
            print(camera.position)

    def input(self, key):
        # --- زوم با اسکرول ---
        if key == 'scroll up':
            camera.position += camera.forward * self.zoom_speed
            #print(camera.position)

        elif key == 'scroll down':
            camera.position -= camera.forward * self.zoom_speed
            #print(camera.position)
        
        elif key == '1':  # Left view
            camera.position = (0, 0, 20)
            #camera.position = (0, 0, camera.Z)
            camera.rotation = Vec3(0 , 180 , 0)
            #print(f'position ==> {camera.position}\nrotation ==> {camera.rotation}')
            # camera.look_at(cube)  # نگاه به سمت جسم
            
        elif key == '3':  # Right view
            camera.position = (0, 0, -20)
            #camera.position = (0, 0, -camera.Z)
            camera.rotation = Vec3(0 , 0 , 0)
            #print(f'position ==> {camera.position}\nrotation ==> {camera.rotation}')
            # camera.look_at(cube)  # نگاه به سمت جسم
        
        elif key == '7':  # Top view
            camera.position = (0, 50, 0)
            camera.rotation = Vec3(90 , 0 , 0)
            #print(f'position ==> {camera.position}\nrotation ==> {camera.rotation}')
        
        elif key == '9':  # Bottom view
            camera.position = (0, -10, 0)
            camera.rotation = Vec3(-90 , 0 , 0)
            #print(f'position ==> {camera.position}\nrotation ==> {camera.rotation}')

