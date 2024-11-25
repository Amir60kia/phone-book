import openpyxl
import os

# مسیر پوشه‌ای که فایل‌های اکسل در آن قرار دارند
folder_path = "01"

# شماره سطر و ستون برای سلول I19
row_number = 19
column_number = 9

# پیمایش فایل‌ها در پوشه
for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx"):
        file_path = os.path.join(folder_path, filename)

        # بارگذاری فایل اکسل
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        # دسترسی به سلول با شماره سطر و ستون
        cell = sheet.cell(row=row_number, column=column_number)
        print(cell.value)

        # بررسی و تغییر محتوا در صورت وجود عبارت "تاریخ : 1402"
        if cell.value and "تاریخ : 1402" in str(cell.value):
            # تغییر سال 1402 به 1403 در متن سلول
            cell.value = cell.value.replace("1402", "1403")

        # تغییر نام فایل و ذخیره آن
        new_filename = filename.replace("1402", "1403")
        new_file_path = os.path.join(folder_path, new_filename)
        workbook.save(new_file_path)

        print(f"فایل {filename} به {new_filename} تغییر نام داده شد و تاریخ در سلول I19 ویرایش شد.")
