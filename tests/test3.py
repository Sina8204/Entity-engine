from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

app = Ursina()

buttons = []  # لیست تمام دکمه‌ها به ترتیب ظاهر شدن


def rearrange_buttons():
    y = 0.4
    for b in buttons:
        b.y = y
        y -= 0.1
        # فرزندان بلافاصله بعد از والد
        for child in b.children_buttons:
            child.y = y
            y -= 0.1


class HierarchyButton(Button):
    def __init__(self, label, parent_button=None):
        super().__init__(
            text=label,
            scale=(0.25, 0.06),
            x=-0.7,
            y=0,  # ابتدا y=0، بعد rearrange تنظیم می‌کند
            color=color.azure,
            origin=(-0.5, 0),
            parent=camera.ui   # ← خیلی مهم!
        )
        self.label = label
        self.parent_button = parent_button
        self.children_buttons = []

    def input(self, key):
        if self.hovered and key == 'left mouse down':
            print(f"Clicked: {self.label}")

        if self.hovered and key == 'right mouse down':
            self.open_child_menu()

    def open_child_menu(self):
        # position را نسبت به والد تنظیم کن
        menu = DropdownMenu(
            "Add Child",
            buttons=[
                DropdownMenuButton("Cube",  onclick=lambda: self.add_child_button("Cube")),
                DropdownMenuButton("Plane", onclick=lambda: self.add_child_button("Plane")),
                DropdownMenuButton("Quad",  onclick=lambda: self.add_child_button("Quad")),
            ],
            position=(self.x + 0.35, self.y)
        )


    def add_child_button(self, label):
        child = HierarchyButton(label, parent_button=self)
        self.children_buttons.append(child)

        # اضافه کردن به لیست اصلی
        index = buttons.index(self) + 1
        buttons.insert(index, child)
        rearrange_buttons()


def create_button(label):
    btn = HierarchyButton(label)
    buttons.append(btn)
    rearrange_buttons()


# منوی اصلی Create
create_menu = DropdownMenu(
    "Create",
    buttons=[
        DropdownMenuButton("Cube",  onclick=lambda: create_button("Cube")),
        DropdownMenuButton("Plane", onclick=lambda: create_button("Plane")),
        DropdownMenuButton("Quad",  onclick=lambda: create_button("Quad")),
    ],
    position=(-0.7, 0.45)
)

app.run()

# ######################################################################################3

# from ursina import *
# from ursina.prefabs.dropdown_menu import DropdownMenu , DropdownMenuButton


# app = Ursina()

# buttons = []   # لیست دکمه‌ها به ترتیب نمایش


# # ------------------------------

# # تابع چیدمان دوباره دکمه‌ها

# # ------------------------------
# def rearrange_buttons():
#     y = 0.4
#     for b in buttons:
#         if b.visibleinhierarchy:
#             b.y = y
#             y -= 0.1
#             # نمایش فرزندان فقط اگر باز باشند
#             if b.children_visible:
#                 for child in b.children_buttons:
#                     if child.visibleinhierarchy:
#                         child.y = y
#                         y -= 0.1


# # ------------------------------

# # کلاس دکمه‌های هیرارکی

# # ------------------------------
# class HierarchyButton(Button):
#     def init(self, label, parent_button=None, depth=0):
#         super().init(
#             text=label,
#             scale=(0.25, 0.06),
#             x=-0.7 + depth * 0.05,
#             color=color.azure,
#             origin=(-.5, 0)
#         )

#         self.label = label
#         self.parentbutton = parent_button
#         self.children_buttons = []
#         self.children_visible = True
#         self.depth = depth
#         self.dragging = False
#         self.visibleinhierarchy = True

#         # دکمهٔ Hide/Show
#         self.toggle_btn = Button(
#             text='-',
#             scale=(0.03, 0.03),
#             x=self.x - 0.03,
#             y=self.y,
#             color=color.gray
#         )

#         # خط اتصال
#         self.line = Entity(model='line', color=color.white, enabled=False)

#     # ------------------------------
#     #   ورودی‌ها
#     # ------------------------------
#     def input(self, key):
#         # کلیک چپ → چاپ نام
#         if self.hovered and key == "left mouse down":
#             self.dragging = True
#             self.start_y = mouse.y

#         if key == "left mouse up":
#             if self.dragging:
#                 self.dragging = False
#                 self.snaptonew_position()

#         # کلیک راست → باز کردن منوی Add Child
#         if self.hovered and key == "right mouse down":
#             self.openchildmenu()

#         # کلیک روی دکمهٔ Hide/Show
#         if self.toggle_btn.hovered and key == "left mouse down":
#             self.toggle_children()

#     # ------------------------------
#     #   Drag & Drop
#     # ------------------------------
#     def update(self):
#         # آپدیت موقعیت دکمهٔ Hide/Show
#         self.toggle_btn.x = self.x - 0.03
#         self.toggle_btn.y = self.y

#         # رسم خط والد–فرزند
#         if self.parent_button:
#             self.line.enabled = True
#             self.line.position = (self.x + 0.12, self.y, 0)
#             self.line.scaley = abs(self.y - self.parentbutton.y)
#             self.line.rotation_z = 90

#         # درگ کردن
#         if self.dragging:
#             self.y = mouse.y

#     # ------------------------------
#     #   اسنپ کردن بعد از Drag
#     # ------------------------------
#     def snaptonew_position(self):
#         # پیدا کردن نزدیک‌ترین دکمه
#         sorted_buttons = sorted(buttons, key=lambda b: b.y, reverse=True)

#         for i, b in enumerate(sorted_buttons):
#             if self.y > b.y:
#                 buttons.remove(self)
#                 buttons.insert(i, self)
#                 break

#         rearrange_buttons()

#     # ------------------------------
#     #   ساخت DropdownMenu فرزند
#     # ------------------------------
#     def openchildmenu(self):
#         DropdownMenu(
#             "Add Child",
#             buttons=[
#                 DropdownMenuButton("Cube", onclick=lambda: self.addchild_button("Cube")),
#                 DropdownMenuButton("Plane", onclick=lambda: self.addchild_button("Plane")),
#                 DropdownMenuButton("Quad", onclick=lambda: self.addchild_button("Quad")),
#             ],
#             position=(self.x + 0.3, self.y)
#         )

#     # ------------------------------
#     #   ساخت دکمهٔ فرزند
#     # ------------------------------
#     def addchildbutton(self, label):
#         child = HierarchyButton(label, parent_button=self, depth=self.depth + 1)
#         self.children_buttons.append(child)

#         # درج فرزند در لیست اصلی درست بعد از والد
#         index = buttons.index(self) + 1
#         buttons.insert(index, child)

#         rearrange_buttons()

#     # ------------------------------
#     #   پنهان/نمایش فرزندان
#     # ------------------------------
#     def toggle_children(self):
#         self.childrenvisible = not self.childrenvisible
#         self.togglebtn.text = '+' if not self.childrenvisible else '-'

#         for child in self.children_buttons:
#             child.visibleinhierarchy = self.children_visible

#         rearrange_buttons()


# # ------------------------------

# # ساخت دکمهٔ والد از منوی Create

# # ------------------------------
# def create_button(label):
#     btn = HierarchyButton(label)
#     buttons.append(btn)
#     rearrange_buttons()


# # ------------------------------

# # DropdownMenu اصلی Create

# # ------------------------------
# DropdownMenu(
#     "Create",
#     buttons=[
#         DropdownMenuButton("Cube", onclick=lambda: create_button("Cube")),
#         DropdownMenuButton("Plane", onclick=lambda: create_button("Plane")),
#         DropdownMenuButton("Quad", onclick=lambda: create_button("Quad")),
#     ],
#     position=(-0.7, 0.45)
# )


# app.run()
