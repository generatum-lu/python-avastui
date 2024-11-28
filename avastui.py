# import secrets
# import string
from tkinter import Tk, TclError
from time import sleep
import requests
import rsa
import json
from Crypto.PublicKey import RSA

from pynput import keyboard

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



key_pair = RSA.generate(2048)
public_key = key_pair.publickey().exportKey()
private_key = key_pair.exportKey()
print(public_key)
print(private_key)


clipboard_before = ""
while True:
    try:

        # secret = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        # print('secret: ' + secret)

        clipboard = Tk().clipboard_get()
        print('clipboard content: ' + clipboard)

        if clipboard != clipboard_before and clipboard != "":
            print('clipboard: content changed')
            print('invoke API')
            encClipboard = ""
            print(encClipboard)
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
            data = {'question': str(encClipboard)}
            encClipboard = ""
            data_json = json.dumps(data)
            # POST request with custom header and data
            response = requests.post(url, json=data, headers=headers)
            print(response.status_code)
            print(response.json())
        else:
            print('clipboard: content no change')

        sleep(5)
        clipboard_before = clipboard

    except TclError:
        print('clipboard: TclError, clipboard is empty')
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


