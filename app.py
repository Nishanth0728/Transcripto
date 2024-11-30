from flask import Flask, request, render_template
from youtube_transcript_api import YouTubeTranscriptApi as yta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_transcript', methods=['POST'])
def get_transcript():
    video_id = request.form.get('video_id')
    if not video_id:
        return "Please provide a valid YouTube Video ID."

    try:
        # Fetch the transcript
        data = yta.get_transcript(video_id)
        transcript = " ".join([entry['text'] for entry in data])

        # Render the transcript on the page
        return render_template('transcript.html', transcript=transcript)

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
