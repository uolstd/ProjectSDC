import streamlit as st
from transformers import pipeline
import os
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id: str):
    ls = YouTubeTranscriptApi.get_transcript(video_id)
    tx = [d["text"]+ "" for d in ls]

    with open("ms_kitco.txt", "w") as f:
        f.write("".join(tx))
    return "".join(tx)

st.markdown("<h1 style='text-align: center; color: red;'>Video Transcript Summarizer</h1>", unsafe_allow_html=True)
full_yt  = st.text_input("Enter video link", "")
tx = ""
if st.button("Get Summary"):
    video_id = full_yt.split("=")[1]
    tx = get_transcript(video_id)
    
    with open("ms_kitco.txt", "r") as f:
        tx = f.read()
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        x3 = summarizer(tx[:4000], max_length = 230)
        res = x3[0]["summary_text"]
        st.write(res)

if st.button("Delete Transcript"):
    if os.path.exists("ms_kitco.txt"):
        os.remove("ms_kitco.txt")
        st.success("Transcript deleted successfully.")
    else:
        st.error("The transcript does not exist.")

transcript = st.text_area("Edit Transcript", tx)
if st.markdown(" Here you can edit your Transcript for your Furture need"):
    with open("ms_kitco.txt", "w") as f:
        f.write(transcript)
        # st.success("Transcript updated successfully.")
st.markdown("INSTRUCTIONS:: This Web application will only generate summary for those video who have transcript, if your video doesn't have any transcript you will face the error page")