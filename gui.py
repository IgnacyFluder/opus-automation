
from tkinter.ttk import Progressbar
from tkinter import *
from tkinter import messagebox
from resources import *
import subprocess
import tkinter
import webbrowser
import inspect
import sequence
import threading
import uploader

reel = uploader.Reel(
    FB_CREDENTIALS['client_id'],
    FB_CREDENTIALS['client_secret'],
    FB_CREDENTIALS['access_url'],
    FB_CREDENTIALS['page_id']
)
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def save_settings():
    with open('resources.py', 'w') as config_file:
        config_file.write("from selenium.common.exceptions import NoSuchElementException\nfrom selenium.common.exceptions import StaleElementReferenceException\nfrom selenium.common.exceptions import ElementClickInterceptedException\n")
        config_file.write("#Any modifications to this file may cause the program to not work properly, please use the ui to change settings\n###########RESOURCES#############\n")
        for i in range(len(SETTER)):
            try:
                if SETTER_TYPES[i] == str:
                    config_file.write(f"{SETTER_NAMES[i]} = '{SETTER[i]}'\n")
                elif SETTER_TYPES[i] == bool:
                    config_file.write(f"{SETTER_NAMES[i]} = {str(SETTER[i].get())}\n")
                else:
                    config_file.write(f"{SETTER_NAMES[i]} = {str(SETTER[i])}\n")
            except AttributeError:
                config_file.write(f"{SETTER_NAMES[i]} = {str(SETTER[i])}\n")
        config_file.write("IGNORED_EXCEPTIONS=(NoSuchElementException,StaleElementReferenceException,ElementClickInterceptedException,)\n")
        config_file.write("SETTER = [DOMAIN_LIST, TIMEOUT, PROXY_TYPE, PAID_PROXY_BACKBONE, DO_SLEEP]\nSETTER_NAMES = ['DOMAIN_LIST', 'TIMEOUT', 'PROXY_TYPE', 'PAID_PROXY_BACKBONE', 'DO_SLEEP']\nSETTER_HINTS = ['List of domains to use for email creation', 'Timeout for selenium(to this is added from 0.1 to 0.9 more seconds for more security)', 'Proxy type', 'Proxy backbone', 'Sleep between actions']\nSETTER_TYPES = [list, int, str, str, bool]\n")
        config_file.write("""FB_CREDENTIALS = {"""+f"""
    'client_id':'{str(FB_CREDENTIALS['client_id'])}',
    'client_secret':'{FB_CREDENTIALS['client_secret']}',
    'access_url':'{FB_CREDENTIALS['access_url']}',
    'page_id':'{FB_CREDENTIALS['page_id']}'"""+"""
}""")
    messagebox.showinfo('Settings saved', 'Your settings have been successfully saved!')

root = tkinter.Tk()
root.title('Opus automation')

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

def open_settings_popup():
    top= Toplevel(root)
    top.geometry("300x250")
    top.resizable(False, False)
    top.title("Config")

    input_list = []

    for i in range(len(SETTER)):
        pw = PanedWindow(top)
        pw.pack(expand = 1)

        if len(SETTER_NAMES[i]) < 20:
            while len(SETTER_NAMES[i]) < 20:
                SETTER_NAMES[i] += " "

        if SETTER_TYPES[i] == bool:
            var = BooleanVar(value=False)
            if SETTER[i] == True:
                var.set(True)
            
            print(var.get())
            lab = Label(top, text=SETTER_NAMES[i])
            inpu = Checkbutton(top, bd = 7, onvalue=True, offvalue=False, variable=var)
            
            
            input_list.append(var)
        else:
            lab = Label(top, text=SETTER_NAMES[i])
            inpu = Entry(top, bd = 5)
            inpu.insert(0, SETTER[i])
            input_list.append(inpu)

        CreateToolTip(inpu, SETTER_HINTS[i]+ " | "+str(SETTER_TYPES[i]))

        pw.add(lab)
        pw.add(inpu)
    
    def save():
        for i in range(len(SETTER)):
            if SETTER_TYPES[i] == bool:
                SETTER[i] = input_list[i]
            elif SETTER_TYPES[i] == int:
                SETTER[i] = int(input_list[i].get())
            elif SETTER_TYPES[i] == str:
                SETTER[i] = str(input_list[i].get())
            elif SETTER_TYPES[i] == list:
                SETTER[i] = str(input_list[i].get()).split(",")
        save_settings()
        top.destroy()
        
    button = Button(top, text='Save', width=25, bg="grey", command=save)
    button.pack()

def open_auth_popup():
    top= Toplevel(root)
    top.resizable(False, False)
    top.geometry("300x250")
    top.title("Auth settings")

    input_list = []

    for fb_credential in FB_CREDENTIALS:
        pw = PanedWindow(top)
        pw.pack(expand = 1)

        lab = Label(top, text=fb_credential)
        inpu = Entry(top, bd = 5)
        inpu.insert(0, FB_CREDENTIALS[fb_credential])
        CreateToolTip(inpu, fb_credential+" for more info visit https://developers.facebook.com/docs/instagram-api/getting-started")

        pw.add(lab)
        pw.add(inpu)
        input_list.append(inpu)
    
    def save():
        count = 0
        for facebook_credential in FB_CREDENTIALS:
            FB_CREDENTIALS[facebook_credential] = input_list[count].get()
            count += 1
        save_settings()
        top.destroy()
    

    button = Button(top, text='Save', width=25, bg="grey", command=save)
    button.pack()

def redirect_to_gh():
    webbrowser.open_new_tab('https://github.com/IgnacyFluder/opus-automation')

def open_yopmail():
    # Windows
    def _i():
        try:
            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open('https://yopmail.com/wm')
        except:
            webbrowser.open_new_tab('https://yopmail.com/wm')
    th = threading.Thread(target=_i)
    th.start()
    

def start_normal(url, reel, headless=False):
    th = threading.Thread(target=sequence.run, args=([url], headless, reel))
    messagebox.showinfo("Running", "Thread is running, for progress see command line.")
    th.start()

def start_raw(url, reel, headless=False):
    th = threading.Thread(target=sequence.run_raw, args=([url], headless, reel))
    messagebox.showinfo("Running(raw)", "Thread is running, for progress see command line.")
    th.start()


# context menu
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label='Settings', menu=filemenu)
filemenu.add_command(label='Config', command=open_settings_popup)
filemenu.add_command(label='Facebook auth', command=open_auth_popup)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.quit)
helpmenu = Menu(menu)
menu.add_cascade(label='About', menu=helpmenu)
helpmenu.add_command(label='Github repo', command=redirect_to_gh)

# main frame
ourMessage ='Welcome to the OPUS.PRO auto uploader!'
messageVar = Message(root, text = ourMessage)
messageVar.config(bg='lightgreen')
messageVar.pack(expand = 1)

w = Label(root, text='insert video link')
inpu = Entry(root, bd = 5)

w.pack()
inpu.pack()


m2 = PanedWindow()
startbtn = Button(root, text='start automation', width=25, bg="blue", command=lambda: start_normal(inpu.get(), reel=reel, headless=True))
rawbtn = Button(root, text='start raw automation', width=20, bg="grey", command=lambda: start_raw(inpu.get(), reel=reel, headless=True))
removebtn = Button(root, text='kill all chrome processes', width=47, bg="red", command=sequence.remove_chrome)
yopbtn = Button(root, text='open yopmail.com', width=47, bg="grey", command=open_yopmail)


m2.add(startbtn)
m2.add(rawbtn)

m2.pack()
removebtn.pack()
yopbtn.pack()

w = Label(root, text='for more info about the program visit the about section')
w.pack()


root.mainloop()
#run(['https://youtu.be/7doXTqVp16g'], headless=True)