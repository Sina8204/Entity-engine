from ursina import *

app = Ursina()
ground = Entity(model='plane', scale=20, texture='white_cube', texture_scale=(20, 20))

# ایجاد یک دوربین
camera.position = (0, 0, -10)
speed = 4     # سرعت حرکت دوربین
pan_speed = 4 # سرعت حرکت با راست‌کلیک

def update():
    # حرکت با کلیدها
    if held_keys['d']:
        camera.x += time.dt * speed

    if held_keys['a']:
        camera.x -= time.dt * speed

    if held_keys['w']:
        camera.y += time.dt * speed

    if held_keys['s']:
        camera.y -= time.dt * speed

    # --- حرکت دوربین با راست‌کلیک و حرکت ماوس ---
    if mouse.right and mouse.moving:
        camera.x += mouse.delta.x * pan_speed
        camera.y += mouse.delta.y * pan_speed


app.run()
