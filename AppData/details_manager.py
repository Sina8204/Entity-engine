# data_manager.py
import json
import os

class DataManager:
    def __init__(self, file_path="AppData/details.json"):
        self.file_path = file_path
        #self._load_all()
    
    def set_item(self , **kwargs):
        with open(self.file_path , 'r' , encoding='utf-8') as data_file:
            data = json.load(data_file)
            data["child_items"] = kwargs['child_items']
            with open(self.file_path , 'w' , encoding='utf-8') as details:
                json.dump(data , details , ensure_ascii=False , indent=2)


    def _load_all(self):
        """بارگذاری همه دیکشنری‌ها از فایل"""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # اختصاص به متغیرهای کلاس
                self.project_info = data.get("project_info", {"path": ""})
                self.add_entity_menu = data.get("add_entity_menu", {"sum_menu": []})
        else:
            # مقادیر پیش‌فرض
            self.project_info = {"path": ""}
            self.add_entity_menu = {"sum_menu": []}
            self._save_all()
    
    def _save_all(self):
        """ذخیره همه دیکشنری‌ها در فایل"""
        data = {
            "project_info": self.project_info,
            "add_entity_menu": self.add_entity_menu
        }
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def save(self):
        """ذخیره دستی (برای مواقعی که مستقیم تغییر دادید)"""
        self._save_all()
    
    def reload(self):
        """بارگذاری مجدد از فایل"""
        self._load_all()

# ایجاد نمونه سراسری
data_manager = DataManager()