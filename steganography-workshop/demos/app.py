import streamlit as st
from PIL import Image
from stegano_model.model_utils import load_model, inference_encoder, inference_decoder
import numpy as np


col1, col2 = st.columns([4, 1])
col1.title("Steganography Workshop")

col2.image(Image.open("./data/roboticslogo.jpg"))

PRETRAINED_MODEL = f"./data/models/pretrained_model.pt"
PRETRAINED_MODEL_2 = f"./data/models/pretrained_model_2.pt"
SIZE_IMAGE = 64
model_pretrained = load_model(PRETRAINED_MODEL)
model_pretrained_2 = load_model(PRETRAINED_MODEL_2)

option = st.selectbox(
    'Choose a pre-trained model',
    ('1', '2'))

st.header("Encoder")
if option == '1':
    selected_model = PRETRAINED_MODEL
    model_pretrained = load_model(PRETRAINED_MODEL)
else:
    selected_model = PRETRAINED_MODEL_2
    model_pretrained = load_model(PRETRAINED_MODEL_2)

def encoded_predict(file_source, file_payload):
    _, encoded_image = inference_encoder(
        model_pretrained,
        file_source,
        file_payload,
        device="cpu",
    )
    return encoded_image

def decode_predict(file_encoded):
    _, decoded_image = inference_decoder(
        model_pretrained,
        file_encoded,
        device="cpu",
    )
    return decoded_image


input_image = st.file_uploader("Upload an Image")
payload = st.file_uploader("Upload Payload")


if st.button("Compute 🔥"):
    # Encode and save the image in results directory
    encoding = encoded_predict(input_image, payload)


st.header("Decoder")
secret_image = st.file_uploader("Upload encoded tiff image")
if st.button("Reveal 🔎"):
    decoding = decode_predict(secret_image)
    if decoding is not None:
        input_image = Image.open("results/image_decoded_result.png")
        st.image(input_image, caption='Revealed secret')


st.subheader("Model Architecture")
st.image(Image.open("./data/architecture.jpg"))
left, right = st.columns([3,2])
right.caption("Source: https://arxiv.org/pdf/1711.07201.pdf")