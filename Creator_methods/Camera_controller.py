from ursina import *
import json

class CameraClipManager:
    def __init__(self):
        self.min_near = 0.01
        self.max_near = 5.0
        self.max_ratio = 10000
        
    def set_near(self, value):
        value = max(value, self.min_near)
        value = min(value, self.max_near)
        
        # بررسی نسبت
        far = camera.clip_plane_far
        if far / value > self.max_ratio:
            print(f"نسبت {far/value} بیش از حد مجاز است")
            # تنظیم اتوماتیک
            value = far / (self.max_ratio * 0.8)
        try:
            camera.clip_plane_near = value
            print(f"seted far plane => {value}")
            return value
        except Exception as e:
            print(f"Error at set near: {e}")
            camera.clip_plane_near = 0.1
            print(f"seted far plane => {0.1}")
        
    
    def set_far(self, value):
        # مشابه برای far
        value = max(value, 10)  # حداقل
        value = min(value, 10000)  # حداکثر
        
        near = camera.clip_plane_near
        if value / near > 10000:
            value = near * 1000  # تنظیم به نسبت معقول
        
        if value <= camera.clip_plane_near:
            value = camera.clip_plane_near * 100
        
        if value / camera.clip_plane_near > self.max_ratio:
            value = camera.clip_plane_near * (self.max_ratio * 0.8)
        try:
            camera.clip_plane_far = value
            print(f"seted far plane => {value}")
            return value
        except:
            print(f"Error at set clip_plane_far to {value}")
            camera.clip_plane_far = 1000
            print(f"seted far plane => {1000}")
            
        

# استفاده
manager = CameraClipManager()
# manager.set_near(0.05)
# manager.set_far(500)


class CameraController(Entity):
    def __init__(self, rotate_speed=80, pan_speed=5, zoom_speed=3):
        super().__init__()

        self.rotate_speed = rotate_speed
        self.pan_speed = pan_speed
        self.zoom_speed = zoom_speed

        self.is_set_camera = False
        self.camera_details = {}

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
        self.camera_fov = camera.fov

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
        elif key == 'w':
            self.camera_fov += 1
            self.set_fov(self.camera_fov)
            print(f"fov seted => {self.camera_fov}")
        elif key == 's':
            self.print_attrs()

        match(key):
            case 'i' : camera.fov += 1
            # print(json.dumps(self._attrs() , ensure_ascii=False , indent=2))
    def set_camera(self ,
                   position ,
                   rotation ,
                   scale ,
                   fov ,
                   near_plane ,
                   far_plane ,
                   orthographic):
        if not self.is_set_camera:
            self.camera_details = {
                'position' : camera.position ,
                'rotation' : camera.rotation ,
                'scale' : camera.scale ,
                'fov' : camera.fov ,
                'near_plane' : camera.clip_plane_near ,
                'far_plane' : camera.clip_plane_far ,
                'orthographic' : camera.orthographic
            }
        self.set_position(position)
        self.set_rotation(rotation)
        self.set_scale(scale)
        self.set_orthographic(orthographic)
        self.set_fov(fov)
        self.set_near_plane(near_plane)
        self.set_far_plane(far_plane)
        self.is_set_camera = True

    def un_set_camera(self):
        if self.is_set_camera:
            # self.set_camera(**self.camera_details)
            camera.position = self.camera_details['position']
            camera.rotation = self.camera_details['rotation']
            camera.scale = self.camera_details['scale']
            camera.fov = self.camera_details['fov']
            camera.clip_plane_near = self.camera_details['near_plane']
            camera.clip_plane_far = self.camera_details['far_plane']
            camera.orthographic = self.camera_details['orthographic']
            self.is_set_camera = False
        
    def set_position(self , value):
        camera.position = value

    def set_rotation(self , value):
        camera.rotation = value

    def set_scale(self , value):
        camera.scale = value
    
    def set_orthographic(self , value):
        camera.orthographic = value
    
    def set_fov(self , value):
        camera.fov = value

    def set_near_plane(self , value):
        manager.set_near(value)

    def set_far_plane(self , value):
        manager.set_far(value)
        
    def set_opened_scene_text(self , path):
        self.opened_scene_text.text = f"Scene : {path}"

    
    def set_opened_scene_source_text(self , path):
        self.opened_scene_script_text.text = f"Scene source path : {path}"

    def _attrs(self):
        return {
            'position' : camera.position ,
            'rotation' : camera.rotation ,
            'scale' : camera.scale ,
            'fov' : camera.fov ,
            'near_plane' : camera.clip_plane_near ,
            'far_plane' : camera.clip_plane_far ,
            'orthographic' : camera.orthographic
        }

    def print_attrs(self):
        for key , value in list(self._attrs().items()):
            print(f"{key} : {value}")
Active_camera_controller = CameraController()