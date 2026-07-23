در پکیج **Ursina**، کلاس `Camera` یک موجودیت ویژه است که برای نمایش صحنه از دید بازیکن یا دوربین استفاده می‌شود. این کلاس از `Entity` ارث‌بری می‌کند، بنابراین تمام اتریبیوت‌های `Entity` را دارد، به علاوه تعدادی ویژگی خاص برای کنترل دوربین.

در ادامه، مهم‌ترین اتریبیوت‌های مربوط به تنظیم دوربین در Ursina را به‌صورت دسته‌بندی شده معرفی می‌کنم:

---

### ۱. اتریبیوت‌های موقعیت و چرخش (ارث‌بری از Entity)

| اتریبیوت | نوع | توضیح |
|----------|------|--------|
| `position` | `Vec3` | موقعیت دوربین در فضای سه‌بعدی (مختصات x, y, z) |
| `x`, `y`, `z` | `float` | هر کدام از محورهای موقعیت به‌صورت جداگانه |
| `rotation` | `Vec3` | چرخش دوربین بر حسب درجه (Pitch, Yaw, Roll) |
| `rotation_x`, `rotation_y`, `rotation_z` | `float` | چرخش در هر محور به‌صورت جداگانه |
| `world_position` | `Vec3` | موقعیت در فضای جهانی (اگر دوربین زیرمجموعه‌ای داشته باشد) |
| `world_rotation` | `Vec3` | چرخش در فضای جهانی |

---

### ۲. اتریبیوت‌های مربوط به نمای دوربین (Projection)

| اتریبیوت | نوع | توضیح |
|----------|------|--------|
| `fov` | `float` | **زاویه میدان دید** (Field of View) بر حسب درجه. مقدار پیش‌فرض `60` درجه است. افزایش آن باعث نمای بازتر (Wide) و کاهش آن باعث نمای نزدیک‌تر (Zoom) می‌شود. |
| `aspect_ratio` | `float` | نسبت ابعاد تصویر (عرض به ارتفاع). معمولاً به‌طور خودکار از پنجره گرفته می‌شود، اما قابل تنظیم دستی است. |
| `near_plane` | `float` | **صفحه برش نزدیک** - نزدیک‌ترین فاصله از دوربین که اشیا دیده می‌شوند. پیش‌فرض `0.1`. |
| `far_plane` | `float` | **صفحه برش دور** - دورترین فاصله از دوربین که اشیا دیده می‌شوند. پیش‌فرض `100`. |
| `orthographic` | `bool` | اگر `True` باشد، دوربین به حالت **ارتوگرافیک** (بدون پرسپکتیو) می‌رود که برای بازی‌های دوبعدی یا نمای نقشه استفاده می‌شود. |
| `orthographic_size` | `float` | در حالت ارتوگرافیک، اندازه نمای قابل مشاهده را مشخص می‌کند. |

---

### ۳. اتریبیوت‌های کنترل دوربین (ویژه دوربین اصلی)

| اتریبیوت | نوع | توضیح |
|----------|------|--------|
| `enabled` | `bool` | اگر `False` باشد، دوربین غیرفعال شده و چیزی نمایش نمی‌دهد. |
| `parent` | `Entity` یا `Scene` | والد دوربین را مشخص می‌کند. اگر به یک موجودیت متصل شود، دوربین با آن حرکت می‌کند. |
| `camera` (به‌عنوان شیء) | `Camera` | خود دوربین. معمولاً با `camera = Camera()` ساخته می‌شود. |
| `ui_camera` | `Camera` | دوربین مخصوص رابط کاربری (UI) که در پس‌زمینه قرار دارد. |

---

### ۴. اتریبیوت‌های مربوط به پس‌زمینه و رنگ

| اتریبیوت | نوع | توضیح |
|----------|------|--------|
| `background_color` | `color` | رنگ پس‌زمینه دوربین (پیش‌فرض `color.black`). |
| `clear_color` | `color` | همان `background_color` - رنگ پاک‌کننده صحنه قبل از رندر. |

---

### ۵. اتریبیوت‌های پیشرفته (کمتر استفاده می‌شوند)

| اتریبیوت | نوع | توضیح |
|----------|------|--------|
| `node` | `NodePath` | گره Panda3D پشت صحنه (اگر با Panda3D آشنایی دارید). |
| `shader` | `Shader` | برای اعمال شیدرهای سفارشی روی دوربین. |
| `render_target` | `RenderTarget` | هدف رندرینگ (برای افکت‌های تصویری یا آینه‌ها). |

---

### مثال‌های کد:

```python
from ursina import *

app = Ursina()

# تغییر زاویه دید
camera.fov = 90  # نمای بازتر

# تغییر موقعیت دوربین
camera.position = (0, 5, -10)
camera.rotation = (20, 0, 0)  # نگاه به پایین

# فعال کردن حالت ارتوگرافیک برای نمای دوبعدی
# camera.orthographic = True
# camera.orthographic_size = 10

# تغییر صفحات برش
camera.near_plane = 0.5
camera.far_plane = 200

# تغییر رنگ پس‌زمینه
camera.background_color = color.light_gray

app.run()
```

---

### نکته مهم:
اگر از `EditorCamera` (که با کلید F برای فعال‌سازی در حین اجرا استفاده می‌شود) استفاده می‌کنید، این کلاس دارای اتریبیوت‌های اضافی مثل `speed` (سرعت حرکت) و `rotation_speed` (سرعت چرخش) نیز هست که برای ناوبری در صحنه طراحی شده‌اند.

اگر سوال خاصی درباره نحوه تنظیم یکی از این اتریبیوت‌ها دارید، خوشحال می‌شوم بیشتر توضیح بدهم. 😊

# تغییر ویژگی های camera

سینا، خیلی خوب گرفتی مسئله رو—بریم سراغ خود کد Ursina، نه حدس و گمان.

1. واقعاً چه اتریبیوت‌هایی برای دوربین وجود دارند؟

توی سورس Ursina، کلاس Camera این پراپرتی‌ها رو دارد:   

- fov → زاویه دید افقی  
- orthographic → سوییچ بین پرسپکتیو و اورتو  
- clipplanenear → near plane  
- clipplanefar → far plane  

و برای aspect ratio از window.aspect_ratio استفاده می‌کند، نه از خود camera.   

پس این‌ها رو می‌تونی مستقیم ست کنی:

```python
camera.fov = 60
camera.orthographic = False
camera.clipplanenear = 0.1
camera.clipplanefar = 500
```

---

2. nearplane و farplane

به‌جای nearplane و farplane باید از همین دو تا استفاده کنی:

```python
camera.clipplanenear = 0.3
camera.clipplanefar = 300
```

این‌ها روی لنز Panda3D ست می‌شوند داخل خود کلاس Camera.   

---

3. aspect_ratio

در Ursina، aspect ratio به‌صورت خودکار از پنجره گرفته می‌شود:

```python
from ursina import window

print(window.aspect_ratio)   # مثلاً 16/9
```

اگر بخوای aspect_ratio رو عوض کنی، باید اندازه‌ی پنجره رو تغییر بدی، نه camera:

```python
window.size = (1280, 720)   # این غیرمستقیم aspect_ratio رو عوض می‌کند
```

خود دوربین از window.aspect_ratio برای تنظیم لنز استفاده می‌کند.   

---

4. orthographic_size

در Ursina، وقتی camera.orthographic = True باشد، اندازه‌ی دید اورتو از روی fov و aspectratio محاسبه می‌شود و با setfilmsize(self.fov * window.aspectratio, self.fov) روی لنز ست می‌شود.   

یعنی برای تغییر «اندازه‌ی اورتو»، باید:

```python
camera.orthographic = True
camera.fov = 20   # هرچه fov کوچک‌تر، زوم بیشتر (در حالت اورتو)
```

---

5. جمع‌بندی عملی برای چند دوربین مجازی

برای هر دوربین مجازی، این‌ها رو ذخیره کن:

```python
cam1 = Entity(
    position=(0, 5, -10),
    rotation=(15, 0, 0),
    fov=40,
    ortho=False,
    near=0.1,
    far=200
)
```

و موقع سوییچ:

```python
def applycamerasettings(cam):
    camera.position = cam.position
    camera.rotation = cam.rotation
    camera.fov = cam.fov
    camera.orthographic = cam.ortho
    camera.clipplanenear = cam.near
    camera.clipplanefar = cam.far
```

اگر دوست داری، می‌تونیم با هم یک سیستم کامل «پروفایل دوربین» طراحی کنیم که راحت بین‌شون سوییچ کنی.