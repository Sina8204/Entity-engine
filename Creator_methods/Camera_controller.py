from ursina import *

class CameraController(Entity):
    def __init__(self, rotate_speed=80, pan_speed=5, zoom_speed=3):
        super().__init__()

        self.rotate_speed = rotate_speed
        self.pan_speed = pan_speed
        self.zoom_speed = zoom_speed

        self.veiw_text = Text(
            text='Veiw (Front)' , 
            position = (window.right.x - 0.2 , window.bottom.y + 0.06) ,
            color = color.yellow , 
            background=True,
            background_color=color.rgba(100, 150, 200, 0.8))
        
        self.opened_scene_text = Text(
            text='Scene : ' , 
            position = (window.bottom.x - 0.2 , -0.44) ,
            color = color.yellow)
        self.opened_scene_script_text = Text(
            text='Scene  script : ' , 
            position = (window.bottom.x - 0.2 , -0.4) ,
            color = color.yellow)
        

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
        
        elif key == '1' and held_keys['control'] :  # Left view
            camera.position = (0, 0, 20)
            #camera.position = (0, 0, camera.Z)
            camera.rotation = Vec3(0 , 180 , 0)
            self.veiw_text.text = 'Veiw (Left)'
            self.opened_scene_text.text += 'tests/test_add_script/Source/Level1'
            # self.opened_scene_text.background = False
            # self.opened_scene_text.background = True
            #print(f'position ==> {camera.position}\nrotation ==> {camera.rotation}')
            # camera.look_at(cube)  # نگاه به سمت جسم
            
        elif key == '3' and held_keys['control']:  # Right view
            camera.position = (0, 0, -20)
            #camera.position = (0, 0, -camera.Z)
            camera.rotation = Vec3(0 , 0 , 0)
            self.veiw_text.text = 'Veiw (right)'
            #print(f'position ==> {camera.position}\nrotation ==> {camera.rotation}')
            # camera.look_at(cube)  # نگاه به سمت جسم
        
        elif key == '7' and held_keys['control']:  # Top view
            camera.position = (0, 50, 0)
            camera.rotation = Vec3(90 , 0 , 0)
            self.veiw_text.text = 'Veiw (Top)'
            #print(f'position ==> {camera.position}\nrotation ==> {camera.rotation}')
        
        elif key == '9' and held_keys['control']:  # Bottom view
            camera.position = (0, -10, 0)
            camera.rotation = Vec3(-90 , 0 , 0)
            self.veiw_text.text = 'Veiw (Bottom)'
            #print(f'position ==> {camera.position}\nrotation ==> {camera.rotation}')

    def set_opened_scene_text(self , path):
        self.opened_scene_text.text = f"Scene : {path}"

    
    def set_opened_scene_source_text(self , path):
        self.opened_scene_script_text.text = f"Scene source path : {path}"


Active_camera_controller = CameraController()