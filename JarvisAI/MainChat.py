from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from google_trans_new import google_translator 
import speech_recognition as sr
from selenium import webdriver
from gtts import gTTS
import threading
import pyttsx3
import time
import os

path = os.getcwd()

translator = google_translator()

def StartCommunicatingAI():
    global MainBrowser

    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_experimental_option("detach", True)
    MainBrowser = webdriver.Chrome(path+r"\chromedriver.exe")
    MainBrowser.get("https://my.replika.ai/login")

    while(True):
        try:
            Gmail = MainBrowser.find_element_by_id("emailOrPhone")
            Gmail.send_keys("帳號無法公開")

            Gmail.send_keys(Keys.RETURN)
            break
        except:
            continue

    time.sleep(2)

    while(True):
        try:
            Password = MainBrowser.find_element_by_id("login-password")
            Password.send_keys("密碼無法公開")

            Password.send_keys(Keys.RETURN)
            break
        except:
            continue

    time.sleep(2)

    while(True):
        try:
            Accept = MainBrowser.find_element_by_class_name("GdprNotification__LinkButton-nj3w6j-1.hQVndK")
            Accept.click()
            break
        except:
            continue

    time.sleep(5)

    def talk(TTS):
        translated_output_text = translator.translate(TTS,lang_src="en", lang_tgt='zh-tw')
        engine = pyttsx3.init()
        Voice = engine.getProperty('voices')
        engine.setProperty('voice', Voice[0].id)
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate-40)
        engine.say(translated_output_text)
        engine.runAndWait()
        print("\n"+TTS+"\n -->> \n"+translated_output_text+"\n")

    def SendMessage(message):
        while(True):
            try:
                InputText = MainBrowser.find_element_by_id("send-message-textarea")
                try:
                    InputText.click()
                    InputText.send_keys(message)
                    InputText.send_keys(Keys.RETURN)
                    break
                except:
                    continue
            except:
                break

    def GetResponse():

        AllRes = ""

        history = []

        while(True):
            try:
                responseAll = MainBrowser.find_elements_by_class_name(
                    "MessageGroup__MessageGroupInner-h4dfhv-1.gZnBBv"
                    )

                try:
                    responses = responseAll[-1].find_elements_by_class_name(
                        "MessageHover__MessageHoverRoot-sc-6lkiln-0.kbKNLG.BubbleText__BubbleTextRoot-sc-1bng39n-0.iPctYY.MessageGroup__StyledMessage-h4dfhv-2.eCHIKq"
                        )
                    
                    for response in responses:
                        splited = response.get_attribute("innerHTML").split("aria-label=\"Sara says:\">")
                        res = splited[1].split("<span>")[1].split("</span>")[0]
                        if res not in history:
                            history.append(res)
                            talk(res)
                            listen=True
                        elif res in history:
                            if listen == True:
                                r = sr.Recognizer()
                                while(True):
                                    print("listening. . . ")
                                    with sr.Microphone() as speech:
                                        try:
                                            audio = r.listen(speech)
                                            try:
                                                text = r.recognize_google(audio, language="zh_tw")
                                                translated_input_text = translator.translate(text,lang_src="zh-tw", lang_tgt='en')
                                                print("\nYou: \n"+text+"\n --> \n"+translated_input_text+"\n")
                                                SendMessage(translated_input_text)
                                                listen = False
                                                break
                                            except:
                                                continue
                                        except:
                                            continue
                    time.sleep(2)
                except:
                    continue
            except:
                break
        print("history : ")
        for wrd in history:
            print(wrd)

    getRes = threading.Thread(target=GetResponse)
    getRes.start()




StartCommunicatingAI()