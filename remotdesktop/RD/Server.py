import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)

print("Server is listening...")
while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} has been established!")
    client_socket.send(b"Welcome to the remote desktop!")
    client_socket.close()


import time
from PIL import ImageGrab
import io

def send_live_screen(client_socket):
    while True:
        screenshot = ImageGrab.grab()
        byte_arr = io.BytesIO()
        screenshot.save(byte_arr, format='PNG')
        client_socket.sendall(byte_arr.getvalue())
        time.sleep(0.1)  # تنظیم فواصل ارسال

from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

def on_click(x, y, button, pressed):
    # ارسال اطلاعات کلیک ماوس به سرور
    pass

def on_press(key):
    # ارسال اطلاعات کلید فشرده شده به سرور
    pass

# شروع گوش دادن به ورودی‌ها
with MouseListener(on_click=on_click) as mouse_listener, KeyboardListener(on_press=on_press) as keyboard_listener:
    mouse_listener.join()
    keyboard_listener.join()