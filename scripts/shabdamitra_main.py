import os
import shutil
import logging
from pydub import AudioSegment
import speech_recognition as sr
from datetime import datetime
from googletrans import Translator
from langdetect import detect

# Create logger folder if it doesn't exist
log_folder = "logger"
os.makedirs(log_folder, exist_ok=True)

# Setup logging with a timestamped log file inside the "logger" folder
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(log_folder, f"Shabdamitra_log_{timestamp}.txt")

# Configure logging to only write to file with utf-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8")  # Log file with utf-8 encoding
    ],
)
logger = logging.getLogger()


def convert_to_wav(input_path, output_path="temp_audio.wav"):
    logger.info(f"Converting {input_path} to wav format.")
    try:
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format="wav")
        logger.info(f"Conversion successful. Saved as {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"Error during audio conversion: {e}")
        raise


def split_audio(file_path, chunk_length_ms=60000):
    logger.info(f"Splitting audio file {file_path} into chunks.")
    try:
        audio = AudioSegment.from_wav(file_path)
        chunks = [
            audio[i : i + chunk_length_ms]
            for i in range(0, len(audio), chunk_length_ms)
        ]
        chunk_paths = []
        os.makedirs("temp_chunks", exist_ok=True)
        for i, chunk in enumerate(chunks):
            chunk_name = f"temp_chunks/chunk{i}.wav"
            chunk.export(chunk_name, format="wav")
            chunk_paths.append(chunk_name)
        logger.info(f"Audio split into {len(chunks)} chunks.")
        return chunk_paths
    except Exception as e:
        logger.error(f"Error while splitting audio: {e}")
        raise


def detect_language_from_text(text):
    try:
        lang = detect(text)
        logger.info(f"Detected language: {lang}")
        return lang
    except Exception as e:
        logger.error(f"Language detection failed: {e}")
        return "unknown"


def recognize_speech_auto_language(audio_file):
    logger.info(f"Auto-recognizing language from {audio_file}")
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        # Try with Hindi first
        try:
            text_hi = recognizer.recognize_google(audio, language="hi-IN")
            lang_hi = detect_language_from_text(text_hi)
            if lang_hi == "hi":
                logger.info("Final language detected: Hindi")
                return text_hi.strip(), "hi-IN"
        except:
            pass

        # Then try with English
        try:
            text_en = recognizer.recognize_google(audio, language="en-IN")
            lang_en = detect_language_from_text(text_en)
            if lang_en == "en":
                logger.info("Final language detected: English")
                return text_en.strip(), "en-IN"
        except:
            pass

        return "", "unknown"

    except Exception as e:
        logger.error(f"Error during language auto recognition: {e}")
        return "", "unknown"


def translate_to_english(hindi_text):
    logger.info("Translating Hindi text to English.")
    translator = Translator()
    try:
        translation = translator.translate(hindi_text, src="hi", dest="en")
        logger.info("Translation successful.")
        return translation.text
    except Exception as e:
        logger.error(f"Error during translation: {e}")
        return ""


if __name__ == "__main__":
    # 📥 Step 1: Define input path
    input_audio = (
        "C:\\Users\\Harshit Mishra\\Desktop\\Github\\Shabdamitra\\input\\a.mp4"
    )

    # 🕓 Step 2: Timestamp for output files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 📤 Step 3: Output directories
    hindi_output_dir = (
        "C:\\Users\\Harshit Mishra\\Desktop\\Github\\Shabdamitra\\output\\hindi"
    )
    english_output_dir = (
        "C:\\Users\\Harshit Mishra\\Desktop\\Github\\Shabdamitra\\output\\english"
    )
    os.makedirs(hindi_output_dir, exist_ok=True)
    os.makedirs(english_output_dir, exist_ok=True)

    try:
        # 🎧 Step 4: Convert audio to wav
        temp_wav = convert_to_wav(input_audio)

        # ✂️ Step 5: Split audio into chunks
        chunks = split_audio(temp_wav, chunk_length_ms=30000)

        # 🗣️ Step 6: Recognize speech and auto-detect language
        full_text = ""
        detected_language = ""

        for chunk_path in chunks:
            logger.info(f"Processing chunk: {chunk_path}")
            text, lang = recognize_speech_auto_language(chunk_path)
            if lang != "unknown":
                full_text += text + " "
                detected_language = lang  # Use last known valid detection

        full_text = full_text.strip()

        # 🌐 Step 7: Handle according to detected language
        if detected_language == "hi-IN":
            hindi_output = os.path.join(hindi_output_dir, f"{timestamp}.txt")
            with open(hindi_output, "w", encoding="utf-8") as f:
                f.write(full_text)
            logger.info(f"Hindi text saved to {hindi_output}")

            full_english_text = translate_to_english(full_text)
            english_output = os.path.join(english_output_dir, f"{timestamp}.txt")
            with open(english_output, "w", encoding="utf-8") as f:
                f.write(full_english_text.strip())
            logger.info(f"English text saved to {english_output}")

        elif detected_language == "en-IN":
            english_output = os.path.join(english_output_dir, f"{timestamp}.txt")
            with open(english_output, "w", encoding="utf-8") as f:
                f.write(full_text)
            logger.info(f"English text saved to {english_output}")

        else:
            logger.error("Could not detect language.")
            print("❌ Language could not be detected.")

        # 🧹 Step 8: Clean temp files
        if os.path.exists("temp_chunks"):
            shutil.rmtree("temp_chunks")
        if os.path.exists(temp_wav):
            os.remove(temp_wav)

        logger.info("Temporary files cleaned up.")
        print(f"\n✅ Speech recognition & translation complete.")
        if detected_language == "hi-IN":
            print(f"📝 Hindi: {hindi_output}")
            print(f"📝 English: {english_output}")
        elif detected_language == "en-IN":
            print(f"📝 English: {english_output}")
    except Exception as e:
        logger.error(f"Error in main process: {e}")
        print("❌ An error occurred. Please check the logs.")
