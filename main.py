import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API Keys
weather_api_key = os.getenv("WEATHER_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")
ipinfo_token = os.getenv("IPINFO_TOKEN")
huggingface_token = os.getenv("HUGGINGFACE_TOKEN")

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
    except:
        command = ""
    return command

def get_weather():
    city = "Faridabad"  # You can use IP-based detection later
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    res = requests.get(url).json()
    if res.get("main"):
        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"]
        talk(f"The temperature in {city} is {temp}°C with {desc}.")
    else:
        talk("Couldn't fetch weather.")

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}"
    res = requests.get(url).json()
    articles = res.get("articles", [])[:3]
    if articles:
        for i, article in enumerate(articles):
            talk(f"News {i+1}: {article['title']}")
    else:
        talk("Sorry, I couldn't get news right now.")

def ask_question(question):
    url = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
    headers = {"Authorization": f"Bearer {huggingface_token}"}
    payload = {"inputs": {
        "question": question,
        "context": "You are an AI assistant. Try to help with general questions."
    }}
    response = requests.post(url, headers=headers, json=payload)
    answer = response.json().get('answer', "Sorry, I don't know that.")
    talk(answer)

def run_alexa():
    command = take_command()
    print("User:", command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('Playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        talk(info)
    elif 'weather' in command:
        get_weather()
    elif 'news' in command:
        get_news()
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'question' in command:
        talk("Ask your question.")
        question = take_command()
        ask_question(question)
    elif 'date' in command:
        talk('Sorry, I have a headache.')
    else:
        talk("Sorry, I didn't catch that.")

# Run Loop
while True:
    run_alexa()
