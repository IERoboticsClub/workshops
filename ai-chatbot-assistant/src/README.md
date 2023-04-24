#  AI - Chatbot Assistant Robotics Club



<div style="text-align:center"><img src="https://img.freepik.com/free-vector/flat-woman-chatting-with-chatbot-communicating-ai-robot-assistant_88138-959.jpg?w=1380&t=st=1680905997~exp=1680906597~hmac=2aa93663bfc4191fe606f4e0342d0aa3dda0292e276236cf084b0c29c16b5c8e" width="" height="180" /></div>

<br>

## Chatbots 💬 

Imagine having a digital assistant that can chat with you like a real person, providing you with instant and relevant information whenever you need it. That's the power of a chatbot AI assistant! It's a cutting-edge tool that can engage with users in real-time through a messaging interface, making it an ideal solution for businesses and organizations looking to improve customer service and support.


## Understanding the Components



- We have an FastAPI Application which allows us to connect to our large language model.

- First we establish a connection to the controller (for our API)
    - `python3 -m fastchat.serve.controller`
    This yields an application startup on port 21001, to which you can start making requests.

    For example: by running `python3 -m fastchat.serve.model_worker --model-path vicuna_13B --device mps`

    ```sh
    2023-04-22 09:43:33 | INFO | controller | Register a new worker: http://localhost:21002
    2023-04-22 09:43:33 | INFO | controller | Register done: http://localhost:21002, {'model_names': ['vicuna_13B'], 'speed': 1, 'queue_length': 0}
    2023-04-22 09:43:33 | INFO | stdout | INFO:     ::1:63551 - "POST /register_worker HTTP/1.1" 200 OK
    ```
    Take note of the following parameters:

    - host='localhost'
    - port=21002 
    - worker_address='http://localhost:21002'
    - controller_address='http://localhost:21001'
    - model_path='vicuna_13B'



# Troubleshooting 

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



# Presenters
