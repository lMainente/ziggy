import pyttsx3
import datetime
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import webbrowser
import pyautogui
import wikipedia
import os
import psutil
import wolframalpha
from time import sleep
from fbchat import Client
from fbchat.models import *

def speak(audio):
    print(audio)
    engine = pyttsx3.init()
    engine.setProperty('rate', 130)  
    voices = engine.getProperty('voices')       
    engine.setProperty('voice', voices[1].id)  
    engine.say(audio)
    engine.runAndWait()

def click():
    pyautogui.click()

def username():
    username = psutil.users()
    for user_name in username:
        first_name = user_name[0]
        speak(f"this computer is signed to {first_name} as a username.")
    
def screenshot():
    pyautogui.screenshot(f"C://Users//{first_name}//Desktop//screenshot.png")

def battery():
    battery = psutil.sensors_battery()
    battery_percentage = str(battery.percent)
    plugged = battery.power_plugged
    speak(f"it is {battery_percentage} percent.")
    if plugged:
        speak("and It is charging....")
    if not plugged:
        if battery_percentage <= "95%":
            speak("plug charger.")

def shutDown():
    speak(f'Ok    ')
    speak('Initializing shutdown protocol ')
    click()
    pyautogui.keyDown('alt')
    pyautogui.press('f4')
    pyautogui.keyUp('alt')
    pyautogui.press('enter')
    sleep(3)
    pyautogui.press('enter')

def restart():
    speak("Ok     ")
    speak("Restarting your computer")
    click()
    pyautogui.keyDown('alt')
    pyautogui.press('f4')
    pyautogui.keyUp('enter')
    sleep(3)
    pyautogui.press('r')
    pyautogui.press('enter')

def Sleep():
    speak('Ok     ')
    speak("Initializing sleep mode")
    pyautogui.keyDown('alt')
    pyautogui.press('f4')
    pyautogui.keyUp('alt')
    sleep(2)
    pyautogui.press('s')
    pyautogui.press('s')
    pyautogui.press('enter')

def weather():
    speak("Checking the details for weather...")
    URL = "https://weather.com/weather/today/l/-24.0074,-46.4227?par=google&temp=c"
    header = {"User-Agent":'User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    page = requests.get(URL, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    temperature = soup.find(class_="CurrentConditions--tempValue--MHmYY").get_text()
    description = soup.find(class_="CurrentConditions--phraseValue--mZC_p").get_text()
    temp = "A temperatura é " + temperature + " celcius." + ' e esta ' + description + ' la fora.'
    speak(temp)
    if temperature < '20°':
        speak("Friozin bom.")
    elif temperature <= '14°':
        speak("Esta bem frio la fora, é bom usar uma roupa mais pesada.")
    elif temperature >= '25°':
        speak("Calorzinho.")
    elif temperature >= '30°':
        speak("O arrebatamento ja passou e você ta no inferno")

def message():
    speak("Checking for messages....")
    userID = "your email"
    psd = 'your password'
    useragent = "you user agent"

    cli = Client(userID, psd, user_agent=useragent, max_tries=1)
    if cli.isLoggedIn():
        threads = cli.fetchUnread()
        if len(threads) == 1:
            speak(f"You have {len(threads)} message.")
            info = cli.fetchThreadInfo(threads[0])[threads[0]]
            speak("You have message from {}".format(info.name))
            msg = cli.fetchThreadMessages(threads[0], 1)
            for message in msg:
                speak("the message is {}".format(message.text))
        elif len(threads) >= 2:
            speak(f"You have {len(threads)} messages.")
            for thread in threads:
                initial_number = 0
                info = cli.fetchUserInfo(thread[initial_number])[thread[initial_number]]
                initial_number += 1
                speak("you have message from {}".format(info.name))
                msg = cli.fetchThreadMessages(thread[initial_number], 1)
                msg.reverse()
                for message in msg:
                    speak(f"The message is {message.text}.")
        else:
            speak("You have no messages.")
    else:
        print("Not logged in")

def time():
    time = datetime.datetime.now().strftime('%I:%M:%S')
    speak(f"the current time is {time}.")

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak(f"the current year is {year}, current month is {month} and the current date is {date}")

def google_search(audio_data):
    try:
        search_query = "+".join(audio_data.split())
        url = f"https://www.google.com/search?q={search_query}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        search_results = soup.select('div.g')  
        
        if search_results:
            for result in search_results:
                result_title = result.find('h3')
                if result_title:
                    result_title_text = result_title.get_text()
                    result_url = result.find('a')['href']
                    result_snippet = result.select_one('div.IsZvec').get_text() if result.select_one('div.IsZvec') else ""
                    
                    speak(f"The top search result for '{audio_data}' is: {result_title_text}")
                    if result_snippet:
                        speak(f"Here's some information: {result_snippet}")
                    speak("Opening the webpage.")
                    webbrowser.open(result_url)
                    break  
        else:
            speak(f"No search results found for '{audio_data}'")

    except Exception as e:
        speak("Sorry, I encountered an error while processing your request.")


def youtube_search(audio_data):
    url = "https://www.youtube.com/results?search_query=" + audio_data
    webbrowser.open(url)
    speak(f"getting the result for {audio_data} from youtube.com")
    
def wikipedia_search(audio_data):
    if audio_data:
        try:
            results = wikipedia.summary(audio_data, sentences=2)
            speak('According to Wikipedia, ')
            speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"Multiple matches found for {audio_data}. Please be more specific.")
        except wikipedia.exceptions.PageError as e:
            speak(f"Sorry, no information found on {audio_data}.")
    else:
        speak("You didn't specify a topic. Please try again.")
        
def calculate(audio_data):
    app_id = '8REQUG-YQ7JGY96T8'
    client = wolframalpha.Client(app_id)
    res = client.query(audio_data)
    answer = next(res.results).text
    speak(answer)

def greeting():
    speak('Welcome back .')
    time()
    date()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 400
        r.dynamic_energy_threshold = True
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio)
        print(query)
        if 'Ziggy' in query:
            speak("Yes, how can i help you right now")
        elif 'tell me the date' in query or 'tell me date' in query:
            date()
        elif 'hows going' in query or 'how are you' in query:
            greeting() 
        elif 'tell me the time' in query or 'what time is it' in query or 'tell time' in query:
            time()
        elif 'thank you' in query:
            speak('No problem ')
        elif 'open Google' in query:
            webbrowser.open("https://www.google.com")
            speak("Opening google...")
        elif 'Google search' in query:
            speak('What do you want to search')
            audio_data = command()
            google_search(audio_data)
        elif 'open YouTube' in query:
            webbrowser.open("https://www.youtube.com")
            speak("Opening Youtube....")
        elif 'YouTube search' in query:
            speak('What do you want to search?')
            audio_data = command()
            youtube_search(audio_data)
        elif 'open Facebook' in query:
            webbrowser.open_new_tab("https://www.facebook.com")
            speak("Opening Facebook")
        elif 'open Gmail' in query:
            webbrowser.open("https://mail.google.com/mail/u/0/#inbox")
            speak("Opening Gmail..")
        elif 'open maps' in query or 'show my location' in query:
            webbrowser.open("https://www.google.com/maps/@26.6235458,87.3614451,16z")
            speak("Opening Maps...")
        elif 'calculate' in query:
            speak('Tell me ')
            audio_data = command()
            calculate(audio_data)
        elif 'tell me' in query:
            audio_data = query.replace('tell me', '')
            calculate(audio_data)
        elif "what's the weather" in query or 'tell me the temperature' in query or "what's the temperature" in query:
            weather()
        elif 'click the mouse' in query or 'click mouse' in query or 'click' in query:
            click()
        elif 'take a screenshot' in query or 'take screenshot' in query:
            screenshot()
        elif 'Wikipedia' in query:
            speak('What do you want to search')
            audio_data = command()
            wikipedia_search(audio_data)
        elif 'close current window' in query:
            pyautogui.keyDown('alt')
            pyautogui.press('f4')
            pyautogui.keyUp('alt')
            speak('Current window is closed.')
        elif 'battery percentage' in query or 'percentage in battery' in query or 'percent in my pc' in query:
            battery()
        elif 'shutdown' in query or 'shut down' in query or 'close my PC' in query:
            shutDown()
        elif 'sleep' in query or 'sleep mode' in query:
            Sleep()
        elif 'check message' in query or 'check messages' in query or 'check new messages' in query or 'check new message' in query or 'any new messages' in query or 'any new messages' in query or 'any new message' in query or 'any messages' in query or 'any message' in query:
            message()
        elif 'username' in query or 'user' in query or 'user name' in query:
            username()

    except:
        return None
    return query



if __name__ == '__main__':
    while True:
        command()