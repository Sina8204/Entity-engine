# app.py

## <p dir="rtl">مستندات فایل app.py</p>

<p dir="rtl">
این فایل , فایل اصلی و اجرا کننده پروژه است.
</p>

<p dir="rtl">
<strong>وارد کردن ماژول های مورد نیاز جهت شروع :</strong>
</p>

```python
from ursina import *
import json
from Creator_methods.UI_classes import Sort_menus , catch_menus
from AppData import ProjectData
from Creator_methods import Browser
```
<p dir="rtl">
<strong>ایجاد حلقه اجرای پروژه :</strong>
</p>

```python
app = Ursina()

#Entities and other objects in app

app.run()
```

<p dir="rtl">
<strong>ایجاد منو ها</strong>
</p>

```
menu = catch_menus('Menus')
```
<p dir="rtl">
بر اساس معماری که در قسمت intro توضیح داده شد , قایل ها و پوشه های درون پوشه Menus به منو تبدیل میشوند.
با استفاده از کلاس <strong>catch_menus(path : str)</strong> منو ها ایجاد میشوند اما موقعیت و نظم مناسبی ندارند. به عبارتی تمامی منو ها به صورت یک لیست در متغیر menu ذخیره میشوند.
</p>

---

<p dir="rtl">
<strong>مرتب سازی منو ها به صورت افقی</strong>
</p>

```
Sort_menus(menu() , menus_x_pos=0.5)
```
<p dir="rtl">
کلاس <strong>Sort_menus</strong> در آرگومان اول خود لیستی از منو ها را دریافت میکند و آنها را به صورت سظری در بالای صفحه مرتب میکند. فاصله بین آنها با استفاده از اتریبیوت menus_x_pos تعیین میشود.
</p>

---

<p dir="rtl">
<strong>ایجاد یک plane</strong>
</p>

```
ground = Entity(model='plane', scale=20, texture='white_cube', texture_scale=(20, 20))
ground.y -= 1
```

<p dir="rtl">
یک plane به صورت خوابیده در صحنه ایجاد میکنیم که قرارگیری سایر انتیتی ها در صحنه به نسبت آن سنجیده شوند.
</p>

---

<p dir="rtl">
<strong>فعال سازی قابلیت های حرکت و چزخش دوربین در صحنه</strong>
</p>

```python
from Creator_methods.Camera_controller import Active_camera_controller
```

<p dir="rtl">
شی Active_camera_controller امکانات زیر را در اختیارمان قرار میدهد :

<ul dir="rtl"> 
    <li>✅ چرخش دوربین با فشردن اسکرول و درگ کردن در صحنه</li> 
    <li>✅ Zoom in و Zoom out کردن با Scroll up و Scroll down</li> 
    <li>✅ حرکت کردن دوربین با فشردن Right click و درگ کردن در صحنه</li> 
    <li>✅ با استفاده از شرتکات های زیر میتوانید زاویه دوربین را به زاویه اختصاص داده شده به آن شرتکات تغییر دهید :</li> 
    <ul dir="rtl"> 
        <li><code>ctrl + 1</code> : Left view</li>
        <li><code>ctrl + 3</code> : Right view</li>
        <li><code>ctrl + 7</code> : Top view</li>
        <li><code>ctrl + 9</code> : Bottom view</li>
    </ul>
</ul>
</p>

---

<p dir="rtl">
چاپ کردن اطلاعات صحنه و پروژه ایجاد شده
</p>

```python
def input(key):
    match(key):
        case "q": print(json.dumps(ProjectData.data , ensure_ascii=False , indent=2))
        case "t" : print(ProjectData.data)
        case "b": print(json.dumps(Browser() , ensure_ascii=False , indent=2))
```

<ul dir="rtl"> 
    با استفاده از شرتکات های زیر میتوانید اطلاعاتی درباره پروژه خود در برنامه و موجودیت های صحنه را در ترمینال دریافا کیند :
    <ul dir="rtl"> 
        <li><code>q</code> : چاپ جزعیات صحنه شامل نام انتیتی های ایجاد شده و ویژگی های آنها مثل موقعیت , چرخش , اندازه و سایر ویژگی ها تعریف شده برای آنها.</li>
        <li><code>t</code> : جزعیات صحنه را به صورت نامرتب در ترمینال چاپ میکند. با شرت کات <code>q</code>  چاپ جزعیات با json انجام میشود که گاهی ممکن است به دلیل ناخوانا بودن جزعیت با خطا مواجه شوید. بنابراین میتوانید از شرتکات <code>t</code> استفاده کنید.</li>
        <li><code>b</code> : چاپ اطلاعات پروژه باز شده در برنامه که شامل مسیر پروژه , مسیر صحنه باز شده , نام صحنه باز شده و سایر اطلاعات تعریف شده در شی Browser میشود.</li>
    </ul>
</ul>
</p>