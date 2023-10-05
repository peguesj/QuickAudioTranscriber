import logging
import os
from datetime import datetime
from pydub import AudioSegment
import speech_recognition as sr
import tempfile
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create a directory for transcripts if it doesn't exist
if not os.path.exists('transcripts'):
    os.makedirs('transcripts')

# Generate timestamped filename for the transcript
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
transcript_filename = f'transcripts/transcript_{timestamp}.txt'

# Function to transcribe audio
def transcribe_audio(i, chunk):
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_filename = temp_file.name + ".wav"
        logging.debug(f"Exporting audio to temporary file: {temp_filename}")
        chunk.export(temp_filename, format="wav")
        
        recognizer = sr.Recognizer()
        logging.debug(f"Starting transcription for file: {temp_filename}")
        with sr.AudioFile(temp_filename) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                logging.debug(f"Transcription successful for chunk {i + 1}. Sample text: {text[:50]}...")
                return text
            except sr.UnknownValueError:
                logging.error(f"Could not understand audio in chunk {i + 1}")
                return "Could not understand audio"
            except sr.RequestError as e:
                logging.error(f"Could not request results in chunk {i + 1}; {e}")
                return f"Could not request results; {e}"

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

with ThreadPoolExecutor() as executor:
    future_to_chunk = {executor.submit(transcribe_audio, i, chunk): chunk for i, chunk in enumerate(chunks)}
    with open(transcript_filename, 'w') as f:
        for future in future_to_chunk:
            chunk_text = future.result()
            transcribed_text += chunk_text + " "
            logging.debug(f"Appending text from completed chunk to transcript.")

# Output the entire combined transcribed text to both stdout and the transcript file
logging.debug("Transcription process completed. Outputting sample text.")
print(transcribed_text[:500])
with open(transcript_filename, 'a') as f:
    f.write("\n\n--- Full Transcript ---\n")
    f.write(transcribed_text)
