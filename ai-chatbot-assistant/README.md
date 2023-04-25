#  AI - Virtual Assistant


<div style="text-align:center"><img src="./assets/jarvis.png" width="" height="180" /></div>

<!--
<br>
<div style="text-align:center"><img src="./assets/robotics.jpg" width="" height="75" /><img src="./assets/gdsc.jpg" width="" height="75" /></div>
<div style="text-align:center"></div>
<br>
-->

## Chatbots 💬 

Imagine having a digital assistant that can chat with you like a real person, providing you with instant and relevant information whenever you need it. That's the power of a chatbot AI assistant! It's a cutting-edge tool that can engage with users in real-time through a messaging interface, making it an ideal solution for businesses and organizations looking to improve customer service and support.

<br>

# Table of Contents
#### 1. Set up Docker
#### 2. [Set up Redis](#setting-up-redis)
#### 3. [Connecting a Language Model](#connecting-a-language-model)
#### &nbsp;&nbsp;&nbsp;&nbsp; 3.1 [Run Vicuna Locally](#runing-vicuna-locally)
#### &nbsp;&nbsp;&nbsp;&nbsp; 3.2 [Connect any other language model](#connecting-any-other-language-model)
#### 4. 


<br>

## Set up Docker
1. Install [Docker](https://docs.docker.com/get-docker/) on your local machine


## Setting up Redis
1. Install [Redis GUI](https://redis.com/redis-enterprise/redis-insight/) on your local machine
2. Start the Redis server in the terminal using docker image with modules
```bash
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
```
3. Add a Redis Database connection to the Redis server through the GUI 
```
Database Alias: 127.0.0.1:6379
```

<br>

# Actions for Jarvis

## Libraries Imported
The code imports several external libraries using the import statement. These libraries include:
- webbrowser
- TemporaryFile
- geocoder
- requests
- speech_recognition
- streamlit
- gtts
- pygame

## Text to Speech Function
This function uses the Google Text-to-Speech API to convert text to speech. It takes a string argument as input and outputs the corresponding speech using the mixer library.

## Voice Command Recognition

The run_alexa function uses the take_command function to recognize voice commands from the user. It listens for voice input for a maximum of 5 seconds and then returns the spoken command as a string in lowercase format.
- we initialize a listener (imagine as if it is a digital microphone)
- recognize_google (explain more in depth)
- timeout and phrase_time_limit (explain)

## Main Program Loop
The run_alexa function is the main program loop. It takes no arguments and executes indefinitely until a "terminate" command is spoken. It listens for voice commands from the user and performs the associated action by calling the corresponding function based on the recognized command.

### Opening tabs
Keywords are used to detect the type of command to execute.
- blackboard
- notion
- mail
In the above example webbrowser module is used for opening up the commanded tabs.

## Actions with APIs
_APIs are like a set of rules and protocols that allow different software programs to talk to each other and share data or functionality_

### Joke
The api that we chose for the Joke action receive a retrieves a data from an endpoint using a GET request. Then, it is converted into JSON format from where we access the Joke string.

### Weather API Endpoint
- Using geocoder library, user's geolocation is identified. 
- API key needs to be retrieved from the following website: https://api.openweathermap.org/  and put the way it is specified below.
```python
 https://api.openweathermap.org/data/2.5/weather?lat={g.latlng[0]}&lon={g.latlng[1]}&appid={API_KEY}
 ```
- With the API key the weather is retrieved.

### News about a specific topic API
https://newsapi.org/ 
- The command is split to get the keyword for the desired topic
- Sign up for an API_KEY through https://newsapi.org/ 
```python
 (https://newsapi.org/v2/top-headlines?q={search_query}&apiKey={API_KEY})
```
-  With the API key the news are retrieved.

### General news
This variable stores the URL for the Top News API endpoint, which returns the top headlines from the United Kingdom. It includes the API key as a parameter for authentication.
``` python
https://newsapi.org/v2/top-headlines?country=gb&apiKey={API_KEY}
```
- The headlines can be retrieved about any topic, you just need to change the query.

### Plot of
Uses [omdb.com ](https://www.omdbapi.com/)
-API is used to retrieve plots of movies.
```python
https://www.omdbapi.com/?t={search_query}&plot=full&apiKey={API_KEY}
```

## Streamlit Interface
The code utilizes the streamlit library to create a simple web interface. The user can start the program by clicking on a button labeled "Run Alexa." The program listens for voice commands and communicates its response to the user using the Text_to_speech function. The web interface also includes a caption reminding the user how to terminate the program and a spinning icon to indicate that the program is listening for voice input.

<br>

# Connecting a Language Model
In this section we offer 2 solutions to connect a language model to our chatbot. The first one is to use [Vicuna](https://vicuna.lmsys.org/), an Open-Source Chatbot Impressing GPT-4 with 90% ChatGPT Quality. The second one is to connect any other language model such as Bard, ChatGPT, etc.. by following the steps [here](#)

## Runing Vicuna Locally

- First of all, to run Vicuna, you need to have Vicuna. [Read the repo](https://github.com/IERoboticsClub/Vicuna)

- If you don't have Vicuna model, you could connect any other language model such as GPT-2, GPT-3, etc.. by following the steps [here](#)

- To run Vicuna we have a FastAPI Application which allows us to connect to our large language model.

- We used a macboook pro 64GB M1 chip to run both 7B and 13B Vicuna models, and it was running smoothly.

- To serve using the web UI, you need three main components: streamlit web UI, model worker that hosts Vicuna, and a controller to coordinate the UI with the model worker. Here are the commands to follow in your terminal:

Steps:
### 1. Launch the controller
```bash
python3 -m fastchat.serve.controller
```
- This yields an application startup on port 21001, to which you can start making requests.

### 2. Launch the model worker
```bash
python3 -m fastchat.serve.model_worker --model-path /path/to/vicuna/weights
```

> ```bash
> python3 -m fastchat.serve.model_worker --model-path vicuna_13B --device mps
> ```


At this point, you will have an endpoint open to access vicuna through payloads (message prompts) and get responses. 

### <u>Vicuna Troubleshooting</u>

PORTS ISSUES 
The ports you will be using are 7860, and 21001, 21002, 7860

If you get an error with any of the ports run the following scripts in your terminal: 

*Find the PID process of the PORT being used*
```sh 
sudo lsof -i :<port>
```
*kill PID* [CULTURE](https://www.youtube.com/watch?v=IuGjtlsKo4s)
```sh 
kill -9 <PID>
```
Example: 

```sh
 sudo lsof -i :21002
```

Output: 
```sh
COMMAND     PID           USER   FD   TYPE             DEVICE SIZE/OFF NODE 
Google      673 ieroboticsclub   31u  IPv6 0x7fe8b004caaac511      0t0  TCP 
Python     3506 ieroboticsclub   14u  IPv6 0x7fe8b004caacaa91      0t0  TCP 
````
Kill:
```sh
kill -9 673 3506
```
Any other issues,  please refer to the [Vicuna Documentation](https://github.com/lm-sys/FastChat)

## Connect any other language model

The connection to the GPT models family can be made through the streamlit app. Bard integration if future work so feel free to make a PR on it :)

<br>

# Presenters
- Nicholas Dieke
- Adnan Bhanji
- [Vera Prohaska](https://github.com/vtwoptwo)
- [Diego Sanmartin](https://github.com/dsanmart)
