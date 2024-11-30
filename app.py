from flask import Flask, request, render_template
from youtube_transcript_api import YouTubeTranscriptApi as yta
from deep_translator import GoogleTranslator
import re
import os
from moviepy import VideoFileClip
import speech_recognition as sr

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    Handles multiple URL formats.
    """
    video_id_match = re.search(r"(?<=v=)[^&]+|(?<=youtu\.be/)[^?&]+", url)
    return video_id_match.group(0) if video_id_match else None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_transcript_page', methods=['GET'])
def get_transcript_page():
    return render_template('get_transcript.html')

@app.route('/get_transcript', methods=['POST'])
def get_transcript():
    video_url = request.form.get('video_url')
    target_language = request.form.get('language')

    if not video_url:
        return "Please provide a valid YouTube Video URL."

    # Extract the video ID from the URL
    video_id = extract_video_id(video_url)
    if not video_id:
        return "Invalid YouTube URL. Please check the URL format."

    try:
        # Fetch the transcript
        data = yta.get_transcript(video_id)
        transcript = " ".join([entry['text'] for entry in data])

        # Translate the transcript
        translated = GoogleTranslator(source="auto", target=target_language).translate(transcript)

        # Render the transcript page
        return render_template('transcript.html', transcript=translated)

    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/upload_page', methods=['GET'])
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'video_file' not in request.files:
        return "No file uploaded."

    video_file = request.files['video_file']
    target_language = request.form.get('language')

    if video_file.filename == '':
        return "No file selected."

    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
    video_file.save(video_path)

    try:
        # Extract audio from video
        video = VideoFileClip(video_path)
        audio_path = video_path.rsplit('.', 1)[0] + ".wav"
        video.audio.write_audiofile(audio_path)
        video.close()  # Ensure the video file is released

        # Transcribe audio to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as audio_file:
            audio = recognizer.record(audio_file)
            transcript = recognizer.recognize_google(audio)

        # Translate the transcript
        translated = GoogleTranslator(source="auto", target=target_language).translate(transcript)

        # Render the transcript page
        return render_template('transcript.html', transcript=translated)

    except Exception as e:
        return f"An error occurred: {e}"

    finally:
        # Clean up temporary files
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)

if __name__ == '__main__':
    app.run(debug=True)
