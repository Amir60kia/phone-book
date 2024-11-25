import sqlite3

conn = sqlite3.connect('phonebook.db')
cursor = conn.cursor()

# افزودن اطلاعات
cursor.execute('''ALTER TABLE contacts ADD COLUMN company VARCHAR(255);

''')

# ذخیره تغییرات
conn.commit()

# بستن اتصال
conn.close()

print("Contact added successfully.")
