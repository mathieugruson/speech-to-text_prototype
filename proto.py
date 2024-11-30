import os
from pydub import AudioSegment
from openai import OpenAI
import os
from dotenv import load_dotenv
import openai

# Load environment variables from the .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to split audio into chunks
def split_or_retrieve_audio(input_file, chunk_size_mb=1.2, output_folder="chunks"):
    """
    Splits an audio file into chunks if the output folder does not exist.
    If the folder exists, retrieves the filenames of the chunks.

    Args:
        input_file (str): Path to the input audio file.
        chunk_size_mb (float): Maximum size of each chunk in megabytes (default: 1.2 MB).
        output_folder (str): Folder to save or retrieve the chunks.

    Returns:
        list: A list of file paths to the audio chunks.
    """
    # Check if the folder already exists
    if os.path.exists(output_folder):
        print(f"Folder '{output_folder}' exists. Retrieving existing files...")
        chunks = [
            os.path.join(output_folder, f) for f in sorted(os.listdir(output_folder))
            if f.endswith(".mp3")  # Adjust if you use a different format
        ]
        if not chunks:
            print(f"No audio chunks found in '{output_folder}'.")
        return chunks

    # Folder does not exist; create it and split the audio
    os.makedirs(output_folder, exist_ok=True)
    print(f"Splitting audio into {chunk_size_mb} MB chunks...")
    
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    
    # Calculate chunk duration in milliseconds
    chunk_size_bytes = chunk_size_mb * 1024 * 1024  # Convert MB to bytes
    average_bitrate = (audio.frame_rate * audio.frame_width * audio.channels * 8)  # Bitrate in bits/sec
    chunk_duration_ms = (chunk_size_bytes * 8) / average_bitrate * 1000  # Convert to milliseconds
    
    # Split audio into chunks
    chunks = []
    for i in range(0, len(audio), int(chunk_duration_ms)):
        chunk = audio[i:i + int(chunk_duration_ms)]
        chunk_file = os.path.join(output_folder, f"chunk_{i // int(chunk_duration_ms)}.mp3")
        chunk.export(chunk_file, format="mp3")
        chunks.append(chunk_file)
    
    return chunks

# Function to transcribe audio chunks
def transcribe_audio_chunks(chunks, model="whisper-1"):
    client = OpenAI()
    transcription_text = ""

    for chunk_file in chunks:
        with open(chunk_file, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                response_format="text"
            )
            print(transcription)
            transcription_text += transcription + " "
    
    return transcription_text.strip()

# Main function
def main():
    input_audio = "senat.mp3"  # Path to your 124MB audio file
    chunk_folder = "audio_chunks"
    
    # Step 1: Split the audio into chunks
    print("Splitting audio into chunks...")
    chunks = split_or_retrieve_audio(input_audio, output_folder=chunk_folder)
    print(f"Audio split into {len(chunks)} chunks.")
    
    # Step 2: Transcribe the audio chunks
    print("Transcribing audio chunks...")
    transcription = transcribe_audio_chunks(chunks)
    print("Transcription complete.")
    
    # Save transcription to file
    with open("transcription.txt", "w", encoding="utf-8") as output_file:
        output_file.write(transcription)
    print("Transcription saved to 'transcription.txt'.")

if __name__ == "__main__":
    main()
