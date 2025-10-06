from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
from dotenv import load_dotenv
import os
import threading
import queue

load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

weather_api_key = os.getenv("WEATHER_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")
ipinfo_token = os.getenv("IPINFO_TOKEN")
huggingface_token = os.getenv("HUGGINGFACE_TOKEN")

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)

response_queue = queue.Queue()

def talk(text):
    engine.say(text)
    engine.runAndWait()
    return text

def listen_microphone():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=0.5)
            audio = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(audio)
            return command.lower()
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except Exception as e:
        return None

def get_weather(city="Faridabad"):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        res = requests.get(url).json()
        if res.get("main"):
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            return f"The temperature in {city} is {temp}°C with {desc}."
        else:
            return "Couldn't fetch weather information."
    except:
        return "Weather service is currently unavailable."

def get_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}"
        res = requests.get(url).json()
        articles = res.get("articles", [])[:3]
        if articles:
            news_list = [f"{i+1}. {article['title']}" for i, article in enumerate(articles)]
            return " ".join(news_list)
        else:
            return "Sorry, I couldn't get news right now."
    except:
        return "News service is currently unavailable."

def ask_question(question):
    try:
        url = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
        headers = {"Authorization": f"Bearer {huggingface_token}"}
        payload = {"inputs": {
            "question": question,
            "context": "You are an AI assistant. Try to help with general questions."
        }}
        response = requests.post(url, headers=headers, json=payload)
        answer = response.json().get('answer', "Sorry, I don't know that.")
        return answer
    except:
        return "Q&A service is currently unavailable."

def process_command(command):
    command = command.lower()

    if 'alexa' in command:
        command = command.replace('alexa', '').strip()

    response = {
        "success": True,
        "command": command,
        "response": "",
        "action": None
    }

    if 'play' in command:
        song = command.replace('play', '').strip()
        response["response"] = f'Playing {song}'
        response["action"] = "play_music"
        response["data"] = {"song": song}
        try:
            pywhatkit.playonyt(song)
        except:
            response["response"] = "Unable to play music right now"

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        response["response"] = f'Current time is {time}'
        response["action"] = "tell_time"

    elif 'date' in command and 'update' not in command:
        date = datetime.datetime.now().strftime('%B %d, %Y')
        response["response"] = f"Today's date is {date}"
        response["action"] = "tell_date"

    elif 'who is' in command or 'what is' in command:
        person = command.replace('who is', '').replace('what is', '').strip()
        try:
            info = wikipedia.summary(person, sentences=2)
            response["response"] = info
            response["action"] = "wikipedia"
        except:
            response["response"] = "I couldn't find information about that."

    elif 'weather' in command:
        response["response"] = get_weather()
        response["action"] = "weather"

    elif 'news' in command:
        response["response"] = get_news()
        response["action"] = "news"

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        response["response"] = joke
        response["action"] = "joke"

    elif 'question' in command or '?' in command:
        question = command.replace('question', '').strip()
        response["response"] = ask_question(question)
        response["action"] = "question"

    else:
        response["response"] = "I can help you with: playing music, telling time, weather updates, news, Wikipedia searches, jokes, and answering questions."
        response["success"] = False

    return response

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/listen', methods=['POST'])
def listen():
    try:
        audio_data = listen_microphone()
        if audio_data:
            return jsonify({
                "success": True,
                "command": audio_data
            })
        else:
            return jsonify({
                "success": False,
                "message": "No speech detected. Please try again."
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route('/api/command', methods=['POST'])
def command():
    try:
        data = request.json
        user_command = data.get('command', '')
        speak = data.get('speak', False)

        if not user_command:
            return jsonify({
                "success": False,
                "message": "No command provided"
            }), 400

        result = process_command(user_command)

        if speak and result["response"]:
            threading.Thread(target=talk, args=(result["response"],)).start()

        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route('/api/speak', methods=['POST'])
def speak():
    try:
        data = request.json
        text = data.get('text', '')

        if not text:
            return jsonify({
                "success": False,
                "message": "No text provided"
            }), 400

        threading.Thread(target=talk, args=(text,)).start()

        return jsonify({
            "success": True,
            "message": "Speaking..."
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        "status": "online",
        "features": {
            "weather": bool(weather_api_key),
            "news": bool(news_api_key),
            "qa": bool(huggingface_token)
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
