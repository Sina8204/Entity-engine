from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

window.vsync = False
app = Ursina()

# متغیر برای tracking وضعیت نشانگر موس
mouse_locked = True  # در ابتدا نشانگر قفل است (مخفی و در مرکز صفحه)

ground = Entity(model='plane', scale=(100,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
e = Entity(model='cube', scale=(1,5,10), x=2, y=.01, rotation_y=45, collider='box', texture='white_cube')
e.texture_scale = (e.scale_z, e.scale_y)
e = Entity(model='cube', scale=(1,5,10), x=-2, y=.01, collider='box', texture='white_cube')
e.texture_scale = (e.scale_z, e.scale_y)

player = FirstPersonController(y=2, origin_y=-.5)
player.gun = None

gun = Button(parent=scene, model='cube', color=color.blue, origin_y=-.5, position=(3,0,3), collider='box', scale=(.2,.2,1))
def get_gun():
    gun.parent = camera
    gun.position = Vec3(.5,0,.5)
    player.gun = gun
gun.on_click = get_gun

gun_2 = duplicate(gun, z=7, x=8)
slope = Entity(model='cube', collider='box', position=(0,0,8), scale=6, rotation=(45,0,0), texture='brick', texture_scale=(8,8))
slope = Entity(model='cube', collider='box', position=(5,0,10), scale=6, rotation=(80,0,0), texture='brick', texture_scale=(8,8))

hookshot_target = Button(parent=scene, model='cube', color=color.brown, position=(4,5,5))
hookshot_target.on_click = Func(player.animate_position, hookshot_target.position, duration=.5, curve=curve.linear)

def input(key):
    global mouse_locked
    
    # مدیریت کلید Escape برای تغییر وضعیت نشانگر موس
    if key == 'escape':
        if mouse_locked:
            # آزاد کردن نشانگر موس
            mouse.locked = False
            mouse.visible = True
            mouse_locked = False
            print("نشانگر موس فعال شد (آزاد)")
        else:
            # قفل کردن نشانگر موس (حالت بازی)
            mouse.locked = True
            mouse.visible = False
            mouse_locked = True
            print("نشانگر موس غیرفعال شد (قفل)")
    
    # شلیک با دکمه چپ موس (فقط در حالت قفل)
    if key == 'left mouse down' and player.gun and mouse_locked:
        gun.blink(color.orange)
        bullet = Entity(parent=gun, model='cube', scale=.1, color=color.black)
        bullet.world_parent = scene
        bullet.animate_position(bullet.position+(bullet.forward*50), curve=curve.linear, duration=1)
        destroy(bullet, delay=1)

app.run()