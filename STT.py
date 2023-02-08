from turtle import width
import streamlit as st
import pandas as pd
import numpy as np
import meta
from utils.st import (remote_css, local_css,)
import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

st.set_page_config(
        page_title="VoiceCaption: Turn your words into text with VoiceCaption - Effortlessly transcribe, simplify and preserve your thoughts.",
        page_icon="🎤",
        layout="wide",
        initial_sidebar_state="expanded"
    )
col1, col2= st.columns([4, 6])
local_css("style.css")
with col1:
    from PIL import Image
    image = Image.open('stt.png')
    st.image(image, width=300)
    st.markdown(meta.SIDEBAR_INFO, unsafe_allow_html=True)
    with st.expander("Here is how to make me help you 👇", expanded=False):
        st.markdown(meta.STORY, unsafe_allow_html=True)

with col2:
    st.markdown(meta.HEADER_INFO, unsafe_allow_html=True)
    st.markdown(meta.CHEF_INFO, unsafe_allow_html=True)
    audio_lang = st.selectbox("Choose your audio file language", index=1, options=["English", "French", "German"])
    if audio_lang == "English":
        model_type = "en-US_BroadbandModel"
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            file = split_tup = os.path.splitext(uploaded_file.name)
            file = file[1].replace(".", "")
            #print(file)
            audio_type = "audio/" + str(file)
            transcribe = st.button('Transcribe 💡')
            if transcribe:
                authenticator = IAMAuthenticator(st.secrets["authenticator"]) 
                service = SpeechToTextV1(authenticator = authenticator)
                #Insert URL in place of 'API_URL' 
                service.set_service_url(st.secrets["url"])
   
# Insert local mp3 file path in
# place of 'LOCAL FILE PATH' 
                dic = json.loads(
                    json.dumps(service.recognize(audio=uploaded_file,
                    content_type=audio_type,   
                    word_alternatives_threshold=0.9,
                    smart_formatting = True,
                    speaker_labels = True,
                    model=model_type).get_result(), indent=2))
  
# Stores the transcribed text
                transcribed_text = ""
  
                while bool(dic.get('results')):
                    transcribed_text = dic.get('results').pop().get('alternatives').pop().get('transcript')+transcribed_text[:]
                text = st.text_area("Results", transcribed_text, height=300)
                st.download_button(label="Download Transcript", data=transcribed_text, file_name="transcript.text")
    
