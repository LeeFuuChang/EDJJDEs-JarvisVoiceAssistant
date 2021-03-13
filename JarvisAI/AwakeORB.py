from tkinter.ttk import *
from pyautogui import *
from PIL import ImageTk
from tkinter import *
import tkinter as tk
import threading
import psutil
import time
import PIL
import os

path = os.getcwd()

AssistantTopWindow = tk.Tk()
AssistantTopWindow.title("Assistant")
AssistantTopWindow.geometry("300x300+1748+780")
AssistantTopWindow.configure(bg='black')
AssistantTopWindow.overrideredirect(1)
AssistantTopWindow.wm_attributes("-topmost", 1)
AwakeSoundOrbFrame = tk.Frame(AssistantTopWindow)
Orbimg = ImageTk.PhotoImage(PIL.Image.open(path+r"\sirilike\pic00.png"))
AwakeSoundOrbLabel = tk.Label(AwakeSoundOrbFrame,image=Orbimg,width=300,height=250)
AwakeSoundOrbLabel.image = Orbimg
AwakeSoundOrbFrame.pack(side=tk.TOP)
AwakeSoundOrbLabel.pack(side=tk.TOP)
RAMFrame = tk.Frame(AssistantTopWindow, bg="black")
RAMFrame.pack(side=tk.LEFT, anchor=E)
DateTimeFrame = tk.Frame(AssistantTopWindow, bg="black")
DateTimeFrame.pack(side=tk.RIGHT, anchor=E)
TimeLabel = tk.Label(DateTimeFrame, bg="black", fg="white")
TimeLabel.pack(side=tk.TOP, anchor=N)
DateLabel = tk.Label(DateTimeFrame, bg="black", fg="white")
DateLabel.pack(side=tk.TOP, anchor=S)
RAMBarTitle = tk.Label(RAMFrame, bg="black", fg="white")
RAMBarTitle.pack(side=tk.TOP, anchor=N)
RAMBar = Progressbar(RAMFrame, orient=HORIZONTAL, length=225, mode="determinate")
RAMBar.pack(side=tk.TOP, anchor=S)
def UpDateRAM():
    RAMinfo = list(psutil.disk_usage('C:'))
    Percent = round((RAMinfo[1]/RAMinfo[0])*100)
    RAMBar["value"] = Percent
    RAMBarTitle.config(text="RAM Used: "+str(Percent)+"%")
    RAMFrame.update_idletasks()
    AssistantTopWindow.after(60000,TopLevelImage)
def TopLevelImage():
    global i
    try:
        Orbimg = ImageTk.PhotoImage(PIL.Image.open(path+r"\sirilike\pic"+"{:0>2}".format(str(i))+r".png"))
        AwakeSoundOrbLabel.config(image=Orbimg)
        AwakeSoundOrbLabel.image = Orbimg
        AssistantTopWindow.after(30,TopLevelImage)
        i+=1
    except:
        i=0
        Orbimg = ImageTk.PhotoImage(PIL.Image.open(path+r"\sirilike\pic"+"{:0>2}".format(str(i))+r".png"))
        AwakeSoundOrbLabel.config(image=Orbimg)
        AwakeSoundOrbLabel.image = Orbimg
        AssistantTopWindow.after(30,TopLevelImage)
        i+=1
def UpDateTimeLabel():
    y = time.strftime("%Y")
    m = time.strftime("%m")
    d = time.strftime("%d")
    H = time.strftime("%I")
    M = time.strftime("%M")
    D = time.strftime("%p")
    if D=="AM":
        TimeLabel.config(text="上午 "+H+":"+M)
    else:
        TimeLabel.config(text="下午 "+H+":"+M)
    DateLabel.config(text=y+"/"+m+"/"+d)
    AssistantTopWindow.after(1000,UpDateTimeLabel)
AssistantTopWindow.after(0,UpDateTimeLabel)
AssistantTopWindow.after(0,UpDateRAM)
AssistantTopWindow.after(30,TopLevelImage)
AssistantTopWindow.mainloop()