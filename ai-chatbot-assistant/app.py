import streamlit as st
from PIL import Image
import numpy as np
import os
from utils.redis_helpers import connect_redis, reformat_redis, upload_to_redis, create_query_context
from utils.ocr import ocr_files, get_db_schema


st.set_page_config(
    page_title="JarvIEs",
    page_icon=":heart:"
)

# Title
col1, col2, col3 = st.columns([4, 1, 1])
col1.header("JarvIEs - AI Chatbot Assistant")
col2.image(Image.open("./assets/robotics.jpg"))
col3.image(Image.open("./assets/gdsc.png"))

embeddings_preference = st.selectbox("Choose your embeddings preference", ["speed", "quality", "more_speed"])
redis_conn = connect_redis()

chat_tab, data_tab = st.tabs(["Chat", "Data"])

with chat_tab:
    st.header("Chat")
    user_query = st.text_area('Chat with JarvIEs', '')
    if st.button("Submit"):
        answer = create_query_context(redis_conn, user_query, embeddings_preference)
        st.write(answer)

with data_tab:
    st.header("Upload your documents data to JarvIEs")
    files = st.file_uploader("Upload & process your data", type=["pdf"], accept_multiple_files=True)
    # Save files to temp folder
    tempDir = "tempDir"


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
                print("Successfully processed")
                print("Uploading data to Redis")
                for key, value in db_schema.items():
                    upload_to_redis(
                        value[0], 
                        value[1],
                        value[2],
                        value[3],
                        value[4],
                        redis_conn)
                print("Index size: ", redis_conn.ft().info()['num_docs'])
                st.write("Successfully uploaded data to Redis")
                # Delete files from temp folder
        else:
            st.write("No files uploaded!")
    if right.button("Restart Redis"):
        st.write("Formatting Redis")
        reformat_redis(redis_conn, embeddings_preference)
        st.write("Successfully formatted Redis")