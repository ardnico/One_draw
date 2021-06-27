# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import threading
import string
import time
import os
import shutil
import subprocess
import tkinter as tk
import tkinter.font as font
import tkinter.ttk as ttk
from tqdm import tqdm
from datetime import datetime as dt
from glob import glob
from playsound import playsound


# %%
# import pyautogui

# screenshot = pyautogui.screenshot()
# screenshot.save(r"sample.png")


# %%
open_voice = glob("voice\start*")
end_voice = glob("voice\end*")
s_rand_num = (int(dt.now().strftime('%Y%m%d%H%M%S')) % len(open_voice))
e_rand_num = (int(dt.now().strftime('%Y%m%d%H%M%S')) % len(end_voice))


# %%
# give a theme
print("Theme installing now.........")
print("\n")
for i in tqdm(range(5)):
    time.sleep(0.5)
text_data = [i for i in glob(r"theme\*.txt") if i.find("_")==-1]
target_list = []
for t in text_data:
    try:
        try:
            with open(t,"r",encoding='utf-8') as f:
                tmp_line = f.read()
        except:
            with open(t,"r",encoding='shift-jis') as f:
                tmp_line = f.read()
    except:
        waiting = input("お題テキストの文字コードがANSI、UTF-8以外となってます\n 文字コードを変更して格納してください\n処理を終了します：")
        sys.exit()
    target_list += tmp_line.split("\n")
rand_num = (int(dt.now().strftime('%Y%m%d%H%M%S')) % len(target_list))
print("\n------------------------\n")
print(target_list[rand_num])
print("\n------------------------\n")


# %%
# 環境変数の取得
for i in range(28,len(string.ascii_letters)):
    test_path = glob(rf"{string.ascii_letters[i]}:\Program*\CELSYS\**\CLIPStudioPaint.exe",recursive=True)
    if len(test_path) > 0:
        clip_studio = test_path[0]
        break
    else:
        clip_studio = "manual_launch"
# Clipstudioの起動関数
def lounch_cs():
    todate = dt.now().strftime("%Y%m%d")
    old_data = glob(fr"{os.getcwd()}\drawdata\1h_draw_{todate}_???.clip")
    file_num = 0
    if len(old_data) > 0:
        file_num = len(old_data)
    copy_file = fr"{os.getcwd()}\drawdata\1h_draw_{todate}_{str(file_num).zfill(3)}.clip"
    shutil.copy(fr"{os.getcwd()}\1h_draw_format.clip",copy_file)
    subprocess.run([clip_studio,copy_file],check=False)
if clip_studio == "manual_launch":
    print("CLIP Studio が見当たりませんでした。申し訳ないですが手動でペイントソフトを起動してください")
else:
    csthread = threading.Thread(target=lounch_cs)
    csthread.start()


# %%
# timer部分

root=tk.Tk()
root.title("Timer")
text_sec=tk.StringVar()
text_sec.set("0")
my_font=font.Font(size=20)

text_min=tk.StringVar()
text_min.set("60")

buff_min=tk.StringVar()
buff_min.set("0")

buff_sec=tk.StringVar()
buff_sec.set("0")

text_start_stop=tk.StringVar()
text_start_stop.set("START")

progressbar=ttk.Progressbar(root,orient="horizontal",length=230,mode="determinate")
progressbar.grid(row=2,column=0,columnspan=7)

start=True
check=True
stop=False

def start():
    global start,check,text_min,text_sec,start,check,stop,value_time
    start=False
    if check==True and stop==True:
        start=True
        text_start_stop.set("STOP")
        timer()
    
    elif check==False and stop==True:
        count_min=int(buff_min.get())
        count_sec=int(buff_sec.get())
        buff_min.set("0")
        buff_sec.set("0")
        buff_min.set(count_min)
        buff_sec.set(count_sec)
        check=True
        text_start_stop.set("START")
        
    else:
        start=True
        stop=True
        text_start_stop.set("STOP")
        buff_min.set(int(text_min.get()))
        buff_sec.set(int(text_sec.get()))
        maximum_time=int(buff_min.get())*60+int(buff_sec.get())
        #print(maximum_time)
        value_time=0
        div_time=1
        progressbar.configure(maximum=maximum_time,value=value_time)
        timer()
    
        

def timer():
    global start,buff_min,buff_sec,text_min,text_sec,check,value_time,div_time
    if start==True:
        if int(buff_min.get())==0 and int(buff_sec.get())==0:
            pass
        else:
            check=False
            time_min=int(buff_min.get())
            time_sec=int(buff_sec.get())
            if time_min>=0:
                time_sec-=1
                buff_sec.set(str(time_sec))
                value_time+=1
                progressbar.configure(value=value_time)
                root.after(1000,timer)
                if time_sec==-1:
                    time_min-=1
                    buff_min.set(str(time_min))
                    buff_sec.set("59")
            if int(buff_min.get())==0 and int(buff_sec.get())==0:
                start=False
                time_min=0
                time_sec=0
                buff_sec.set(str(time_sec))
                buff_min.set(str(time_min))
                playsound(end_voice[e_rand_num])
                

            
def stop():
    global start,check,stop
    start=True
    check=True
    stop=False
    time_min=0
    time_sec=0
    buff_sec.set(str(time_sec))
    buff_min.set(str(time_min))

labbel=tk.Label(root,text="設定")
labbel.grid(row=0,column=0,columnspan=1)
    
entry=tk.Entry(root,width=2,font=my_font,textvariable=text_min)
entry.grid(row=0,column=1)

label_min=tk.Label(root,text=u"分")
label_min.grid(row=0,column=2)

entry1=tk.Entry(root,width=2,font=my_font,textvariable=text_sec)
entry1.grid(row=0,column=3)

label_sec=tk.Label(root,text=u"秒")
label_sec.grid(row=0,column=4)

button=tk.Button(root,textvariable=text_start_stop,command=start)
button.grid(row=0,column=5)

button=tk.Button(root,text=u"RESET",command=stop)
button.grid(row=0,column=6)

labbel=tk.Label(root,text="タイマー")
labbel.grid(row=1,column=0,columnspan=1)

labbel=tk.Label(root,font=my_font,textvariable=buff_min)
labbel.grid(row=1,column=1,columnspan=1)

labbel=tk.Label(root,text="分")
labbel.grid(row=1,column=2,columnspan=1)

labbel=tk.Label(root,font=my_font,textvariable=buff_sec)
labbel.grid(row=1,column=3,columnspan=1)

labbel=tk.Label(root,text="秒")
labbel.grid(row=1,column=4,columnspan=1)

playsound(open_voice[s_rand_num])
root.mainloop()


# %%



# %%



# %%



# %%



# %%



