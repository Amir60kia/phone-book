import openpyxl
import os

# مسیر پوشه‌ای که فایل‌های اکسل در آن قرار دارند
folder_path = "01"

# پیمایش فایل‌ها در پوشه
for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx"):
        file_path = os.path.join(folder_path, filename)

        # بارگذاری فایل اکسل
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        # پیمایش سلول‌ها برای پیدا کردن متن و تغییر آن
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value and "تاریخ :" in str(cell.value):
                    # استخراج بخش‌های تاریخ
                    parts = cell.value.split(" ")
                    date_parts = parts[-1].split("/")  # جدا کردن سال، ماه، روز

                    # تغییر سال از 1402 به 1403
                    if date_parts[0] == "1402":
                        date_parts[0] = "1403"
                        new_date = "/".join(date_parts)
                        cell.value = f"{parts[0]} {new_date}"

        # تغییر نام فایل و ذخیره آن
        new_filename = filename.replace("1402", "1403")
        new_file_path = os.path.join(folder_path, new_filename)
        workbook.save(new_file_path)

        print(f"فایل {filename} به {new_filename} تغییر نام داده شد و تاریخ در سلول‌ها ویرایش شد.")
