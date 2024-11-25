from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('phonebook.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    contacts = []
    if request.method == 'POST':
        search_query = request.form['search']
        contacts = conn.execute('''  
            SELECT * FROM contacts  
            WHERE LOWER(name) LIKE ?  
            OR LOWER(lastname) LIKE ?  
            OR LOWER(phone) LIKE ?  
            OR LOWER(email) LIKE ?  
            OR LOWER(unit) LIKE ?  
            OR LOWER(mobile) LIKE ?
            OR LOWER(company) LIKE ? 
            
        ''', ('%' + search_query.lower() + '%',) * 7).fetchall()
        conn.close()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']
        unit = request.form['unit']
        mobile = request.form['mobile']
        company =request.form['company']

        conn = get_db_connection()
        # existing_contact = conn.execute('''
        #            SELECT * FROM contacts
        #            WHERE phone = ? OR email = ? OR mobile = ?
        #        ''', (phone, email, mobile)).fetchone()
        #
        # if existing_contact:
        #     error = 'این شماره داخلی، ایمیل یا شماره موبایل قبلاً ثبت شده است.'
        #     conn.close()
        #     return render_template('add.html', error=error)  # نمایش پیام خطا

        conn.execute('INSERT INTO contacts (name,lastname, phone, email, unit, mobile, company) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (name, lastname, phone, email, unit, mobile, company))
        conn.commit()
        conn.close()
        return redirect(url_for('indexadmin'))

    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    contact = conn.execute('SELECT * FROM contacts WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        phone = request.form['phone']
        email = request.form['email']
        unit = request.form['unit']
        mobile = request.form['mobile']
        company = request.form['company']

        conn.execute('''
            UPDATE contacts SET name = ?, lastname = ?, phone = ?, email = ?, unit = ?, mobile = ?, company = ?
            WHERE id = ?
        ''', (name, lastname, phone, email, unit, mobile, company, id))
        conn.commit()
        conn.close()
        return redirect(url_for('indexadmin'))

    conn.close()
    return render_template('edit.html', contact=contact)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contacts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('indexadmin'))



# @app.route('/indexadmin')
# def indexadmin():
#     return render_template('indexadmin.html')  # اینجا صفحه دیگری ایجاد خواهیم کرد.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # با توجه به اطلاعات شما، username و password را بررسی کنید.
        # اینجا ما یک مقدار ثابت برای نمایش می‌گذاریم.
        if username == 'admin' and password == 'password':  # اینجا باید اعتبارسنجی واقعی انجام دهید
            return redirect(url_for('indexadmin'))

            # اگر کاربر معتبر نبود، می‌توانید یک پیام خطا نمایش دهید
        error = 'نام کاربری یا رمز عبور اشتباه است.'
        return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/indexadmin', methods=['GET', 'POST'])
def indexadmin():
    conn = get_db_connection()
    contacts = []

    if request.method == 'POST':
        search_query = request.form['search']
        contacts = conn.execute('''  
            SELECT * FROM contacts  
            WHERE LOWER(name) LIKE ?  
            OR LOWER(lastname) LIKE ?  
            OR LOWER(phone) LIKE ?  
            OR LOWER(email) LIKE ?  
            OR LOWER(unit) LIKE ?  
            OR LOWER(mobile) LIKE ?
            OR LOWER(company) LIKE ? 
        ''', ('%' + search_query.lower() + '%',) * 7).fetchall()
        conn.close()
        return render_template('indexadmin.html', contacts=contacts)

    conn.close()
    return render_template('indexadmin.html', contacts=[])


@app.route('/upload_excel', methods=['GET', 'POST'])
def upload_excel():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "فایل موجود نیست"
        file = request.files['file']
        if file.filename == '':
            return "نام فایل ارسال نشده است"

            # برای اطمینان از اینکه نوع فایل درست است
        if not file.filename.endswith('.xlsx'):
            return "فقط فایل‌های اکسل قابل قبول است."

            # خواندن فایل اکسل
        df = pd.read_excel(file)

        # ایجاد اتصال به پایگاه داده
        conn = get_db_connection()

        # درج داده‌ها در پایگاه داده
        for index, row in df.iterrows():
            # existing_contact = conn.execute('''
            #     SELECT * FROM contacts
            #     WHERE phone = ? OR email = ? OR mobile = ?
            # ''', (row['phone'], row['email'], row['mobile'])).fetchone()
            #
            # if not existing_contact:
                conn.execute(
                    'INSERT INTO contacts (name, lastname, phone, email, unit, mobile, company) VALUES (? ,?, ?, ?, ?, ?, ?)',
                    (row['name'], row['lastname'], row['phone'], row['email'], row['unit'], row['mobile'], row['company']))

        conn.commit()
        conn.close()
        return redirect(url_for('indexadmin'))

    return render_template('upload_excel.html')  # ایجاد یک template جدید برای بارگذاری فایل


if __name__ == '__main__':
    app.run(debug=True)
