# app.py
from flask import Flask, request, render_template, redirect, url_for
from transformers import pipeline
import os
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

def get_transcript(video_id: str):
    try:
        ls = YouTubeTranscriptApi.get_transcript(video_id)
        tx = [d["text"]+ "" for d in ls]

        with open("ms_kitco.txt", "w") as f:
            f.write("".join(tx))
        return "".join(tx)
    except YouTubeTranscriptApi.TranscriptsDisabled: # change the exception class name
        return "Sorry this video doesn't have any transcript" # return the message instead of aborting

@app.route('/', methods=['GET', 'POST'])
def index():
    transcript = ""
    if request.method == 'POST':
        video_link = request.form.get('video_link')
        if "=" in video_link:
            video_id = video_link.split("=")[1]
            tx = get_transcript(video_id)
            transcript = tx # added this line
            if transcript != "Sorry this video doesn't have any transcript": # check if the transcript is valid
                summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
                x3 = summarizer(tx[:4000], max_length = 230)
                res = x3[0]["summary_text"]
                transcript = res # overwrite the transcript with the summary
        else:
            video_id = None  # or some default value

            with open("ms_kitco.txt", "r") as f:
                tx = f.read()
                summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
                x3 = summarizer(tx[:4000], max_length = 230)
                res = x3[0]["summary_text"]
                transcript = res

            if 'delete' in request.form:
                if os.path.exists("ms_kitco.txt"):
                    os.remove("ms_kitco.txt")
                    transcript = "Transcript deleted successfully."
                else:
                    transcript = "The transcript does not exist."

            # if 'update' in request.form:
            #     with open("ms_kitco.txt", "w") as f:
            #         f.write(request.form.get('transcript'))
            #         transcript = "Transcript updated successfully."

    return render_template('index.html', transcript=transcript)

if __name__ == '__main__':
    app.run(debug=True) # you can also use debug mode if you want
