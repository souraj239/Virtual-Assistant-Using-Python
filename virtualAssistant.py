import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
from googlesearch import *

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour=int(datetime.datetime.now().hour)
    if(hour>=0 and hour <12):
        speak("Good Morning!")
    elif (hour>=12 and hour <18):
        speak("Good Afternoon!")
    else:
        speak('Good Evening!')
    speak("I am your Personal Virtual Assistant! Please tell me how may I help you ?")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1 
        audio=r.adjust_for_ambient_noise(source)
        audio=r.listen(source,10)
    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language='en-in')
        print(f"You said :  {query}\n")
        
    except sr.WaitTimeoutError:
        speak("Couldn't hear you. Did you say anything?")
        
        
    except Exception as e:
        #print(e)
        print("Didn't get that! Please Repeat")
        return "None"
    return query

def googleSearch(query):
    chrome_path = r'C:\\Program Files (x86)\\Google\\Chrome\\Application %s'
    for url in search(query, tld="co.in", num=1, stop = 1, pause = 2):
        webbrowser.open("https://google.com/search?q=%s" % query)
    
def readNotes():
    with open("notes.txt","r") as f:
       notes=f.read() 
    speak(notes)

def openApp(appName):
    appdir={}
    try:
        with open("applicationpaths.txt","r") as f:                 #add the apps and their path names in the file
            for line in f:
                (app,path)= line.split("  ")
                appdir[app]=path
        os.startfile((appdir.get(appName)).strip())
    except Exception as e:
        print(e)
        speak("Cannot find the Application. Searching on google")
        googleSearch(f"open {query}")

def addressbook(first_name):
    addDict={}
    with open("addressbook.txt",'r') as f:                          #populate the addressbook.txt with your contacts
        for line in f:
            (name,email)=line.split(" ")
            addDict[name]=email
    return addDict.get(first_name,"Error")

def takeNotes():
    while(True):
        speak("Please dictate your notes")
        notes=takeCommand()
        with open("notes.txt","a+") as f:
            f.writelines(notes)
        speak("Do you want to add anything else ? ")
        choice=takeCommand().lower()
        if "no" in choice or 'exit' in choice:
            break

def sendEmail(to, message):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    with open('credentials.txt','r') as f:                          #put your credentials in cred.txt fie as shown in example
        cred=f.read()
    eid,passw=cred.split(" ")[0], cred.split(" ")[1]
    server.login(eid,passw)
    server.sendmail(eid,to,message)


if __name__=="__main__":
    wishMe()
    while True:
        query=takeCommand().lower()
        if 'wikipedia'in query:
            speak("Searching wikipedia......")
            query=query.replace("wikipedia"," ")
            results=wikipedia.summary(query,sentences=3)
            speak("According to Wikipedia...")
            speak(results)
            
        if 'who is'in query:
            speak("Searching wikipedia......")
            query=query.replace("who is"," ")
            results=wikipedia.summary(query,sentences=3)
            speak("According to Wikipedia...")
            speak(results)
        
        elif "open youtube" in query:
            speak("opening youtube")
            chrome_path = r'C:\\Program Files (x86)\\Google\\Chrome\\Application %s'
            webbrowser.open("youtube.com")

        elif "open google" in query:
            speak("opening google")
            chrome_path = r'C:\\Program Files (x86)\\Google\\Chrome\\Application %s'
            webbrowser.open("google.com")        
        
        elif "play music" in query:
            music_dir="D:\\music"                            #Add your own music directory
            songs=os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,songs[0])) 

        elif "time" in query:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
             
        elif "send email" in query:
            try:
                speak("To whom? (First Name Only)")
                contact=takeCommand().lower()
                mailid=addressbook(contact)
                if mailid=="Error":
                    speak("You have entered a Invalid name. Please Try again")
                    raise "InvalidEmailIdException"
                speak("what should I say?")
                message=takeCommand()
                sendEmail( mailid ,message)
                speak("Your email has been sent")
           
            except Exception as e:
                print(e)
                speak("Error sending email")
        
        elif "email id" in query:
            speak("Who's email id do you want? (First Name Only)")
            contact=takeCommand().lower()
            mailid=addressbook(contact)
            if mailid=="Error":
                speak("You have entered a Invalid name. Please Try again")
            else:
                speak(f"{contact}'s email id is : {mailid}")
                
        elif "open" in query:
            query=(query.replace("open ","")).strip()
            openApp(query)
            
        elif "take notes" in query:
            takeNotes()
        
        elif "read" in query and "notes" in query:
            readNotes()
            
        elif "exit" in query:
            speak("Have a Good day!")
            break
            
        else:
            googleSearch(query)