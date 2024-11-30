# import secrets
# import string
from tkinter import Tk, TclError
from time import sleep
import requests
# import rsa
# import json
import argparse

from pynput import keyboard
import pyautogui as pya

from cryptography.fernet import Fernet
# import json

import time

from selectedtext import get_selected_text_from_front_window


# https://www.geeksforgeeks.org/convert-python-script-to-exe-file/
# pip install pyinstaller
# pyinstaller --onefile -w 'avastui.py'
# https://stackoverflow.com/questions/25733467/no-module-named-when-using-pyinstaller
# cd W:\Dateien\_generatum\Projekte\Python
# pyinstaller --paths=subfolder python-avastui/avastui.py
# START /B "" W:\Dateien\_generatum\Projekte\Python\dist\avastui\avastui.exe
# https://superuser.com/questions/1069972/windows-run-process-on-background-after-closing-cmd
# W:\Dateien\_generatum\Projekte\Python\python-avastui\hide_current_console.exe & exit
# https://www.nirsoft.net/utils/nircmd.html
# W:\Dateien\_generatum\Projekte\Python\python-avastui\nircmd-x64\nircmd.exe execmd W:\Dateien\_generatum\Projekte\Python\dist\avastui\avastui.exe

# def getClipboardText():
#    root = tk.Tk()
#    # keep the window from showing
#    # root.withdraw()
#    root.quit()
#    return root.clipboard_get()

# r = tkinter.Tk()
# text = r.clipboard_get()
# r.withdraw()
# r.update()
# r.destroy()

# https://gist.github.com/ostinelli/aeebf4643b7a531c248a353cee8b9461
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives.asymmetric import rsa
# save file helper
#def save_file(filename, content):
#    f = open(filename, "wb")
#    f.write(content)
#    f.close()
# generate private key & write to disk
#private_key = rsa.generate_private_key(
#    public_exponent=65537,
#    key_size=4096,
#    backend=default_backend()
#)
#pem = private_key.private_bytes(
#    encoding=serialization.Encoding.PEM,
#    format=serialization.PrivateFormat.PKCS8,
#    encryption_algorithm=serialization.NoEncryption()
#)
#save_file("private.pem", pem)
## generate public key
#public_key = private_key.public_key()
#pem = public_key.public_bytes(
#    encoding=serialization.Encoding.PEM,
#    format=serialization.PublicFormat.SubjectPublicKeyInfo
#)
#save_file("public.pem", pem)

# api_key = os.environ.get("GROQ_API_KEY")
# api_key = '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'
# url = "https://api.groq.com/openai/v1/models"
# headers = {
#     "Authorization": f"Bearer {api_key}",
#     "Content-Type": "application/json"
# }
# response = requests.get(url, headers=headers)
# print(response.json())

def on_press(key):
    # try:
    #     print('alphanumeric key {0} pressed'.format(
    #         key.char))
    # except AttributeError:
    #     print('special key {0} pressed'.format(
    #         key))
    global insertPressed
    global start
    global keyboardString
    if insertPressed == 1:
        if key == keyboard.Key.backspace:
            #print('backspace')
            keyboardString = str(keyboardString).replace("'", "").replace("Key.space", " ").replace("Key.shift_r", "").replace("Key.shift_l", "").replace("Key.insert", "")
            keyboardString = keyboardString[:-1]
        else:
            #print('other key')
            keyboardString += str(key)
    if key == keyboard.Key.insert:
        insertPressed += 1
        if insertPressed == 1:
            start = time.perf_counter()
        if insertPressed == 2:
            stop = time.perf_counter()
            if stop - start < 1:
                #pya.hotkey("ctrl", "c") # copy the text (simulating key strokes)
                root = Tk()
                root.withdraw()
                root.clipboard_clear()
                root.clipboard_append(str(get_selected_text_from_front_window()))
                root.update()
                insertPressed = 0
            if stop - start > 1:
                root = Tk()
                root.withdraw()
                root.clipboard_clear()
                keyboardString = str(keyboardString).replace("'", "").replace("Key.space", " ").replace("Key.shift_r", "").replace("Key.shift_l", "").replace("Key.insert", "")
                #print('keyboardString: ' + keyboardString)
                root.clipboard_append(str(keyboardString))
                root.update()
                keyboardString = ""
                insertPressed = 0

def on_release(key):
    return True
    # print('key released')
    # print('{0} released'.format(key))
    # if key == keyboard.Key.insert:
    #     # Stop listener
    #     return False

# https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

parser = argparse.ArgumentParser()
parser.add_argument("vendor", help="Specify the vendor of the model to use.", nargs='?', type=str, const='groq', default='groq')
parser.add_argument("model", help="Specify the model to use.", nargs='?', type=str, const='llama-3.1-70b-versatile', default='llama-3.1-70b-versatile')
parser.add_argument("system", help="Specify the system query to use.", nargs='?', type=str,
                    const='You are an anti money laundering expert. To pass an exam at a university, which is important for your career, you must comprehensively answer or explain the following query.',
                    default='You are an anti money laundering expert. To pass an exam at a university, which is important for your career, you must comprehensively answer or explain the following query.')
args = parser.parse_args()
# print(args)

insertPressed = 0
start = time.perf_counter()
keyboardString = ""


# Collect events until released
# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#   listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(on_press=on_press) #  on_release=on_release)
listener.start()

# key = Fernet.generate_key()
# print(key.decode()) # cNkXmbsNUoAyyLx9bR8HMcj_5JaDNq42Bz_YDXcf3t4=

clipboard_before = ""
while True:
    try:

        # secret = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        # print('secret: ' + secret)

        clipboard = Tk().clipboard_get()
        # print('clipboard content: ' + clipboard)

        if clipboard != clipboard_before and clipboard != "":

            # https://stackoverflow.com/questions/20706783/put-byte-array-to-json-and-vice-versa
            token = encrypt(clipboard.encode(), 'cNkXmbsNUoAyyLx9bR8HMcj_5JaDNq42Bz_YDXcf3t4='.encode()).decode()
            # print('token: ' + token)

            # print('clipboard: content changed')
            # print('invoke API')
            # encClipboard = rsa.encrypt(clipboard.encode(), public_key)
            # print(encClipboard)
            # https://nelson.cloud/invoking-amazon-api-gateway-with-an-api-key/
            # url = "https://12abcde45.execute-api.us-west-1.amazonaws.com/prod/create"
            url = "https://u1enyzfj5e.execute-api.eu-central-1.amazonaws.com/prod"
            # API key specified as a header
            # Key hardcoded for demonstrational purposes. Do not push/commit plaintext keys!
            # headers = {"x-api-key": "abc123"}
            headerAuthKey = "authorizationToken"
            headerAuthValue = "api-chatgpt-ac3e320f7adac9065bdbf711a08f09fc0a57a711"
            headers = {"Content-Type" : "application/json", headerAuthKey : headerAuthValue}
            # Data to be sent
            # data = {'question': str(encClipboard)}
            # system = "You are an anti money laundering expert. To pass an exam at a university, which is important for your career, you must answer or explain the following query."
            data = {'vendor' : args.vendor, 'model' : args.model, 'system' : args.system, 'query': token}
            # data = {'question': 'explain risk based approach'}
            # data_json = json.dumps(data)
            # POST request with custom header and data
            response = requests.post(url, json=data, headers=headers)
            # print(response.status_code)
            # print(response.json())
        # else:
            # print('clipboard: content no change')

        sleep(5)
        clipboard_before = clipboard

    except TclError:
        # print('clipboard: TclError, clipboard is empty')
        sleep(5)





#cmb = [{keyboard.Key.shift, keyboard.Key(char='a')},{keyboard.Key.shift, keyboard.Key(char='A')}]
#current = set()

#def execute():
#    print("Detected hotkey")

#def on_press(key):
#    if any([key in z for z in cmb]):
#        current.add(key)
#        if any(all(k in current for k in z) for z in cmb):
#            execute()

#def on_release(key):
#    if any([key in z for z in cmb]):
#        current.remove(key)
#    if key == keyboard.Key.esc:
#        # Stop listener
#        return False

#with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#    listener.join()

# What is AML/CFT?
# What is FATF?
# What is the CSSF?

