from flask import Flask, request, redirect, url_for, session, render_template_string
import pyautogui

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # این مقدار را به صورت تصادفی و پیچیده تعیین کنید

# کاربران مجاز
users = {'username': 'password'}  # نام کاربری و کلمه عبور


@app.route('/')
def index():
    return render_template_string('''  
        <form method="POST" action="/login">  
            <input type="text" name="username" placeholder="Username" required>  
            <input type="password" name="password" placeholder="Password" required>  
            <button type="submit">Login</button>  
        </form>  
    ''')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        session['username'] = username
        return redirect(url_for('control'))
    return 'Invalid credentials', 401


@app.route('/control')
def control():
    if 'username' not in session:
        return redirect(url_for('index'))

    return render_template_string('''  
        <h1>Control Panel</h1>  
        <form method="POST" action="/screenshot">  
            <button type="submit">Take Screenshot</button>  
        </form>  
        <form method="POST" action="/logout">  
            <button type="submit">Logout</button>  
        </form>  
    ''')


@app.route('/screenshot', methods=['POST'])
def screenshot():
    if 'username' not in session:
        return redirect(url_for('index'))

    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')
    return 'Screenshot taken and saved!'


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)