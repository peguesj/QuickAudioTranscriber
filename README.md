# Multi-threaded Audio Transcription Script

## Metadata
- Author: Jeremiah Pegues <jeremiah@pegues.io>
- Date: 2023-10-05
- Version: 0.1
- License: GPL

## Description
This Python script transcribes audio files using the Google Web Speech API. It utilizes multi-threading to speed up the transcription process. The script is designed to be efficient and robust, providing verbose debugging information and saving transcriptions to timestamped text files.

## Features
- Multi-threaded processing for speed.
- Verbose debugging via syslog-format logs.
- Outputs transcript to a timestamped text file and standard output.
- Error handling for unknown or untranslatable audio.

## Requirements
- Python 3.x
- Install the required Python packages via pip:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Place your `.wav` audio file in the same directory as the script, or specify the path in `audio_path`.
2. Run the script:
    ```bash
    python <script_name>.py
    ```
3. Check the `transcripts` folder for the generated transcript.

## How It Works
1. The audio is divided into 30-second chunks.
2. A pool of worker threads is created.
3. Each chunk is passed to a worker thread for transcription.
4. The transcribed text of each chunk is saved to a timestamped text file and also printed to stdout.

## Logging
The script logs each action at every stage to help you monitor the transcription process closely.

## License
This project is licensed under the GPL.

---
