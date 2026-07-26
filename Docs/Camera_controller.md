# Camera_controller.py
## <p dir="rtl">مستندات فایل Camera_controller.py</p>

<p dir="rtl">
در این فایل کلاسی تعریف کردیم تا دوربین صحنه را با آن کنترل کنیم. نام این کلاس <strong>CameraController</strong> میباشد که یک شی با نام <strong>Active_camera_controller</strong> از این کلاس تعریف کردیم تا با استفاده از آن دوربین صحنه را کنترل کنیم و همچنین از ویژگی هایی که در این کلاس تعریف شده استفاده کنیم.<br>
علاوه بر کلاس <strong>CameraController</strong> کلاسی دیگر با نام <strong>CameraClipManager</strong> تعریف کردیم تا ویژگی های near_plane و far_plane دوربین را کنترل کنیم. 
</p>
<p dir="rtl">
تنظیم این دو ویژگی نیازمند رعایت نسبت معینی بین آنهاست. اگر نسبت <code>far_plane</code> به <code>near_plane</code> بیش از حد بزرگ باشد، موتور گرافیکی Panda3d با خطا مواجه شده و برنامه از کار می‌افتد. این کلاس با اعمال محدودیت‌های مناسب، از بروز چنین خطاهایی جلوگیری می‌کند.</p>

<p dir="rtl">
در ادامه کد این دو کلاس را توضیح میدهیم.
</p>

---

## <p dir="rtl">ایجاد کلاس CameraClipManager :</p>

```python
class CameraClipManager:
    def __init__(self):
        self.min_near = 0.01
        self.max_near = 5.0
        self.max_ratio = 10000
```
<p dir="rtl">
در سازنده این کلاس متغیر هایی جهت تنظیم کمترین مقدار near_plane  و بیشترین مقدار near_plane تعریف کردیم و همچنین بیشترین مقدار ratio را هم ذخیره کردیم تا در فرآيند محاسبات ست کردن near_plane و far_plane از آنها استفاده کنیم.
</p>

<p dir="rtl">
<strong>تعریف تابع تنظیم کردن near_plane با نام <code>set_near</code> :</strong>
</p>

```python
def set_near(self, value):
    value = max(value, self.min_near)
    value = min(value, self.max_near)
```

<p dir="rtl">
در این تابع ابتدا بیشترین و کمترین مقداری که آرگومان value میتواند داشته باشد را تنظیم کردیم.
</p>

```python
# بررسی نسبت
    far = camera.clip_plane_far
```
<p dir="rtl">
مقدار فعلی far_plane دوربین را دریافت کردیم و در متغیر far ذخیره میکنیم تا بررسی مقدار مناسب value را با آن انجام دهیم.
</p>

```python
if far / value > self.max_ratio:
    print(f"نسبت {far/value} بیش از حد مجاز است")
    # تنظیم اتوماتیک
    value = far / (self.max_ratio * 0.8)
```

<p dir="rtl">
نکته مهم: نسبت <code>far_plane</code> به <code>near_plane</code> نباید از حداکثر مجاز (<code>max_ratio</code>) بیشتر شود. در صورت بروز این مشکل، مقدار <code>near_plane</code> را به‌گونه‌ای تنظیم می‌کنیم که این نسبت در محدوده مجاز قرار گیرد.<br>
 حال اگر این شرط برقرار نباشد , مقدار <code>value</code> بدون هیچ تغییری باقی میماند و در ادامه با همان مقداری که در ورودی تابع داده شد پیش میرود.
</p>

```python
try:
    camera.clip_plane_near = value
    print(f"seted far plane => {value}")
    return value
```
<p dir="rtl">
با اینکه بررسی های لازم را انجام دادیم , محض احتیاط جهت جلوگیری از بروز هرگونه خطایی از ساختار <code>try-except</code> استفاده میکنیم.<br>
درصورتی که خطایی رخ ندهد مقدار <code>near_plane</code> دوربین را برابر value قرار میدهیم.
</p>

```python
except Exception as e:
    print(f"Error at set near: {e}")
    camera.clip_plane_near = 0.1
    print(f"seted far plane => {0.1}")
```
<p dir="rtl">
درصورت هرگونه بروز خطایی مقدار <code>near_plane</code> دوربین را برابر <code>0.1</code> قرار میدهیم.
</p>

<p dir="rtl">
<strong>تعریف تابع تنظیم کردن far_plane با نام <code>set_far</code> :</strong>
</p>

```python
def set_far(self, value):
    # مشابه برای far
    value = max(value, 10)  # حداقل
    value = min(value, 10000)  # حداکثر
    near = camera.clip_plane_near
```

<p dir="rtl">
همانند تابع قبل , در ابتدا بیشترین و کمترین مقداری که آرگومان <code>value</code> میتواند داشته باشد را تعیین میکنیم. همچنین مقدار فعلی <code>near_plane</code> دوربین را هم در متغیر <code>near</code> ذخیره میکنیم.
</p>

```python
if value / near > 10000:
    value = near * 1000  # تنظیم به نسبت معقول

if value <= camera.clip_plane_near:
    value = camera.clip_plane_near * 100

if value / camera.clip_plane_near > self.max_ratio:
    value = camera.clip_plane_near * (self.max_ratio * 0.8)
```

<p dir="rtl">
در صورت برقراری شرط های تعیین شده مقدار معینی را برای <code>value</code> تعیین میکنیم تا با خطایی مواجه نشویم.
</p>

```python
try:
    camera.clip_plane_far = value
    print(f"seted far plane => {value}")
    return value
except:
    print(f"Error at set clip_plane_far to {value}")
    camera.clip_plane_far = 1000
    print(f"seted far plane => {1000}")
```

<p dir="rtl">
حال در صورتی که خطایی رخ ندهد مقدار <code>value</code> بر روی <code>far_plane</code> دوربین اعمال میشود ولی اگه خطایی رخ دهد مقدار <code>1000</code> بر روی <code>far_plane</code> دوربین ایجاد میشود.
</p>

```python
manager = CameraClipManager()
```

<p dir="rtl">
جحت استفاده از کلاس <code>CameraClipManager</code> شی <code>manager</code> را تعریف کردیم.
</p>

---

## <p dir="rtl">ایجاد کلاس CameraController :</p>

<p dir="rtl">
جهت کنترل دوربین در صحنه , کلاس <code>CameraController</code> را تعریف کردیم.<br>
با استفاده از این کلاس  میتوانیم کار های زیر را انجام دهیم:
</p>
<p dir="rtl">
<ul dir="rtl"> 
    <li>✅ چرخش دوربین با فشردن اسکرول و درگ کردن در صحنه</li> 
    <li>✅ <code>Zoom in</code> و <code>Zoom out</code> کردن با <code>Scroll up</code> و <code>Scroll down</code></li> 
    <li>✅ حرکت کردن دوربین با فشردن <code>Right click</code> و درگ کردن در صحنه</li> 
    <li>✅ با استفاده از کلید های ترکیبی زیر میتوانید زاویه دوربین را به زاویه اختصاص داده شده به آن کلیدهای ترکیبی تغییر دهید :</li> 
    <ul dir="rtl"> 
        <li><code>ctrl + 1</code> : Left view</li>
        <li><code>ctrl + 3</code> : Right view</li>
        <li><code>ctrl + 7</code> : Top view</li>
        <li><code>ctrl + 9</code> : Bottom view</li>
    </ul>
</ul>
</p>
<p dir="rtl">
در ادامه به بررسی کد این کلاس میپردازیم :
</p>


```python
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
```

<p dir="rtl">
در سازنده این کلاس آرگومان های <code>rotate_speed</code> , <code>pan_speed</code> , <code>zoom_speed</code> را به ترتیب جهت تنظیم سرعت چرخش دوربین با فشردن اسکرول , سرعت حرکت کردن دوربین با راست کلیک و سرعت زوم کردن دوربین با اسکرول کردن را تعریف کردیم.
</p>

<p dir="rtl">
دو متغیر <code>self.is_set_camera</code> و <code>self.camera_details</code> برای مدیریت وضعیت دوربین تعریف شده‌اند: 
</p>

<p dir="rtl">
    <ul dir="rtl"> 
        <li><code>self.is_set_camera</code>: مشخص می‌کند که آیا دوربین صحنه غیرفعال شده و دوربین کاربر جای آن را گرفته است یا خیر.</li> 
        <li><code>self.camera_details</code>: آخرین وضعیت (موقعیت، چرخش، fov و ...) دوربین صحنه را قبل از تغییر ذخیره می‌کند تا در صورت نیاز بتوان به آن بازگشت.</li> </ul>
</p>

<p dir="rtl">
 این مکانیزم به کاربر اجازه می‌دهد بین دوربین‌های مختلف در صحنه جابه‌جا شود و همواره امکان بازگشت به دوربین اصلی را داشته باشد.
</p>

```python
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
```

<p dir="rtl">
انتیتی هایی جهت نمایش اطلاعاتی در صحنه تعریف کردیم که در لیست زیر میتوانید این اطلاعات را بررسی کنید :
<ul dir="rtl"> 
    <li><code>self.veiw_text</code> : نمایش آخرین تغییر زاویه خاصی از دوربین که شامل <code>left</code> , <code>right</code> , <code>top</code> , <code>bottom</code> میشود</li>
    <li><code>self.opened_scene_text</code> : نام صحنه ای که باز است و کاربر دارد در آن کار میکند.</li>
    <li><code>self.opened_scene_script_text</code> : مسیر اسکریپت صحنه ای که کاربر دارد در آن کار میکند. و در صورت Run کردن صحنه آن اسکریپت اجرا میشود.</li>
</ul>
</p>

```python
# تنظیمات اولیه دوربین
camera.position = (0, 0, -10)
self.camera_fov = camera.fov
```

<p dir="rtl">
موقعیت اولیه دوربین در صحنه تنظیم میشود و مقدار <code>fov</code> آن در متغیر <code>self.camera_fov</code> ذخیره میشود.
</p>

```python
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
```

<p dir="rtl">
بررسی تابع update :
</p>

```python
    # --- Rotate mouse by scroll (Middle Mouse) ---
    if mouse.middle and mouse.moving:
        camera.rotation_y += mouse.velocity.x * self.rotate_speed
        camera.rotation_x -= mouse.velocity.y * self.rotate_speed
        print(camera.rotation)
```

<p dir="rtl">
در صورتی که اسکرول فشرده شد و موس در حال حرکت بود , دوربین را درجهات تعیین شده حرکت بده.
</p>

```python
    # --- Move (Pan) mouse by right click---
    if mouse.right and mouse.moving:
        right = camera.right
        up    = camera.up

        camera.position += right * mouse.velocity.x * self.pan_speed
        camera.position += up * (-mouse.velocity.y) * self.pan_speed
        print(camera.position)
```

<p dir="rtl">
در صورتی که راست کلیک فشرده شد و موس در حال حرکت بود , دوربین را در موقعیت های تعیین شده حرکت بده.
</p>

```python
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
        case 'i' : 
            self.camera_fov -= 1
            self.set_fov(self.camera_fov)
```

<p dir="rtl">
در صورت کلیک دکمه های مذکور اعمال تعیین شده در شرطشان اجرا میشود. در زیر این دکمه ها و اعمال کلیکشان را میتوانید بررسی کنید :
</p>

<p dir="rtl">
    <ul dir="rtl"> 
        <li><code>scroll up</code> : عمل <code>Zoomin</code> را انجام میدهد</li>
        <li><code>scroll down</code> : عمل <code>Zoomout</code> را انجام میدهد</li>
        <li><code>ctrl + 1</code> : زاویه دوربین را به نمای <code>Left</code> تغییر میدهد</li>
        <li><code>ctrl + 3</code> : زاویه دوربین را به نمای <code>Right</code> تغییر میدهد</li>
        <li><code>ctrl + 7</code> : زاویه دوربین را به نمای <code>Top</code> تغییر میدهد</li>
        <li><code>ctrl + 9</code> : زاویه دوربین را به نمای <code>Bottom</code> تغییر میدهد</li>
        <li><code>w</code> : مقدار fov دوربین صحنه را 1 واحد افزایش میدهد.</li>
        <li><code>s</code> : مقدار ویژگی های <code>position</code> , <code>rotation</code> , <code>scale</code> , <code>fov</code> , <code>near_plane</code> , <code>far_plane</code> , <code>orthographic</code> را در ترمینال چاپ میکند.</li>
        <li><code>i</code> : مقدار fov دوربین صحنه را 1 واحد کاهش میدهد.</li>
    </ul>
</p>


```python
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
```

<p dir="rtl">
این تابع برای تغییر دوربین صحنه به یک دوربین سفارشی که کاربر ساخته است، استفاده می‌شود: 
    <ol dir="rtl"> 
        <li>ابتدا بررسی می‌کند که آیا قبلاً دوربین دیگری تنظیم شده است یا خیر (<code>self.is_set_camera</code>).
        </li> 
        <li>اگر دوربین صحنه هنوز فعال است، وضعیت فعلی آن را در <code>self.camera_details</code> ذخیره می‌کند.
        </li> 
        <li>سپس ویژگی‌های دوربین جدید (که کاربر تعیین کرده) را روی دوربین صحنه اعمال می‌کند.
        </li> 
        <li>در نهایت <code>self.is_set_camera</code> را <code>True</code> قرار می‌دهد تا مشخص شود دوربین صحنه غیرفعال است.
        </li> 
    </ol> 
</p>

<p dir="rtl">
این امکان به کاربر اجازه می‌دهد بین چند دوربین مختلف در صحنه جابه‌جا شود، در حالی که همیشه وضعیت دوربین اصلی برای بازگشت محفوظ است.
</p>

```python
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
```

<p dir="rtl">
این تابع برای بازگشت از دوربین سفارشی به دوربین اصلی صحنه استفاده می‌شود: 
    <ol dir="rtl"> 
        <li>بررسی می‌کند که آیا دوربین صحنه غیرفعال است (<code>self.is_set_camera == True</code>).</li> 
        <li>اگر چنین است، آخرین وضعیت ذخیره‌شده دوربین صحنه را از <code>self.camera_details</code> بازیابی می‌کند.</li> 
        <li>ویژگی‌های بازیابی‌شده را روی دوربین صحنه اعمال می‌کند.</li> 
        <li><code>self.is_set_camera</code> را <code>False</code> می‌کند تا نشان دهد دوربین صحنه دوباره فعال شده است.</li> 
    </ol>
</p>

```python
    def set_position(self , value):
        camera.position = value
```

<p dir="rtl">
موقعیت دوربین را تغییر میدهد.
</p>

```python
    def set_rotation(self , value):
        camera.rotation = value
```

<p dir="rtl">
چرخش دوربین را تنظیم میکند
</p>


```python
    def set_scale(self , value):
        camera.scale = value
```

<p dir="rtl">
اندازه دوربین را تغییر میدهد.
</p>

```python
    def set_orthographic(self , value):
        camera.orthographic = value
```

<p dir="rtl">
ویژگی <code>orthographic</code> دوربین را تغییر میدهد.
</p>

```python
    def set_fov(self , value):
        camera.fov = value
```

<p dir="rtl">
مقدار fov دوربین را تغییر میدهد.
</p>


```python
    def set_near_plane(self , value):
        manager.set_near(value)
```

<p dir="rtl">
با استفاده از شی <code>manager</code> که بالاتر توضیح دادیم , ویژگی <code>near_plane</code> دوربین را تنظیم میکند.
</p>


```python
    def set_far_plane(self , value):
        manager.set_far(value)
```

<p dir="rtl">
با استفاده از شی <code>manager</code> ویژگی <code>far_plane</code> دوربین را تنظیم میکند.
</p>

```python
    def set_opened_scene_text(self , path):
        self.opened_scene_text.text = f"Scene : {path}"
```

<p dir="rtl">
با استفاده از این متود , متن انتیتی <code>self.opened_scene_text</code> را تغییر میدهیم.
</p>

```python
    def set_opened_scene_source_text(self , path):
        self.opened_scene_script_text.text = f"Scene source path : {path}"
```

<p dir="rtl">
با استفاده از این متود , متن انتیتی <code>self.opened_scene_script_text</code> را تغییر میدهیم.
</p>

```python
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
```

<p dir="rtl">
با استفاده از این متود , میتوانیم ویژگی های فعلی دوربین را دریافت کنیم.
</p>

```python
    def print_attrs(self):
        for key , value in list(self._attrs().items()):
            print(f"{key} : {value}")
```

<p dir="rtl">
در این متود با استفاده از متود <code>_attrs</code> ویژگی های فعالی دوربین را دریافت و در ترمینال چاپ میکنیم.
</p>

```python
Active_camera_controller = CameraController()
```

<p dir="rtl">
در انتها یک شی از کلاس <code>CameraController</code> تعریف میکنیم و در سراسر پروژه از آن استفاده میکنیم.
</p>
