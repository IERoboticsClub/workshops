import webbrowser  # open blackboard etc
from tempfile import TemporaryFile

import geocoder  # get location
import numpy as np
import pandas as pd
import requests  # make API GET Requests
import speech_recognition as sr  # Recognize audio
import streamlit as st
from gtts import gTTS  # Google Text to Speech
from pygame import mixer
from streamlit_chat import message

st.set_page_config(
    page_title="Talk To Jarvis",
    page_icon="📝",
)

top_news_url = ('https://newsapi.org/v2/top-headlines?country=gb&apiKey=4956d442731e4f4a9c6b8ab201436a83')

def Text_to_speech(text):
    message(text, avatar_style="bottts", seed="Felix") 
    speech = gTTS(text = text, lang='en')
    mixer.init()
    sf = TemporaryFile()
    speech.write_to_fp(sf)
    sf.seek(0)
    mixer.music.load(sf)
    mixer.music.play()
    while mixer.music.get_busy():
        pass


listener = sr.Recognizer()
def take_command():
    command = ''
    try:
        with sr.Microphone() as source:
            print('listening...')
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(voice)
            command = command.lower().replace('alexa', '')
            
    except Exception as e:
        print(e)
    return command

def print_command(command):
    message(command, is_user=True) 

def run_alexa():
    
    with st.container():
        while True:
            command = take_command()

            if 'blackboard' in command:
                print_command(command)
                Text_to_speech('I am opening blackboard')
                webbrowser.open('https://blackboard.ie.edu/')
            elif ('mail' or 'gmail' or 'inbox') in command:
                print_command(command)
                Text_to_speech('I am opening mail..')
                webbrowser.open('https://mail.google.com/mail/u/0/#inbox')
            elif 'notion' in command:
                print_command(command)
                Text_to_speech('I am opening notion')
                webbrowser.open('https://www.notion.so/')
            elif 'joke' in command:
                print_command(command)
                response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
                if response.status_code == 200:
                    joke = response.json()["joke"]
                    Text_to_speech(joke)
                else:
                    print("Failed to retrieve joke. Status code:", response.status_code)
            elif 'weather' in command:
                print_command(command)
                g = geocoder.ip('me')
                response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={g.latlng[0]}&lon={g.latlng[1]}&appid=6a135bc7b549672e2c7ad106580fc8aa&units=metric"
        , headers={"Accept": "application/json"})
                if response.status_code == 200:
                    weather = response.json()

                    Text_to_speech(f"In {weather['name']} it is currently and {weather['weather'][0]['main']} and {weather['main']['temp']} °C")
                else:
                    print("Failed to retrieve weather. Status code:", response.status_code)
            


            elif 'news about' in command:
                print_command(command)
                search_query = command.split("news about")[1]
                response = requests.get(F'https://newsapi.org/v2/top-headlines?q={search_query}&apiKey=4956d442731e4f4a9c6b8ab201436a83', headers={"Accept": "application/json"})
                if response.status_code == 200:
                    articles = response.json()['articles']
                    count = 0
                    for article in articles:
                        Text_to_speech(article['title'])
                        print(article['title'])
                        if count == 2:
                            break
                        count = count + 1
                else:
                    print("Failed to retrieve news. Status code:", response.status_code)


            elif 'news' in command:
                print_command(command)
                response = requests.get(top_news_url, headers={"Accept": "application/json"})
                if response.status_code == 200:
                    articles = response.json()['articles']
                    count = 0
                    for article in articles:
                        Text_to_speech(article['title'])
                        print(article['title'])
                        if count == 5:
                            break
                        count = count +1
                else:
                    print("Failed to retrieve news. Status code:", response.status_code)

            elif 'plot of' in command:
                print_command(command)
                search_query = command.split("plot of")[1]
                response = requests.get(f'https://www.omdbapi.com/?t={search_query}&plot=full&apiKey=9e1b88d0', headers={"Accept": "application/json"})
                if response.status_code == 200:
                    plot = response.json()['Plot']
                    Text_to_speech(plot)
                else:
                    print("Failed to retrieve plot. Status code:", response.status_code)

            elif 'terminate' in command:
                print("Terminated")
                break


st.header("Talk to Jarvis")

st.caption("Some of the many features of Jarvis include: ")

# create 7 columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write("🌤️ Weather ")
  
with col2:
    st.write("📚 Blackboard")

with col3:
    st.write("📝 Notion")

with col4:
    st.write("📰 News ")

# create a container in between the columns

col1, col2, col3 = st.columns(3)




with st.sidebar:
    st.image("https://www.scribblemagiclab.com/wp-content/wphb-cache/gravatar/5cd/5cdc35b0e8289f3738a632e15bb20c5bx500.jpg", width=300)



col1, col2 = st.columns(2)

with col1:
    if st.button('Run Jarvis'):
        with st.spinner('Listening..'):
            st.caption("To stop the program, say: \"Terminate.\"")
            st.session_state.is_alexa_running = True
            run_alexa()

with col2:
    if st.button('Stop Jarvis'):
        st.session_state.is_alexa_running = False

