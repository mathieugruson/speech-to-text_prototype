# Speech-to-Text Transcription Project

This project provides an efficient solution for converting audio files into text using OpenAI's Whisper API. It supports chunking of large audio files, retrieving existing preprocessed chunks, and generating accurate transcriptions.

## Purpose of the Project

Transcription of audio and video content is invaluable, especially when a text transcript is unavailable. For instance, consider the **[colloque sur le consentement et la définition pénale du viol](https://videos.senat.fr/video.4855134_673e11ca87771.colloque-sur-le-consentement-et-la-definition-penale-du-viol?timecode=1191000)** hosted on the Senate's video portal. This important discussion lacks a text transcript, making it less accessible for analysis or quick review, as it lasts 3 hours.

This project aims to address such challenges by:
- Automatically transcribing audio files into readable text.
- Improving accessibility for people with hearing impairments.
- Enabling quicker analysis and review of video or audio content.

## Features

- **Audio Splitting**: Automatically splits large audio files into smaller chunks to meet API size constraints.
- **File Reuse**: Checks for pre-existing chunks in the folder to avoid redundant processing.
- **Accurate Transcriptions**: Utilizes OpenAI's Whisper API for reliable speech-to-text conversion.
- **Output Management**: Saves transcriptions to a text file for easy access.

## Prerequisites

1. **Python**: Ensure Python 3.7 or higher is installed.
2. **OpenAI API Key**: Obtain an API key from OpenAI and set it in a `.env` file.
3. **Required Libraries**: Install dependencies with pip:
   ```bash
   pip install openai pydub python-dotenv
