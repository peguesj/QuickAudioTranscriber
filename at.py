import logging
from pydub import AudioSegment
import speech_recognition as sr
import tempfile
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Function to transcribe audio
def transcribe_audio(audio_segment, temp_filename):
    logging.debug(f"Exporting audio to temporary file: {temp_filename}")
    audio_segment.export(temp_filename, format="wav")
    
    recognizer = sr.Recognizer()
    logging.debug(f"Starting transcription for file: {temp_filename}")
    with sr.AudioFile(temp_filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            logging.debug(f"Transcription successful for chunk. Sample text: {text[:50]}...")
        except sr.UnknownValueError:
            logging.error("Could not understand audio")
            return "Could not understand audio"
        except sr.RequestError as e:
            logging.error(f"Could not request results; {e}")
            return f"Could not request results; {e}"
    return text

logging.debug("Initializing...")

# Load the audio file
audio_path = "audio.wav"
logging.debug(f"Loading audio file from: {audio_path}")
audio = AudioSegment.from_file(audio_path, format="wav")

# Divide the audio into 30-second chunks for easier processing
chunk_length = 30 * 1000  # in milliseconds
logging.debug(f"Dividing audio into chunks of {chunk_length} milliseconds")
chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]

# Transcribe each chunk and collect the text
logging.debug("Starting transcription process...")
transcribed_text = ""
for i, chunk in enumerate(chunks):
    logging.debug(f"Processing chunk {i + 1}...")
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_filename = temp_file.name + ".wav"
        chunk_text = transcribe_audio(chunk, temp_filename)
        transcribed_text += chunk_text + " "
        logging.debug(f"Sample text from chunk {i + 1}: {chunk_text[:50]}")

# Output a sample of the transcribed text
logging.debug("Transcription process completed. Outputting sample text.")
print(transcribed_text[:500])
