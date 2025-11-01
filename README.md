# Voice Assistant - Setup Instructions 

## Quick Start Guide

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note for PyAudio installation:**
- **Windows**: `pip install pipwin` then `pipwin install pyaudio`
- **Mac**: `brew install portaudio` then `pip install pyaudio`
- **Linux**: `sudo apt-get install portaudio19-dev` then `pip install pyaudio`

### 2. Configure Environment Variables

Create a `.env` file in the project root with your API keys:

```env
WEATHER_API_KEY=your_openweather_api_key
NEWS_API_KEY=your_news_api_key
IPINFO_TOKEN=your_ipinfo_token
HUGGINGFACE_TOKEN=your_huggingface_token
```

**Where to get API keys:**
- **Weather**: [OpenWeather API](https://openweathermap.org/api) (Free tier available)
- **News**: [News API](https://newsapi.org/) (Free tier available)
- **IPInfo**: [IPInfo.io](https://ipinfo.io/) (Optional)
- **HuggingFace**: [HuggingFace](https://huggingface.co/settings/tokens) (Free)

### 3. Start the Backend Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 4. Open the Web Interface

Open your browser and navigate to:
```
http://localhost:5000
```

## Features

### Voice Commands
Click the microphone button and speak any command:
- "Alexa play [song name]" - Play music on YouTube
- "Alexa time" - Get current time
- "Alexa weather" - Get weather updates
- "Alexa news" - Get latest headlines
- "Alexa who is [person]" - Wikipedia search
- "Alexa joke" - Get a random joke
- "Alexa question" - Ask a question

### Text Commands
Type commands directly in the input field:
- Same commands work without saying "Alexa"
- Press Enter or click send button

## Troubleshooting

### Microphone not working?
- Check browser permissions (allow microphone access)
- Ensure PyAudio is properly installed
- Test your microphone in system settings

### Backend not connecting?
- Make sure `python app.py` is running
- Check if port 5000 is available
- Look for error messages in the terminal

### API features not working?
- Verify your API keys in `.env` file
- Check API key validity and quotas
- Some features require valid API keys

## Architecture

- **Frontend**: HTML/CSS/JavaScript (Vanilla JS)
- **Backend**: Flask (Python)
- **Speech Recognition**: Google Speech Recognition API
- **Text-to-Speech**: pyttsx3 (offline)
- **APIs**: OpenWeather, News API, HuggingFace, Wikipedia

## Sharing with Users

To share this with users:

1. **Deploy Backend**: Use services like Heroku, Railway, or PythonAnywhere
2. **Configure CORS**: Update allowed origins in `app.py`
3. **Environment Variables**: Set API keys in hosting platform
4. **Frontend**: Can be served by Flask or deployed separately

### Example Deployment (Railway)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

## Development

### Run in Development Mode
```bash
# Backend with auto-reload
python app.py

# The app runs on port 5000 by default
```

### File Structure
```
project/
├── app.py              # Flask backend API
├── main.py             # Original CLI version
├── index.html          # Frontend UI
├── styles.css          # Styling
├── requirements.txt    # Python dependencies
├── .env               # API keys (create this)
└── README.md          # Documentation
```

## Security Notes

- Never commit `.env` file to version control
- Use environment variables for API keys
- Validate user input on the backend
- Implement rate limiting for production use

## Support

For issues or questions, please refer to the original repository or create an issue on GitHub.
