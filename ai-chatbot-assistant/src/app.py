import streamlit as st
from streamlit_chat import message
import requests
import json


st.set_page_config(
    page_title="JarvIEs",
    page_icon=":heart:"
)

# set chatbot box 
st.header("Your IE Virtual Assistant")

controller_addr = "http://localhost:21001"
worker_addr = "http://localhost:21002"
worker_id = ""
no_register = ""
model_name = "vicuna_13B"
device = "mps"
num_gpus = "1"
max_gpu_memory = "13GiB"
load_8bit=False
max_new_tokens =512
temperature = 0.7

with st.sidebar:
    st.write("# Model Parameters")
    model_name = st.text_input("Model Name", model_name)
    device = st.selectbox("Device", ["cpu", "cuda", "mps"], index=2 if device == "mps" else 1)
    num_gpus = st.selectbox("Number of GPUs", ["0", "1", "2", "3"], index=int(num_gpus))
    max_gpu_memory = st.selectbox("Max GPU Memory", ["4GiB", "8GiB", "12GiB", "13GiB"])
    load_8bit = st.checkbox("Load 8-bit", value=load_8bit)
    max_new_tokens = st.number_input("Max New Tokens", value=max_new_tokens, step=128)
    temperature = st.slider("Temperature", min_value=0.1, max_value=1.0, value=temperature, step=0.1)


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def clear_history():
    requests.post(controller_addr + "/refresh_all_workers")
    st.session_state['generated'] = []
    st.session_state['past'] = []
    print("History cleared")


def query(prompt):
    print(prompt)
    headers = {"User-Agent": "fastchat Client"}
    pload = {
        "model": model_name,
        "prompt": prompt,
        "max_new_tokens": max_new_tokens,
        "temperature": temperature,
        'stop': "</s>"
    }
    response = requests.post(
        worker_addr + "/worker_generate_stream",
        headers=headers,
        json=pload,
        stream=True,
        timeout=60
    )
    print('Response', response)
    return response

def get_http_response_text(response):
    # Get the raw response data as a string
    response_text = response.text
    # save the response text to a file 

    # Check if the response is JSON
    content_type = response.headers.get("content-type")
    if content_type and "application/json" in content_type:
        # If it's JSON, parse the JSON and get the text
        try:
            # using unicode to avoid ascii errors
            json_object = json.loads(response_text.encode('utf-8').decode('unicode_escape'))
            if isinstance(json_object, dict) and "text" in json_object:
                return json_object["text"]
        except json.JSONDecodeError:
            pass

    # If it's not JSON, assume it's plain text and return the response text
    return response_text.split("extra_data=")[0]

def extract_answer(source_data):
    source_data = str(source_data)
    start = source_data.find("Answer: ") + len("Answer: ")
    end = min([source_data.find(".", start)])
    answer = source_data[start:end].strip()
    return answer

def extract_question(source_data):
    source_data = str(source_data)
    start = source_data.find("Question: ") + len("Question: ")
    end = min([source_data.find("?", start)])
    question = source_data[start:end].strip()
    return question + "?"

def get_text():
    input_text = st.text_input("You: ","Hello, how are you?",  key="input")
    return input_text

user_input = get_text()

send = st.button("Send", key="send")
clear = st.button("Clear History", key="clear")
if clear:
    clear_history()

if send:
    res = query(user_input)
    if res: 

        res = get_http_response_text(res)
        last_set = res.split("}")[-2] + "}"
        output = extract_answer(str(last_set))
        
    else:
        output = "Sorry, I didn't get that. Please try again!"

    st.session_state.past.append(extract_question(str(user_input)))
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')