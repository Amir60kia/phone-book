import sqlite3

# ایجاد اتصال به پایگاه داده
conn = sqlite3.connect('phonebook.db')

# ایجاد جدول‌ها
conn.execute('''
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    lastname TEXT,
    phone TEXT,
    email TEXT,
    unit TEXT,
    mobile TEXT,
    company TEXT
    
)
''')

# بستن اتصال
conn.close()

print("Database and table created successfully.")
