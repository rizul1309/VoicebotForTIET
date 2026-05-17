# 🎙️ VoicebotForTIET

A voice-powered chatbot built for **Thapar Institute of Engineering and Technology (TIET)** that helps users find campus locations — offices, labs, and faculty cabins — using natural voice commands. It combines **Rasa NLU** for understanding user intent, **Google Speech Recognition** for voice input, and **Google Text-to-Speech (gTTS)** for spoken responses.

---

## 📑 Table of Contents

- [How It Works (End-to-End Flow)](#how-it-works-end-to-end-flow)
- [Project Structure](#project-structure)
- [Detailed File Explanations](#detailed-file-explanations)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Project](#running-the-project)
- [Web Interface](#web-interface)
- [How Rasa Works in This Project](#how-rasa-works-in-this-project)
- [Deployment Guide](#deployment-guide)
- [Troubleshooting](#troubleshooting)

---

## How It Works (End-to-End Flow)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        VOICEBOT PIPELINE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. User speaks into microphone                                     │
│         │                                                           │
│         ▼                                                           │
│  2. speech_recognition library captures audio                       │
│         │                                                           │
│         ▼                                                           │
│  3. Google Speech Recognition API converts audio → text             │
│         │                                                           │
│         ▼                                                           │
│  4. Text sent via HTTP POST to Rasa server (localhost:5002)         │
│         │                                                           │
│         ▼                                                           │
│  5. Rasa NLU classifies intent & extracts entities                  │
│     (e.g., intent: ask_for_lab, entity: "programming lab 1")       │
│         │                                                           │
│         ▼                                                           │
│  6. Rasa Core picks the next action based on trained stories        │
│         │                                                           │
│         ▼                                                           │
│  7. Custom actions (action_show_cabin_dir, action_show_lab)         │
│     return location information                                     │
│         │                                                           │
│         ▼                                                           │
│  8. Response text returned via REST API                             │
│         │                                                           │
│         ▼                                                           │
│  9. gTTS converts response text → MP3 audio file                   │
│         │                                                           │
│         ▼                                                           │
│  10. playsound plays the audio to the user                          │
│         │                                                           │
│         ▼                                                           │
│  11. Temporary MP3 file is deleted, loop repeats                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
VoicebotForTIET/
│
├── voicebot.py                  # Main application — full voice conversation loop
├── voice_to_text.py             # Standalone utility: microphone → text
├── text_to_voice.py             # Standalone utility: text → speech audio
│
├── data/
│   ├── nlu.md                   # Rasa NLU training data (intents & entities)
│   └── stories.md               # Rasa conversation flow stories
│
├── tests/
│   └── conversation_tests.md    # End-to-end conversation test cases
│
├── templates/
│   ├── IY_Home_page.html        # Web-based chat interface (frontend)
│   ├── rrbclkadmit.html         # Sample HTML template (test artifact)
│   └── rrbclkadmit_files/       # Static assets for the sample template
│
└── __pycache__/                 # Python bytecode cache (auto-generated)
```

---

## Detailed File Explanations

### `voicebot.py` — The Main Application

This is the **heart of the project**. It runs the full voice conversation loop:

1. **Starts the conversation** by sending "Hello" to the Rasa server
2. **Converts the bot's reply to speech** using gTTS and plays it
3. **Enters a loop** where it:
   - Listens to the user's microphone input
   - Converts speech to text using Google Speech Recognition
   - Sends the text to Rasa's REST webhook endpoint
   - Receives the bot's response
   - Converts the response to speech and plays it
4. **Exits** when the bot says "Bye" or "thanks"

```python
# Key endpoint used:
r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})
```

---

### `voice_to_text.py` — Speech-to-Text Utility

A **standalone demo script** that shows how speech recognition works in isolation. It:
- Initializes the `speech_recognition` recognizer
- Captures audio from the microphone
- Sends it to Google's Speech Recognition API
- Prints the recognized text

Use this to **test your microphone setup** before running the full bot.

---

### `text_to_voice.py` — Text-to-Speech Utility

A **standalone demo script** that shows how text-to-speech works in isolation. It:
- Takes a hardcoded text string
- Converts it to an MP3 file using gTTS
- Plays the MP3 using `playsound`

Use this to **test your audio output** before running the full bot.

---

### `data/nlu.md` — NLU Training Data

This file teaches Rasa **what users might say** and how to classify it. It defines:

| Intent | Purpose | Example Phrases |
|--------|---------|-----------------|
| `greet` | User says hello | "hey", "hello", "good morning" |
| `goodbye` | User says bye | "bye", "see you later" |
| `affirm` | User confirms | "yes", "of course", "correct" |
| `deny` | User denies | "no", "never", "not really" |
| `ask_for_cabin` | User asks for an office/cabin location | "Where is dean office", "room no of director" |
| `ask_for_lab` | User asks for a lab location | "Where is programming lab 1", "directions to computer graphics lab" |
| `mood_great` | User is happy | "perfect", "amazing", "I am great" |
| `mood_unhappy` | User is sad | "sad", "terrible", "not very good" |
| `bot_challenge` | User asks if it's a bot | "are you a bot?", "am I talking to a human?" |

**Entities extracted:**
- `designation` — faculty/admin role (dean, dosaa, director)
- `lab` — lab name (programming lab 1, Engineering Design Lab 1, etc.)

---

### `data/stories.md` — Conversation Stories

This file teaches Rasa **how conversations should flow**. Each story is a sequence of user intents and bot actions:

- **Happy path:** greet → mood_great → bot says something happy
- **Sad path:** greet → mood_unhappy → bot cheers up → user affirms/denies
- **Cabin query:** greet → ask_for_cabin → `action_show_cabin_dir` (custom action returns location)
- **Lab query:** greet → ask_for_lab → `action_show_lab` (custom action returns location)
- **Goodbye:** user says bye → bot says goodbye

---

### `tests/conversation_tests.md` — Test Cases

End-to-end test scenarios that validate the bot responds correctly. Run these with:
```bash
rasa test
```

---

### `templates/IY_Home_page.html` — Web Chat Interface

A **web-based frontend** for the voicebot featuring:
- A hero section with TIET branding (address, phone, email)
- A sidebar with links to thapar.edu pages (Admissions, Webkiosk, Placements, etc.)
- A **chat popup widget** (bottom-right corner) where users can type messages
- JavaScript that sends messages via AJAX POST to a `/result` endpoint
- Styled like a modern messenger app

This template uses **Jinja2 templating** (`{% for key,value in result %}`), meaning it's served by a Flask/Python backend.

---

## Prerequisites

Before you begin, make sure you have:

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Python | 3.6 - 3.8 | Runtime (Rasa requires this range) |
| pip | Latest | Package manager |
| Microphone | Any | Voice input |
| Speakers/Headphones | Any | Audio output |
| Internet connection | — | Google Speech & TTS APIs |

---

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/rizul1309/VoicebotForTIET.git
cd VoicebotForTIET
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install rasa
pip install speech_recognition
pip install gTTS
pip install playsound
pip install requests
pip install pyaudio
pip install flask
```

> **Note on PyAudio (Windows):** If `pip install pyaudio` fails, download the appropriate `.whl` file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install it with:
> ```bash
> pip install PyAudio‑0.2.11‑cp37‑cp37m‑win_amd64.whl
> ```

### Step 4: Train the Rasa Model

```bash
rasa train
```

This reads `data/nlu.md`, `data/stories.md`, and your `domain.yml` + `config.yml` to produce a trained model in the `models/` directory.

> **Important:** You will need a `domain.yml` and `config.yml` file for Rasa to train. If they are missing, create them (see [How Rasa Works](#how-rasa-works-in-this-project) section below).

---

## Running the Project

You need **three terminal windows** running simultaneously:

### Terminal 1: Start the Rasa Server

```bash
rasa run --port 5002 --enable-api --cors "*"
```

This starts the Rasa server on port 5002, which the voicebot communicates with.

### Terminal 2: Start the Rasa Actions Server

```bash
rasa run actions
```

This runs custom actions like `action_show_cabin_dir` and `action_show_lab` that return location information.

### Terminal 3: Run the Voicebot

```bash
python voicebot.py
```

The bot will:
1. Greet you with a spoken message
2. Wait for you to speak
3. Process your voice command
4. Respond with spoken audio
5. Repeat until the conversation ends

### Alternative: Test Individual Components

```bash
# Test microphone (speech-to-text only):
python voice_to_text.py

# Test speakers (text-to-speech only):
python text_to_voice.py
```

---

## Web Interface

To use the web-based chat interface instead of voice:

1. You need a Flask server (not included in repo) that serves `templates/IY_Home_page.html`
2. The Flask app should have a `/result` POST endpoint that forwards messages to Rasa
3. Example minimal Flask app:

```python
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('IY_Home_page.html')

@app.route('/result', methods=['POST'])
def result():
    user_message = request.form.get('message')
    r = requests.post('http://localhost:5002/webhooks/rest/webhook',
                      json={"message": user_message})
    bot_response = [i['text'] for i in r.json()]
    return jsonify(bot_response)

if __name__ == '__main__':
    app.run(debug=True)
```

---

## How Rasa Works in This Project

### Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│  User Input  │────▶│   Rasa NLU   │────▶│   Rasa Core      │
│  (text)      │     │  (classifies │     │  (picks action   │
│              │     │   intent)    │     │   from stories)  │
└──────────────┘     └──────────────┘     └──────────────────┘
                                                    │
                                                    ▼
                                          ┌──────────────────┐
                                          │  Action Server   │
                                          │  (custom logic)  │
                                          └──────────────────┘
                                                    │
                                                    ▼
                                          ┌──────────────────┐
                                          │  Bot Response    │
                                          │  (text)          │
                                          └──────────────────┘
```

### Key Rasa Files (you may need to create these)

**`domain.yml`** — Defines the bot's universe:
```yaml
intents:
  - greet
  - goodbye
  - affirm
  - deny
  - ask_for_cabin
  - ask_for_lab
  - mood_great
  - mood_unhappy
  - bot_challenge

entities:
  - designation
  - lab

actions:
  - action_show_cabin_dir
  - action_show_lab

responses:
  utter_greet:
    - text: "Hey! I'm the TIET VoiceBot. How can I help you?"
  utter_happy:
    - text: "Great! Let me know if you need anything."
  utter_cheer_up:
    - text: "Here's something to cheer you up!"
  utter_did_that_help:
    - text: "Did that help you?"
  utter_goodbye:
    - text: "Bye! Have a great day."
  utter_iamabot:
    - text: "I am a bot, powered by Rasa."
```

**`config.yml`** — Defines the NLU pipeline:
```yaml
language: en

pipeline:
  - name: WhitespaceTokenizer
  - name: RegexFeaturizer
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: CountVectorsFeaturizer
    analyzer: char_wb
    min_ngram: 1
    max_ngram: 4
  - name: DIETClassifier
    epochs: 100
  - name: EntitySynonymMapper
  - name: ResponseSelector
    epochs: 100

policies:
  - name: MemoizationPolicy
  - name: TEDPolicy
    max_history: 5
    epochs: 100
  - name: RulePolicy
```

**`actions.py`** — Custom actions (you need to create this):
```python
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionShowCabinDir(Action):
    def name(self):
        return "action_show_cabin_dir"

    def run(self, dispatcher, tracker, domain):
        designation = tracker.get_slot("designation")
        # Add your cabin/office location logic here
        cabin_info = {
            "dean": "F Block, Room 201",
            "dosaa": "F Block, Room 105",
            "doaa": "F Block, Room 103",
            "director": "A Block, Room 001"
        }
        location = cabin_info.get(designation, "Sorry, I don't have that information.")
        dispatcher.utter_message(text=f"The {designation} office is at: {location}")
        return []

class ActionShowLab(Action):
    def name(self):
        return "action_show_lab"

    def run(self, dispatcher, tracker, domain):
        lab = tracker.get_slot("lab")
        # Add your lab location logic here
        lab_info = {
            "programming lab 1": "D Block, Room 301",
            "engineering design lab 1": "C Block, Room 201",
            "system software lab 1": "D Block, Room 302",
            "computer graphics lab": "D Block, Room 303",
            "office csed": "D Block, Room 101",
            "cloud and iot research lab": "D Block, Room 401",
            "doctoral research lab 4": "D Block, Room 402"
        }
        location = lab_info.get(lab.lower() if lab else "", "Sorry, I don't have that information.")
        dispatcher.utter_message(text=f"The {lab} is at: {location}")
        return []
```

---

## Deployment Guide

### Local Deployment (Development)

1. Train the model: `rasa train`
2. Start Rasa server: `rasa run --port 5002 --enable-api --cors "*"`
3. Start actions server: `rasa run actions`
4. Run the bot: `python voicebot.py`

### Server Deployment (Production)

For deploying on a remote server (e.g., AWS, GCP, Heroku):

1. **Dockerize the Rasa server:**
   ```dockerfile
   FROM rasa/rasa:latest
   COPY . /app
   WORKDIR /app
   RUN rasa train
   CMD ["run", "--port", "5002", "--enable-api", "--cors", "*"]
   ```

2. **Deploy the actions server separately:**
   ```dockerfile
   FROM rasa/rasa-sdk:latest
   COPY actions.py /app/actions.py
   ```

3. **For the web interface**, deploy the Flask app behind Nginx/Gunicorn:
   ```bash
   gunicorn app:app --bind 0.0.0.0:5000
   ```

4. **Update the webhook URL** in `voicebot.py` from `localhost:5002` to your server's address.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Could not recognize your voice" | Check microphone permissions, reduce background noise |
| PyAudio installation fails | Use pre-built wheel file (see Installation step) |
| Rasa server connection refused | Make sure `rasa run` is active on port 5002 |
| "No module named 'rasa'" | Activate your virtual environment, reinstall rasa |
| playsound not working | Try `pip install playsound==1.2.2` (older stable version) |
| gTTS fails | Check internet connection (requires Google API access) |
| Empty bot response | Ensure Rasa model is trained (`rasa train`) |

---

## Technologies Used

| Technology | Role |
|------------|------|
| **Rasa** | NLU (intent classification, entity extraction) + Dialogue Management |
| **Google Speech Recognition** | Converts voice → text (via `speech_recognition` library) |
| **Google Text-to-Speech (gTTS)** | Converts text → spoken audio |
| **Flask** | Web server for the chat interface |
| **Jinja2** | HTML templating for the web frontend |
| **jQuery** | AJAX calls in the web chat widget |
| **Python** | Core programming language |

---

## License

This project was built as a campus utility for TIET students and staff.

---

## Author

Built by [rizul1309](https://github.com/rizul1309)
