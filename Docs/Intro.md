# Entity engine

## <p dir="rtl">Entity Engine : تجربه‌ای نوین در بازی‌سازی با پایتون و Ursina </p>

<p dir="rtl">
اگر به دنبال راهی سریع و لذت‌بخش برای ساخت بازی با **Ursina** هستید، **Entity Engine** همان ابزاری است که نیاز دارید. این موتور، مجموعه‌ای از ابزارهای هوشمند را در اختیارتان قرار می‌دهد تا فرایند توسعه را تسهیل کرده و بر کیفیت نهایی بیفزاید.

ایده‌ی شکل‌گیری Entity Engine، ایجاد یک فضای گرافیکی ساده و در عین حال قدرتمند برای کاربران Ursina بود. حالا هر کسی، بدون نیاز به دانش پیچیده، می‌تواند از توانمندی‌های این پکیج بهره ببرد.

**نتیجه‌ی کار با Entity Engine چیست؟**  
یک سورس کد کامل و اجرایی که با زدن یک کلیک بر روی فایل اصلی، بازی شما در محیطی گرافیکی به نمایش درمی‌آید. فرقی نمی‌کند تازه‌کار هستید یا حرفه‌ای؛ Entity Engine مسیر ساخت بازی را برایتان هموار می‌کند.
</p>

---

## <p dir="rtl"> ساختار پروژه ها در Entity engine </p>

```markdown
<Project name>
├── Assets
├── project_scenes.json
└── Source
    ├── __Assets
    ├── __libs
    │   └── changer.py
    ├── __Runner
    │   └── run.py
    ├── __ScnRunner
    │   ├── __init__.py
    │   └── run.py
    ├── scn.py
    ├── <Project name>.py
    └── <Scenes folders>
        ├── details.py
        ├── __init__.py
        └── <Scenes entities folders>
            └── script.py
```
---
## <p dir="rtl"> معماری Entity engine </p>

<p dir="rtl"> 
معماری Entity Engine بر پایه یک ایده‌ی ساده اما بسیار قدرتمند بنا شده است: <strong>تبدیل خودکار ساختار پوشه‌ها و فایل‌ها به منوهای تعاملی</strong>. به عبارت دیگر، هر پوشه در مسیر <code>Menu</code> به یک <strong>منو (Menu)</strong> و هر فایل درون آن به یک <strong>دکمه‌ی منو (Menu Button)</strong> تبدیل می‌شود. این ساختار به صورت تو در تو و کاملاً خودکار تا هر سطحی که نیاز باشد، ادامه پیدا می‌کند. 
</p><p dir="rtl"> برای درک بهتر، یک مثال ساده را بررسی می‌کنیم:<br> 
فرض کنید پوشه‌ای به نام <code>x</code> داریم که شامل پوشه‌ی <code>y</code> و فایل <code>z</code> است. در خروجی، یک منوی <strong>x</strong> ایجاد می‌شود که شامل یک زیرمنوی <strong>y</strong> و یک دکمه‌ی <strong>z</strong> خواهد بود. حال اگر درون پوشه‌ی <code>y</code> نیز زیرپوشه‌های دیگری وجود داشته باشند، آنها نیز به همین ترتیب به منوهای جدید تبدیل و در جایگاه خود قرار می‌گیرند. 
</p>
<p dir="rtl">
 💡 <strong>نکته‌ی کلیدی:</strong><br> اگر به هر دلیلی نمی‌خواهید پوشه‌ای به منو تبدیل شود، کافی است نام آن را با دو خط زیر (<code>__</code>) شروع کنید. برای مثال، پوشه‌ی <code>__FolderName</code> در فرآیند تولید منو نادیده گرفته می‌شود و به صورت یک پوشه‌ی معمولی باقی می‌ماند. 
</p>

### <p dir="rtl">⚡ رویدادهای دکمه‌های منو (Menu Button Events)</p>

<p dir="rtl">
 هر فایل <code>.py</code> که در ساختار منو قرار می‌گیرد، باید یک تابع به نام <code>main</code> داشته باشد. این تابع، دقیقاً همان چیزی است که هنگام کلیک روی دکمه‌ی متناظر با آن فایل، اجرا می‌شود.
</p>
<p dir="rtl"> 
🔍 <strong>مثال عملی:</strong><br> فرض کنید در مسیر <code>Menu</code>، پوشه‌ای به نام <code>Print</code> داریم که شامل فایل <code>hello.py</code> است. طبق معماری توضیح‌داده‌شده، یک منوی <strong>Print</strong> با یک دکمه‌ی <strong>hello</strong> در اختیار خواهیم داشت. حال محتوای فایل <code>hello.py</code> را به صورت زیر در نظر بگیرید: 
</p>

```python
message = "Hello world"
def main(*args , **kwargs)
{
    print(message)
}
```

<p dir="rtl">
 حالا وقتی کاربر روی دکمه‌ی <strong>hello</strong> کلیک کند، عبارت <code>Hello world</code> در ترمینال چاپ می‌شود. این یعنی با کمترین کدنویسی، یک قابلیت تعاملی کامل در اختیار دارید. 
</p>

### <p dir="rtl">🧩 کاربرد این معماری در پروژه‌ی Entity Engine</p>

<p dir="rtl"> 
این رویکرد هوشمندانه، تحولی بزرگ در روند توسعه‌ی Entity Engine ایجاد کرد. ما توانستیم <strong>entity‌های شخصی‌سازی‌شده</strong> را به سادگی و بدون نیاز به نوشتن کلاس‌های جداگانه برای هر کدام، به پروژه اضافه کنیم. هر entity شامل پنل‌ها و گیزموهای مختص خود برای تغییر موقعیت است. 
</p>
<p dir="rtl"> 
🧠 <strong>چالش قبل از این معماری:</strong><br> اگر این ساختار را پیاده‌سازی نمی‌کردیم، برای هر entity مجبور بودیم یک کلاس جداگانه بنویسیم و برای هر کدام، یک منوباتن دستی تعریف کنیم. این فرآیند نه‌تنها زمان‌بر بود، بلکه نگهداری و توسعه‌ی پروژه را به شدت دشوار می‌کرد. 
</p>
<p dir="rtl"> 
✅ <strong>دستاورد این معماری:</strong><br> 
با این راه‌کار، هم فرآیند توسعه برای خودمان ساده‌تر شد و هم مسیر را برای <strong>توسعه‌دهندگان دیگر</strong> هموار کردیم. حالا هر کسی می‌تواند: </p>
<ul dir="rtl"> 
    <li>✅ entity‌های شخصی‌سازی‌شده‌ی خود را به سادگی اضافه کند.</li> 
    <li>✅ قابلیت‌های جدیدی که نیاز دارد، با کمترین کدنویسی پیاده‌سازی کند.</li> 
    <li>✅ منوهای دلخواه خود را فقط با ایجاد پوشه در مسیر <code>Menus</code> بسازد.</li> 
    <li>✅ با ایجاد یک فایل <code>.py</code>، یک دکمه‌ی جدید به منو اضافه و عملکرد مورد نظرش را پیاده کند.</li> 
</ul>
<p dir="rtl"> 
✨ <strong>به عبارت ساده‌تر:</strong> شما فقط کافی است ایده‌ی خود را در قالب یک فایل پایتون در ساختار منو قرار دهید. بقیه‌ی کار را <strong>Entity Engine</strong> انجام می‌دهد! 
</p>

---
### <p dir="rtl">Entity engine structure</p>
<p dir="rtl">
جهت بررسی ساختار و کد ها و کلاس های این پروژه میتوانید منوی درختی زیر را بررسی کنید که هم ساختار پروژه را نمایش میدهد و هم با کلیک بر روی هر لینک شما را به راهنمای آن فایل/پوشه ارجاع میدهد.
</p>

- **Entity Engine**
  - 📂 [AppData](www.google.com) ← داده‌ها و تنظیمات برنامه
    - init.py
    - last_data.json ← آخرین وضعیت پروژه
    - ProjectData_manager.py
    - project_status.py
    - scripts_manager.py
    - settings.json ← تنظیمات کاربر
  - 📂 Creator_methods ← متدهای سازنده و ابزارهای ایجاد
    - 📂 3D_objects
      - camera.glb ← مدل سه‌بعدی دوربین
    - [Camera_controller.py](https://github.com/Sina8204/Entity-engine/blob/bb4e1bece4351bf223ce8639858d3131b3512cc1/Docs/Camera_controller.md) ← مدیریت دوربین صحنه
    - Camera_creator.py
    - deselect.py
    - [Entity_creator.py](https://github.com/Sina8204/Entity-engine/blob/bb4e1bece4351bf223ce8639858d3131b3512cc1/Docs/Entity_creator.md) ← کلاس ایجاد کننده انتیتی ها
    - File_browser.py
    - init.py
    - Scene_manager.py
    - tree_button.py
    - tree_projects_entity.py
    - UI_classes.py
  - 📂 __libs ← کتابخانه‌های داخلی
    - changer.py
  - 📂 Menus ← ساختار منوهای اصلی برنامه
    - 📂 File
      - 📂 New
        - New project.py
        - New scene.py
      - 📂 Open
        - Open project.py
        - Open scene.py
      - 📂 Save
        - Save scene.py
        - Save scene as.py
        - Save project.py
    - 📂 Edit
      - 📂 Run
        - Run project.py
        - Run Scene.py
      - Set IDE.py
      - copy.py
    - 📂 Entity
      - open model
      - 📂 3D entity
        - camera.py
        - cube.py
        - sphere.py
        - diamond.py
        - plane.py
        - quad.py
        - circle.py
        - icosphere.py
        - sky dome.py
        - wireframe cube.py
      - 📂 2D entity
        - sprite.py
  - app.py ← نقطه‌ی ورود اصلی برنامه


