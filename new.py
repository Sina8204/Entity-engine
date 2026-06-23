import os
from pprint import pprint


def build_directory_tree(path: str) -> dict:
    """
    ساختار درختی پوشه و فایل‌ها را به صورت دیکشنری برمی‌گرداند.
    """
    tree = {}
    
    try:
        # لیست تمام آیتم‌های داخل مسیر
        items = sorted(os.listdir(path))  # مرتب‌سازی برای نمایش زیباتر
        
        for item in items:
            item_path = os.path.join(path, item)
            
            if os.path.isdir(item_path):
                # اگر پوشه بود، به صورت بازگشتی درختش را بساز
                tree[item] = build_directory_tree(item_path)
            else:
                # اگر فایل بود، می‌توانی اطلاعات بیشتری هم ذخیره کنی
                tree[item] = "📄 file"   # یا None یا اندازه فایل و ...
                
    except PermissionError:
        tree["🚫"] = "دسترسی غیرمجاز"
    except FileNotFoundError:
        tree["❌"] = "مسیر یافت نشد"
    except Exception as e:
        tree["⚠️"] = f"خطا: {str(e)}"
    
    return tree


def print_tree(path: str = "."):
    """درخت را ساخته و چاپ می‌کند"""
    print(f"🌳 ساختار درختی مسیر: {os.path.abspath(path)}\n")
    tree = build_directory_tree(path)
    pprint(tree, indent=2, width=80, sort_dicts=False)


# ====================== استفاده ======================
if __name__ == "__main__":
    # مسیر دلخواهت را اینجا بگذار (پیش‌فرض: پوشه فعلی)
    target_path = "project"          # یا مثلاً "/home/user/Documents"
    # target_path = "/path/to/your/folder"
    
    print_tree(target_path)