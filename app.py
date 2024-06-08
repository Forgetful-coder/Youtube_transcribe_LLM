import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

prompt = """You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

def video_transcript(video_link):
    try:
        video_id = video_link.split('=')[1]
        transcipt_text = YouTubeTranscriptApi.get_transcript(video_id=video_id)
        
        transcipt=''

        for i in transcipt_text:
            transcipt+= ' ' + i['text']
        return transcipt
    except Exception as e:
        raise e

def get_gemini_response(transcript,prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(transcript+prompt)
    return response.text

#Streamlit app
st.set_page_config(page_title='Youtube transcriber')
st.title('Youtube summarizer')

input = st.text_input('Enter your link here')
submit = st.button('Get your transcriptions')

if input:
    video_id = input.split('=')[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
if submit:
    text = video_transcript(input)

    if text:
        response = get_gemini_response(text,prompt)
        st.markdown('## Detailed notes')
        st.write(response)
