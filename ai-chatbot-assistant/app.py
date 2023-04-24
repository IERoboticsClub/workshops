import streamlit as st
from PIL import Image
import os
import openai
from utils.redis_helpers import connect_redis, reformat_redis, upload_to_redis, create_query_context
from utils.vicuna_helpers import clear_history, query, get_http_response_text, extract_answer
from utils.ocr import ocr_files, get_db_schema
from streamlit_chat import message

# ------ PAGE CONFIG ------
st.set_page_config(
    page_title="JarvIEs",
    page_icon=":heart:"
)


# ------ CONSTANTS ------
redis_conn = connect_redis()
controller_addr = "http://localhost:21001"
worker_addr = "http://localhost:21002"
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []


# ------ SIDEBAR ------
with st.sidebar:
    embeddings_preference = st.selectbox("Choose your embeddings preference", ["speed", "more_speed", "quality"], index=0)
    model_select = st.radio(
        "Select the model you want to use",
        ('Vicuna', 'GPT', 'Bard'))
    if model_select == 'Vicuna':
        st.write("# Vicuna Model Parameters")
        model_name = st.selectbox("Model Name", ["vicuna_7B", "vicuna_13B"], index=1)
        device = st.selectbox("Device", ["cpu", "cuda", "mps"], index=2)
        num_gpus = st.selectbox("Number of GPUs", ["0", "1", "2", "3"], index=1)
        max_gpu_memory = st.selectbox("Max GPU Memory", ["4GiB", "8GiB", "12GiB", "13GiB"], index=3)
        load_8bit = st.checkbox("Load 8-bit", value=False)
        max_new_tokens = st.number_input("Max New Tokens", value=512, step=128)
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    elif model_select == 'GPT':
        openai.api_key = st.text_input("OpenAI API Key", "")
        openai.api_base = st.text_input("OpenAI API Base", "")
        openai.api_type = st.text_input("OpenAI API Type", "")
        openai.api_version = st.text_input("OpenAI API Version", "2022-12-01")
        st.write("# GPT Model Parameters")
        gpt_engine = st.selectbox("Model Name",
            ["gpt-4", "gpt-3.5-turbo", "davinci", "curie", "babbage", "ada"], index=1)
        max_tokens = st.number_input("Max Tokens", value=500, step=100)
        temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=1.0, step=0.1)
        presence_penalty = st.slider("Presence Penalty", min_value=-2.0, max_value=2.0, value=0.0, step=0.1)
        frequency_penalty = st.slider("Frequency Penalty", min_value=-2.0, max_value=2.0, value=0.0, step=0.1)

    elif model_select == 'Bard':
        st.write("WIP!!")


# ------ MAIN PAGE ------
col1, col2, col3 = st.columns([4, 1, 1])
col1.header("JarvIEs - Your AI Virtual Assistant")
col2.image(Image.open("./assets/robotics.jpg"))
col3.image(Image.open("./assets/gdsc.png"))

chat_tab, data_tab = st.tabs(["Chat", "Data"])

with chat_tab:
    st.header("Chat")
    user_query = st.text_area('Chat with JarvIEs', '')
    left, right = st.columns([3,1])
    
    if right.button("Clear Chat History", key="clear"):
        if model_select == 'Vicuna':
            try:
                clear_history()
            except:
                st.warning("Error: Please check the connection with the Vicuna server!")
        st.session_state['generated'] = []
        st.session_state['past'] = []
    if left.button("Submit"):
        try:
            assistant_prompt = create_query_context(redis_conn, user_query, embeddings_preference)
        except:
            st.warning("Error loading your data: Please check the connection with Redis")
            assistant_prompt = user_query
        with st.expander("See generated prompt"):
            st.text(assistant_prompt)
        if model_select == 'Vicuna':
            try:
                res = query(assistant_prompt, model_name, max_new_tokens, temperature, worker_addr)
                if res:
                    res = get_http_response_text(res)
                    last_set = res.split("}")[-2] + "}"
                    output = extract_answer(str(last_set))
                else:
                    output = "Sorry, I didn't get that. Please try again!"
            except:
                st.warning("Error: Please check the connection with the Vicuna server!")
                output = "None"
        elif model_select == 'GPT':            
            try:
                response = openai.Completion.create(
                    engine=gpt_engine,
                    prompt=assistant_prompt,
                    max_tokens=max_new_tokens,
                    temperature=temperature,
                    presence_penalty=presence_penalty,
                    frequency_penalty=frequency_penalty
                )
                output = response.choices[0].text
            except:
                st.warning("Error with the OpenAI API!")
                output = "None"
        elif model_select == 'Bard':
            st.image(Image.open("./assets/wip.jpg"), use_column_width=True)
            output = "None"
        st.session_state.past.append(user_query)
        if output != "None":
            st.session_state.generated.append(output)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

with data_tab:
    st.header("Upload your documents data to JarvIEs")
    files = st.file_uploader("Upload & process your data", type=["pdf"], accept_multiple_files=True)

    tempDir = "tempDir" # TBD - Delete tempDir after processing

    left, right = st.columns([4,1])
    if left.button("Process data"):        
        if files is not None:
            file_names = []    
            dfs = []
            print(files)
            for file in files:
                st.write(file)
                # Open and save file to temp folder
                with open(os.path.join(tempDir, file.name), "wb") as f:
                    f.write(file.getbuffer())
                
                st.write("Processing data")
                sentences = ocr_files(tempDir)
                db_schema = get_db_schema(sentences, embeddings_preference)
                #print("Successfully processed")
                #print("Uploading data to Redis")
                for key, value in db_schema.items():
                    upload_to_redis(
                        value[0], 
                        value[1],
                        value[2],
                        value[3],
                        value[4],
                        redis_conn)
                print("Index size: ", redis_conn.ft().info()['num_docs'])
            st.write("Successfully uploaded data to your Redis database")    
        else:
            st.write("No files uploaded!")
    if right.button("Restart Redis"):
        try:
            redis_conn = connect_redis()
            reformat_redis(redis_conn, embeddings_preference)
            st.write("Successfully formatted Redis")
        except:
            st.error("RedisError: Please check the connection with the Redis server!")
