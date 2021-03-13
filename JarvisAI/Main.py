from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
import speech_recognition as sr
from comtypes import CLSCTX_ALL
from tkinter.ttk import *
from pyautogui import *
from PIL import ImageTk
from gtts import gTTS
from tkinter import *
import tkinter as tk
import webbrowser
import playsound
import pyautogui
import threading
import wikipedia
import requests
import smtplib
import random
import codecs
import time
import PIL
import os

path = os.getcwd()
print("\nRunning In Path: {}\n".format(path))

class schedule():
    def __init__(self, month, day, hour, minute, thing):
        self.month = "{:0>2}".format(str(month))
        self.day = "{:0>2}".format(str(day))
        self.hour = "{:0>2}".format(str(hour))
        self.minute = "{:0>2}".format(str(minute))
        self.thing = str(thing)
        with codecs.open(path+r"\features\Schedule.txt", "a", "utf-8") as f:
            f.writelines([self.month+" "+self.day," ", self.hour+" "+self.minute," "+self.thing+"\n"])
        print("添加行程 : "+self.month+" "+self.day+" "+self.hour+" "+self.minute+" "+self.thing)
        talkTW("已未您添加行程,"+self.month+"月"+self.day+"日,"+self.hour+"點"+self.minute+"分,"+self.thing)

def talkTW(text):
    readtext = gTTS(text,lang="zh-TW")
    TWsound = "TWsound.mp3"
    readtext.save(path+r"\features\TWsound.mp3")
    playsound.playsound(path+r"\features\TWsound.mp3")
    os.remove(path+r"\features\TWsound.mp3")

def GetWeather():
    def WeatherMainWindow():
        global WeatherWindow
        WeatherWindow = tk.Tk()
        WeatherWindow.title("Weather")
        WeatherWindow.wm_attributes("-topmost", 1)
        WeatherWindow.geometry("350x450+849+315")
        def buildUP():
            """Get API Response"""
            fullOneCalldata = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&lang={lang}&units=metric&appid={API}".format(lat="22.6163",lon="120.3133",lang="zh_TW",API="密鑰無法公開"))
            OneCalldata = fullOneCalldata.json()
            fullWeatherdata = requests.get("https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&lang={lang}&units=metric&appid={API}".format(lat="22.6163",lon="120.3133",lang="zh_TW",API="密鑰無法公開"))
            Weatherdata = fullWeatherdata.json()

            """Define Varlues"""
            CityLocation = str(Weatherdata["name"])
            FeelTemp = str(int(Weatherdata["main"]["feels_like"]))+"° "
            WindSpeed = str(round(float(OneCalldata["daily"][0]["wind_speed"])))+"公里/小時"
            Visibility = str(round(int(Weatherdata["visibility"])/1000))+"公里"
            Pressure = str(int(Weatherdata["main"]["pressure"]))+"毫巴"
            AirWetRate = str(int(Weatherdata["main"]["humidity"]))+"%"
            TempToRain = str(round(float(OneCalldata["daily"][0]["dew_point"])))+"°"
            RainRate = str(int(float(OneCalldata["daily"][0]["pop"])*10))+"%"
            Description = str(Weatherdata["weather"][0]["description"])
            SpeekOut = "今日天氣 , "+Description+" , 氣溫 , "+FeelTemp+", 空氣濕度 , "+AirWetRate+" , 降雨機率 , "+RainRate

            with codecs.open(path+r"\features\weather.txt", "w", "utf-8") as WeatherFile:
                WeatherFile.write(SpeekOut)
            
            def talkWeatherOut(WeatherText=SpeekOut):
                talkTW(WeatherText)
            SpeekWeather = threading.Thread(target=talkWeatherOut)
            SpeekWeather.start()

            """Get Time"""
            H = time.strftime("%H")
            M = time.strftime("%M")
            AP = time.strftime("%p")
            if AP=="AM":
                TimeText="上午 "+H+":"+M
            else:
                TimeText="下午 "+H+":"+M
            
            """Define Widgets"""
            LocationLabel = tk.Label(WeatherWindow, text=CityLocation, font=("Arial",25))

            iconID = "\WeatherIcons\\"+Weatherdata["weather"][0]["icon"]
            print(path+iconID+r".png")
            
            WeatherFrame = tk.LabelFrame(WeatherWindow)
            WeatherIconImg = ImageTk.PhotoImage(PIL.Image.open(path+iconID+r".png"), master=WeatherWindow)
            WeatherIcon = tk.Label(WeatherFrame, image=WeatherIconImg)
            WeatherIcon.image = WeatherIconImg
            TempLabel = tk.Label(WeatherFrame, text=FeelTemp, font=("Arial",40))

            WeatherDescription = tk.Label(WeatherWindow, text=Description, font=("Arial",25))

            WhenUpDate = tk.Label(WeatherWindow, text="更新時間: "+TimeText, font=("Arial",15))

            RainRateLabel = tk.Label(WeatherWindow, text="降雨機率 "+RainRate, font=("Arial",15))

            WindInfoLabel = tk.Label(WeatherWindow, text="風速 "+WindSpeed, font=("Arial",15))

            VisibilityLabel = tk.Label(WeatherWindow, text="能見度 "+Visibility, font=("Arial",15))

            PressureLabel = tk.Label(WeatherWindow, text="氣壓 "+Pressure, font=("Arial",15))

            AirWetRateLabel = tk.Label(WeatherWindow, text="濕度 "+AirWetRate, font=("Arial",15))

            TempToRainLabel = tk.Label(WeatherWindow, text="露點 "+TempToRain, font=("Arial",15))

            """Grid Pack Place"""
            LocationLabel.pack(pady=5, side=tk.TOP)
            
            WeatherFrame.pack(pady=5, side=tk.TOP)
            WeatherIcon.pack(side=tk.LEFT)
            TempLabel.pack(side=tk.LEFT)

            WeatherDescription.pack(side=tk.TOP)

            WhenUpDate.pack(pady=5, side=tk.TOP)
            
            RainRateLabel.pack(side=tk.TOP)

            WindInfoLabel.pack(side=tk.TOP)

            VisibilityLabel.pack(side=tk.TOP)

            PressureLabel.pack(side=tk.TOP)

            AirWetRateLabel.pack(side=tk.TOP)

            TempToRainLabel.pack(side=tk.TOP)

        WeatherWindow.after(0,buildUP)
        WeatherWindow.mainloop()
    weatherThread = threading.Thread(target=WeatherMainWindow)
    weatherThread.start()

def AwakeOrb():
    os.system(path+r"\AwakeORB.py")

def sendGmail(SendTo, TheMessage):
    if TheMessage:
        myGmail = "信箱無法公開"
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(myGmail, "信箱無法公開")
        print("Gmail login Successful")
        server.sendmail(myGmail, SendTo, TheMessage)
        print("Gmail Sent:\n"+TheMessage)
        server.quit()

def countdown(t):
    talkTW("開始到計時,{}秒".format(t))
    print("Starting a {} seconds timer".format(t))
    time.sleep(t)
    playsound.playsound(path+r"\features\AlarmClock.mp3")
    print("Time's Up")

def YouTube():
    webbrowser.open("https://www.youtube.com/")

def Gimy():
    webbrowser.open("https://gimy.tv/")

def Googlemap():
    webbrowser.open("https://www.google.com/maps")

def Twitch():
    webbrowser.open("https://www.twitch.tv/godjj")

def hangouts():
    webbrowser.open("https://hangouts.google.com/")

def MessengerGameTime():
    callYiAnnGaming = webdriver.Chrome(path+r"\chromedriver.exe")
    callYiAnnGaming.get("https://www.messenger.com/t/100012184447487")
    time.sleep(2)
    eml = callYiAnnGaming.find_element_by_id("email")
    eml.send_keys("信箱無法公開")
    pwd = callYiAnnGaming.find_element_by_id("pass")
    pwd.send_keys("密碼無法公開")
    pwd.send_keys(Keys.RETURN)
    time.sleep(3)
    send = callYiAnnGaming.find_element_by_class_name("_1mf._1mj")
    send.send_keys(random.choice(["老闆叫你起床了", "老闆叫你別睡了", "老闆找你打遊戲呢", "老闆叫你起來打遊戲了", "起來囉, 打遊戲囉, 李福昌已經在等你囉"]))
    send.send_keys(Keys.RETURN)
    time.sleep(1)
    callYiAnnGaming.quit()

def AddScheduleSpeak():
    r = sr.Recognizer()
    while(True):
        with sr.Microphone() as speech:
            try:
                print("Listening to Schedule. . .")
                talkTW("請問要添加的行程的日期和時間是在什麼時候")
                audio = r.listen(source=speech, timeout=None, phrase_time_limit=5)
                try:
                    text = r.recognize_google(audio, language="zh-TW")
                    if "取消" in text:
                        talkTW("好的")
                        break
                    if "月" and "號" in text:
                        print(text)
                        text = text.split("月")
                        month = text[0]
                        text = text[1].split("號")
                        date = text[0]
                        if "點" and "分" in text:
                            text = text[1].split("點")
                            clock = text[0]
                            text = text[1].split("分")
                            minute = text[0]
                            thing = text[1]
                        elif "點" in text:
                            text = text[1].split("點")
                            clock = text[0]
                            minute = 0
                            thing = text[1]
                        elif "整天" in text[1]:
                            clock = 12
                            minute = 0
                            thing = text[1].replace("整天", "")
                        else:
                            clock = 12
                            minute = 0
                            thing = text[1]
                        
                        schedule(month,date,clock,minute,thing)
                        break
                except:
                    pass
            except:
                pass

def CheckWakeUp():
    playsound.playsound(path+r"\features\AlarmClock.mp3")
    r = sr.Recognizer()
    while(True):
        with sr.Microphone() as speech:
            try:
                print("Waking up. . .")
                audio = r.listen(source=speech, timeout=None, phrase_time_limit=5)
                try:
                    text = r.recognize_google(audio, language="zh-TW")
                    if "好" in text or "醒" in text or "鬧鐘" in text:
                        break
                    else:
                        playsound.playsound(path+r"\features\AlarmClock.mp3")
                except:
                    continue
            except:
                continue

def GoodMorning():
    Ih = time.strftime("%I")
    m=time.strftime("%M")
    mm=time.strftime("%m")
    dd=time.strftime("%d")
    Morning = "早上好！ , "
    D = time.strftime("%A")
    Morning+="現在時間, 早上, "+Ih+"點,"+m+"分,"
    if D.lower()=="monday":
        Morning += "今天是星期一, " 
    elif D.lower()=="tuesday":
        Morning += "今天是星期二, 上學請記得穿制服, "
    elif D.lower()=="wednesday":
        Morning += "今天是星期三, "
    elif D.lower()=="thursday":
        Morning += "今天是星期四, 上學請記得穿班服, "
    elif D.lower()=="friday":
        Morning += "今天是星期五, 上學請記得穿社服, "
    with codecs.open(path+r"\features\weather.txt","r","utf-8") as weather:
        read_weather = weather.read().split(" , ")
        Morning+="今日氣溫,"+read_weather[3]+","+read_weather[1]+","
    with codecs.open(path+r"\features\Schedule.txt", "r", "utf-8") as g:
        Schedule_text=g.read().split("\n")
        for i in range(len(Schedule_text)):
            Schedule_text[i]=Schedule_text[i].split(" ")
    todaySchedule = []
    for i in range(len(Schedule_text)):
        if mm==Schedule_text[i][0] and dd==Schedule_text[i][1]:
            todaySchedule.append(Schedule_text[i][2]+"點"+Schedule_text[i][3]+"分, "+Schedule_text[i][4]+",")
            print("今天"+Schedule_text[i][2]+"點"+Schedule_text[i][3]+"分, "+Schedule_text[i][4])
    if len(todaySchedule) != 0:
        Morning += "今天有"+str(len(todaySchedule))+"個行程,"
        for things in todaySchedule:
            Morning += things
    if int(read_weather[-1].replace("%", ""))>75:
        Morning += "今日極有可能降雨, 外出請記得帶傘"
    elif int(read_weather[3].replace("°", ""))>25:
        Morning += "今天天氣較為溫暖, 可以考慮不帶外套"
    elif int(read_weather[3].replace("°", ""))<20:
        Morning += "今天天氣較為涼爽, 外出建議鞋帶外套"
    else:
        Morning += "今天天氣較為舒適, 適合外出走走"
    talkTW(Morning)

def SetMute(MutingConfiguration):    
    volume = cast(AudioUtilities.GetSpeakers().Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None), POINTER(IAudioEndpointVolume))
    volume.SetMute(MutingConfiguration, None)

def MainFunc():
    threading.Thread(target=AwakeOrb).start()
    NoCallingTimeOut = 0
    r = sr.Recognizer()
    while(NoCallingTimeOut<=50):
        print("listening... "+"{:0>2}".format(str(NoCallingTimeOut)))
        with sr.Microphone() as speech:
            try:
                audio = r.listen(source=speech, timeout=None, phrase_time_limit=5)
                try:
                    text = r.recognize_google(audio, language="zh-TW")
                    print(text)
                    text = text.replace("幫我", "").lower().replace("謝謝", "")
                    i = 0
                    if ("你" in text and "休息" in text) or (("等一下" in text or "有事" in text ) and ("找你" in text or "叫你" in text)):
                        talkTW(random.choice(["好的","好的,我們呆悔見"]))
                        break
                    if "在嗎" in text:
                        talkTW("我在")
                        NoCallingTimeOut = 0
                    if "翻譯" in text:
                        talkTW("好的")
                        now_X , now_Y = pyautogui.position()
                        pyautogui.click(x=2030,y=105,button="right")
                        pyautogui.press("T")
                        pyautogui.moveTo(now_X,now_Y)
                        NoCallingTimeOut = 0
                        continue
                    if "寄" in text or "mail" in text or "郵件" in text:
                        def hearMailMessage():
                            MailInnerMessage = ""
                            while(True):
                                with sr.Microphone() as speech:
                                    try:
                                        audio = r.listen(source=speech)
                                        try:
                                            text = r.recognize_google(audio, language="zh-TW").lower()
                                            print(" --"+text)
                                            if (("送" or "寄") and "出" in text) or "好了" in text or "ok" in text or "結束" in text or "停止" in text:
                                                print("Listening Mail Message Stopped. . .")
                                                break
                                            elif "取消" in text:
                                                MailInnerMessage = ""
                                                break
                                            MailInnerMessage += (text+"\n")
                                        except:
                                            continue
                                    except:
                                        continue
                            return MailInnerMessage
                        if "林" in text and "玲" in text:
                            sendGmail("朋友信箱無法公開", hearMailMessage())
                    if "影片" in text or "youtube" in text or "休息時間" in text:
                        talkTW("好的, 已未您開啟YouTube")
                        YouTube()
                        NoCallingTimeOut = 0
                        continue
                    elif "電影" in text:
                        talkTW("好的")
                        Gimy()
                        NoCallingTimeOut = 0
                        continue
                    elif "twitch" in text:
                        talkTW("好的")
                        Twitch()
                        NoCallingTimeOut = 0
                        continue
                    elif "地圖" in text:
                        talkTW("好的")
                        Googlemap()
                        NoCallingTimeOut = 0
                        continue
                    elif "計算機" in text:
                        os.system("calc")
                        NoCallingTimeOut = 0
                        continue
                    if "叫" in text and "王" in text and "起" in text:
                        talkTW("好的")
                        threading.Thread(target=MessengerGameTime).start()
                    if ("聲音" in text and "開" in text) or ("取消" in text and "靜音" in text):
                        SetMute(0)
                        print("UnMuted")
                        NoCallingTimeOut = 0
                        continue
                    elif ("聲音" in text and "關" in text) or "靜音" in text:
                        SetMute(1)
                        print("Muted")
                        NoCallingTimeOut = 0
                        continue
                    if "搜尋" in text or "是什麼" in text:
                        wikipedia.set_lang("zh-TW")
                        talkTW("稍等, 正在幫您查詢")
                        result = wikipedia.summary(text.replace("搜尋", "").replace("一下", "").replace("是什麼", ""), sentences=2) 
                        print(result)
                        talkTW(result)
                        NoCallingTimeOut = 0
                        continue
                    if ("計時" in text or "倒數" in text) and "秒" in text:
                        text = text.replace("設", "").replace("定", "").replace("一", "").replace("個", "").replace("秒", "").replace("的", "").replace("計時", "").replace("器", "").replace("倒", "").replace("數", "")
                        countdown(int(text.replace("兩", "2")))
                        NoCallingTimeOut = 0
                        continue
                    if "數字" in text:
                        text = text.split("從")[1].split("到")
                        firstNum=text[0].replace("零","0").replace("一","1").replace("二","2")
                        text = text[1].split("選")
                        secondNum=text[0].replace("一","1").replace("二","2")
                        HowMany = text[1].replace("出","").replace("個","").replace("隨機","").replace("數字","").replace("兩","2").replace("一","1")
                        OPList = []
                        for i in range(int(HowMany)):
                            OPList.append(random.randrange(int(firstNum),int(secondNum)))
                        talkTW("我選")
                        print("我選 : ", end="")
                        for index in range(len(OPList)):
                            talkTW(str(OPList[index]))
                            print(str(OPList[index])+",", end="")
                        print()
                        NoCallingTimeOut = 0
                        continue
                    if "等於" in text:
                        text = text.replace("多少", "")
                        text = text.split("等於")[0]
                        if "+" in text:
                            countList = text.split("+")
                            ans = float(countList[0])+float(countList[1])
                        elif "加" in text:
                            countList = text.split("加")
                            ans = float(countList[0])+float(countList[1])
                        elif "-" in text:
                            countList = text.split("-")
                            ans = float(countList[0])-float(countList[1])
                        elif "減" in text:
                            countList = text.split("減")
                            ans = float(countList[0])-float(countList[1])
                        elif "×" in text:
                            countList = text.split("×")
                            ans = float(countList[0])*float(countList[1])
                        elif "乘" in text:
                            if "以" in text:
                                countList = text.split("乘以")
                                ans = float(countList[0])*float(countList[1])
                            else:
                                countList = text.split("乘")
                                ans = float(countList[0])*float(countList[1])
                        elif "÷" in text:
                            countList = text.split("÷")
                            ans = float(countList[0])/float(countList[1])
                        elif "除" in text:
                            if "以" in text:
                                countList = text.split("除以")
                                ans = float(countList[0])/float(countList[1])
                            else:
                                countList = text.split("除")
                                ans = float(countList[0])/float(countList[1])
                        if ans%1==0:      
                            print("等於, "+str(int(ans)))                 
                            talkTW("等於, "+str(int(ans)))
                        else:
                            print("等於, "+str(ans))
                            talkTW("等於, "+str(ans))
                        NoCallingTimeOut = 0
                    if "開" in text and "燈" in text:
                        print("open")
                        talkTW("好的")
                        if int(os.system("curl -X POST http://localhost:2004/LightOn"))==0:
                            time.sleep(1)
                            talkTW("已未您打開電燈")
                        else:
                            talkTW("我無法連接到電燈開關")
                        NoCallingTimeOut = 0
                        continue
                    if "關" in text and "燈" in text:
                        print("close")
                        if int(os.system("curl -X POST http://localhost:2004/LightOff"))==0:
                            talkTW("已未您關閉電燈")
                        else:
                            talkTW("我無法連接到電燈開關")
                        NoCallingTimeOut = 0
                        continue
                    if ("筆記" in text or "紀錄" in text or "記錄" in text) and ("內容" in text or "說" in text or "念" in text or "讀" in text):
                        NoCallingTimeOut = 0
                        InNote = ""
                        with codecs.open(path+r"\features\note.txt", "r", "utf-8") as note:
                            lines = note.readlines()
                        for line in lines:
                            InNote += (line.replace("\r", "").replace("\n", "")+",")
                        talkTW(InNote)
                        continue
                    if "筆記" in text or "紀錄" in text or "記錄" in text:
                        NoCallingTimeOut = 0
                        print("Taking note. . .")
                        talkTW("開始記錄")
                        with codecs.open(path+r"\features\note.txt", "w", "utf-8") as note:
                            while(True):
                                with sr.Microphone() as speech:
                                    try:
                                        audio = r.listen(source=speech, timeout=None, phrase_time_limit=5)
                                        try:
                                            text = r.recognize_google(audio, language="zh-TW")
                                            print(" --"+text)
                                            if (("停" or "結束") and "記錄" in text) or "好了" in text:
                                                print("Stop taking note. . .")
                                                talkTW("記錄完畢")
                                                break
                                            note.write(text+"\n")
                                        except:
                                            continue
                                    except:
                                        continue
                    if "新項目" in text:
                        NoCallingTimeOut = 0
                        talkTW("要將檔案命名為")
                        while(True):
                            with sr.Microphone() as speech:
                                try:
                                    audio = r.listen(source=speech, timeout=None, phrase_time_limit=5)
                                    try:
                                        text = r.recognize_google(audio, language="zh-TW")
                                        print(text)
                                        if "取消" in text or "算了" in text:
                                            talkTW("好的, 取消創建檔案")
                                            ProjectName = "取消"
                                            break
                                        if "就" in text:
                                            text = text.split("就")[1]
                                            ProjectName = text.replace("叫", "").replace("做", "").replace("吧", "")
                                            break
                                        if "名" in text:
                                            ProjectName = text.replace("命", "").replace("名", "").replace("為", "").replace("就", "").replace("吧").replace("叫").replace("做", "")
                                            break
                                    except:
                                        continue
                                except:
                                    continue
                        if "取消" not in ProjectName:
                            print("檔案名稱 : "+ProjectName)
                            talkTW("要幫你把檔案存在主資料庫嗎")
                            for wait in range(3):
                                print("listening doc "+str(wait+1)+"...")
                                with sr.Microphone() as speech:
                                    try:
                                        audio = r.listen(source=speech, timeout=None, phrase_time_limit=5)
                                        try:
                                            text = r.recognize_google(audio, language="zh-TW")
                                            print(text)
                                            with open(path+r"\features\NewProject.bat", "w") as NP:
                                                NP.write("cd / \n")
                                                if "桌面" in text:
                                                    talkTW("好的")
                                                    NP.write("cd C:/Users/a0988/OneDrive/Desktop \nmkdir "+ProjectName)
                                                    NP.write("\ncd "+ProjectName+"\ncd >Main.py\ncd >Test.py")
                                                elif "私人" in text:
                                                    talkTW("好的")
                                                    NP.write("cd G:/ \nmkdir "+ProjectName)
                                                    NP.write("\ncd "+ProjectName+"\ncd >Main.py\ncd >Test.py")
                                                elif "中央" in text:
                                                    talkTW("好的")
                                                    NP.write("C:/Users/a0988/Documents/CodingProjects \nmkdir "+ProjectName)
                                                    NP.write("\ncd "+ProjectName+"\ncd >Main.py\ncd >Test.py")
                                                elif "算" in text or "沒" in text or "不用" in text:
                                                    talkTW("好的, 取消創建檔案")
                                                    break
                                                else:
                                                    continue
                                            os.system(path+r"\features\NewProject.bat")
                                            talkTW("已創建專案, "+ProjectName)
                                            break
                                        except:
                                            continue
                                    except:
                                        continue
                    if "幾點" in text or "時間" in text:
                        h=time.strftime("%H")
                        if 5<=int(h) and int(h)<11:
                            TalkTime="現在時間, 上午, "+time.strftime("%I")+"點,"+time.strftime("%M")+"分,"
                        elif 11<=int(h) and int(h)<14:
                            TalkTime="現在時間, 中午, "+time.strftime("%I")+"點,"+time.strftime("%M")+"分,"
                        elif 14<=int(h) and int(h)<17:
                            TalkTime="現在時間, 下午, "+time.strftime("%I")+"點,"+time.strftime("%M")+"分,"
                        elif 17<=int(h) or int(h)<1:
                            TalkTime="現在時間, 晚上, "+time.strftime("%I")+"點,"+time.strftime("%M")+"分,"
                        elif 1<=int(h) or int(h)<5:
                            TalkTime="現在時間, 凌晨, "+time.strftime("%I")+"點,"+time.strftime("%M")+"分,"
                        talkTW(TalkTime)
                        NoCallingTimeOut = 0
                    if "天氣" in text:
                        GetWeather()
                        time.sleep(5)
                        NoCallingTimeOut = 0
                        continue
                    if "添加形成" in text or "添加行程" in text:
                        AddScheduleSpeak()
                        time.sleep(5)
                        NoCallingTimeOut = 0
                        continue
                    if "行程" in text or "形成" in text:
                        mm=time.strftime("%m")
                        dd=time.strftime("%d")
                        with codecs.open(path+r"\features\Schedule.txt", "r", "utf-8") as g:
                            Schedule_text=g.read().split("\n")
                            for i in range(len(Schedule_text)):
                                Schedule_text[i]=Schedule_text[i].split(" ")
                        t=True
                        todaySchedule = []
                        for i in range(len(Schedule_text)):
                            if mm==Schedule_text[i][0] and dd==Schedule_text[i][1]:
                                todaySchedule.append(Schedule_text[i][2]+"點"+Schedule_text[i][3]+"分, "+Schedule_text[i][4]+",")
                                print("今天"+Schedule_text[i][2]+"點"+Schedule_text[i][3]+"分, "+Schedule_text[i][4])
                                t=False
                        readSchedule = "今天有"+str(len(todaySchedule))+"個行程,"
                        for things in todaySchedule:
                            readSchedule += things
                        if t:
                            talkTW("我這邊沒有任何行程記錄")
                        else:
                            talkTW(readSchedule)
                        NoCallingTimeOut = 0
                    else:
                        NoCallingTimeOut+=1
                        continue
                except:
                    NoCallingTimeOut+=1
                    continue
            except:
                NoCallingTimeOut+=1
                continue
    os.system("taskkill /f /fi \"WindowTitle eq Assistant\"")

def Assistant():
    Alarm = True
    r = sr.Recognizer()
    print("Voice Assistant --Started")
    while(True):
        h = time.strftime("%H")
        m = time.strftime("%M")
        D = time.strftime("%A")
        if int(h)!=5:
            Alarm = True
        if Alarm == True:
            if D[0] != "S":
                if int(h)==5:
                    CheckWakeUp()
                    time.sleep(2)
                    GoodMorning()
                    Alarm = False
        print("waiting...")
        with sr.Microphone() as speech:
            try:
                audio = r.listen(source=speech, timeout=None, phrase_time_limit=3)
                try:
                    call = r.recognize_google(audio, language="zh-TW")
                    print(call)
                    if "早安" in call:
                        GoodMorning()
                    if "鬧鐘" in call:
                        if Alarm == True:
                            talkTW("鬧鐘已是開啟狀態")
                        else:
                            talkTW("鬧鐘並未啟動, 是否要開啟鬧鐘")
                            r = sr.Recognizer()
                            with sr.Microphone() as speech:
                                try:
                                    audio = r.listen(source=speech, timeout=None, phrase_time_limit=3)
                                    try:
                                        check = r.recognize_google(audio, language="zh-TW")
                                        if "開啟" or "好" in check:
                                            Alarm = True
                                            talkTW("已未您設置鬧鈴")
                                        elif "不用" in check:
                                            talkTW("好的, 鬧鐘保持關閉, 如有需要開啟請在通知我")
                                        else:
                                            talkTW("鬧鐘保持關閉, 如有需要開啟請在通知我")
                                    except:
                                        pass
                                except:
                                    pass
                    if "關" in call and "燈" in call:
                        if int(os.system("curl -X POST http://localhost:2004/LightOff"))==0:
                            talkTW("已未您關閉電燈")
                        else:
                            talkTW("我無法連接到電燈開關")
                    if "開" in call and "燈" in call:
                        talkTW("好的")
                        if int(os.system("curl -X POST http://localhost:2004/LightOn"))==0:
                            time.sleep(1)
                            talkTW("已未您打開電燈")
                        else:
                            talkTW("我無法連接到電燈開關")
                    elif "在嗎" in call:
                        talkTW(random.choice(["一直都在", "隨時待命", "一直都在"]))
                        MainFunc()
                    if "謝謝" in call:
                        talkTW("不客氣")
                except:
                    continue
            except:
                continue

MainAssist = threading.Thread(target=Assistant)

MainAssist.start()