from youtube_transcript_api import YouTubeTranscriptApi as yta

# Video ID of the YouTube video
vid_id = 'oe492FoGYng'

# Fetch the transcript using the API
try:
    data = yta.get_transcript(vid_id)

    # Combine all text entries into a single string
    transcript = " ".join([entry['text'] for entry in data])

    # Save the transcript to a text file
    with open("Text.txt", 'w', encoding='utf-8') as file:
        file.write(transcript)

    print("Transcript saved successfully to Text.txt!")

except Exception as e:
    print(f"An error occurred: {e}")
