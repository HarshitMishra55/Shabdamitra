# Shabdamitra Project

## 🧠 Project Goal

Convert voice input (Allahabadi, Hindi, Hinglish) to formal **Hindi and English** — both **text** and **audio** output.

---

## 📁 Project Structure

Shabdamitra/
├── data/ # Training datasets and language corpora
├── input/ # Raw voice input files (e.g., .mp4 or .wav)
├── output/ # Final outputs (text + audio)
│ ├── hindi/ # Formal Hindi text
│ └── english/ # Formal English translation
├── model/ # ML/NLP models and checkpoints
├── scripts/ # Python scripts (main logic & utilities)
│ └── shabdamitra_main.py
├── logger/ # Timestamped logs
├── requirements.txt # All Python dependencies
└── README.md # Project documentation

---

## 🔧 Features

- ✅ Converts MP4 audio to WAV format.
- ✅ Automatically detects language (Hindi or English).
- ✅ Transcribes audio to text.
- ✅ Translates Hindi to English.
- ✅ Stores outputs as `.txt` files.
- ✅ Logs entire process in UTF-8 encoded timestamped files.
- ❌ _[Coming soon]_ Text-to-speech for formal Hindi & English output.

---

## 🚀 Setup Instructions

### 1. Clone the Repository

git clone https://github.com/HarshitMishra55/Shabdamitra.git
cd Shabdamitra

### 2. Create a Virtual Environment (Recommended)

python -m venv venv
venv\Scripts\activate # On Windows
source venv/bin/activate # On Linux/Mac

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Place Audio File

Put your .mp4 or .wav file in the /input/ folder.
Example:
input/a.mp4

### Run the Main Script

python scripts/shabdamitra_main.py

## Output

Hindi transcription saved at: output/hindi/<timestamp>.txt

English translation saved at: output/english/<timestamp>.txt

Logs stored at: logger/Shabdamitra*log*<timestamp>.txt

## Note

Works only for Hindi and English audio as of now.

Use short and clear audio for best results.

Background noise may affect transcription quality.
