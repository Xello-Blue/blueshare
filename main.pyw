import customtkinter as ctk
import win10toast
import requests
import json
import pyautogui
import pyperclip
import threading

#FUNCTIONS

def toast(msg):
    try:
        toaster = win10toast.ToastNotifier()
        toaster.show_toast(
        "BlueShare",
        msg,
        duration = 3,
        icon_path = "icon.png",
        threaded = True,
        )
    except Exception as err:
        print(f"TOASTERROR: {err}")

def get_config():
    return json.loads( open("data/current.cfg", "r", encoding="utf-8").read() )

def get_settings():
    return json.loads( open("data/app.cfg", "r", encoding="utf-8").read() )


def check_config_contents(cfg):
    keys = ["Headers", "Name"]
    for x in keys:
        try:
            cfg[x]
        except:
            return False
    return True

def load_config():
    path = cfgPath.get()
    try:
        config = json.loads(open(path, "r", encoding="utf-8").read())
        if check_config_contents(config):
            open("data/current.cfg", "w").write(json.dumps(config, indent=2))
            toast(f"Config loaded")
        else:
            toast("Invalid config provided")
    except:
        toast("Path does not exist")

def upload_screenshot():
    ss = pyautogui.screenshot()
    ss.save("data/latest.png")
    
    with open("data/latest.png", "rb") as f:
        files = {"image": f}
        r = requests.post("https://xello.blue/upload", headers=get_config()["Headers"], files=files)
        if r.status_code == 200:
            toast("Screenshot Uploaded")
            pyperclip.copy(json.loads(r.content)["imageUrl"])
        else:
            try: toast(json.loads(r.content)["error"])
            except: toast("Upload Error: Failed to connect")

def key_capture(event):
    if event.char == get_settings()["hotkey"]:
        print("[DEBUG] HOTKEY CAPTURED!")
        upload_screenshot()
    else:
        print(f"[DEBUG] Pressed Char: {event.char}")

#GUI
root = ctk.CTk()
root.bind("<Key>", key_capture)


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root.geometry("500x400")
root.title("BlueShare")
root.iconbitmap("icon.png")

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

label = ctk.CTkLabel(master=frame, text="BlueShare", font=("Roboto", 24))
label.pack(pady=10,padx=12)

cfgFrame = ctk.CTkFrame(master=frame)
cfgFrame.pack(pady=20, padx=20)

cfgTitle = ctk.CTkLabel(master=cfgFrame, text="Config", font=("Roboto", 16))
cfgTitle.pack(pady=10, padx=12)

cfgPath = ctk.CTkEntry(master=cfgFrame, placeholder_text="Path to config")
cfgPath.pack(pady=10, padx=12)

cfgLoad = ctk.CTkButton(master=cfgFrame, text= "Load" if open("data/current.cfg","r", encoding="utf-8").read() == "" else "Update", command=load_config)
cfgLoad.pack(pady=10, padx=12)

screenshot_now = ctk.CTkButton(master=frame, text="Screenshot", command=upload_screenshot)
screenshot_now.pack(pady=10, padx=12)

threading.Thread(target=key_capture).start()

root.mainloop()