import streamlit as st
from langchain.chat_models import AzureChatOpenAI
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
gpt_turbo = AzureChatOpenAI(deployment_name="gpt-turbo", temperature=0)


st.title("AI Music Album Generator")

st.write("This is a simple web app to generate music albums using AI.")

user_input = st.text_input("Enter the album you want to generate: ")

if user_input:
    with st.spinner("Generating album..."):
        prompt = f"""
        Instruction: You are an expert musician who has the capacity of following a user input to generate a music album definition for any genre. You will generate an album name, a detailed description of the album artistic cover, and the name and description of five songs (unless different number is stated by the user). Make sure to always follow the same format.

        ----
        Album 1:
        User input: Generate a classical piano album inspired in the modern style

        Answer:
        Album Name: Modern Resonance

        Album Cover Description: A sleek grand piano sits in the middle of an expansive white room, with floor-to-ceiling windows showcasing a bustling cityscape at dusk. The room's minimalistic design emphasizes the piano's silhouette. Shadows play on the floor, created by the soft interplay of the city lights and the setting sun. Above the piano, suspended in the air, is a delicate crystal chandelier, subtly reminiscent of musical notes, twinkling as it catches the last rays of the sun.

        Songs:
        1. Metropolitan Reverie
        Description: Steady rhythmic beats with flowing piano sequences, accented staccatos, and layered arpeggios.

        2. Twilight Sonata
        Description: Melodic piano intertwining of somber and bright notes, creating a dynamic contrast throughout the piece.

        3. Dance of the Digital Age
        Description: Fast-paced, whimsical piano tune with syncopated rhythms and rapid scales, capturing the essence of digital motion.
        
        4. Concrete Lullaby
        Description: Gentle and calm piano melodies with subtle underlying harmonies, painting a serene and tranquil soundscape.

        5. Skyscraper Nocturne
        Description: Dominant deep bass foundation with a soaring piano melodic line above, contrasting the grounded and the aspirational.
        
        ----
        Album 2:
        User input: {user_input}

        Answer:
        """
        with st.expander("Generated LLM prompt:"):
            st.write(prompt)

        gpt3_answer = gpt_turbo.predict(prompt)

        # Extract album name
        album_name_match = re.search(r"Album Name: (.*?)(?=Album Cover Description:)", gpt3_answer, re.DOTALL)
        album_name = album_name_match.group(1).strip()

        # Extract album description
        album_description_match = re.search(r"Album Cover Description: (.*?)(?=Songs:)", gpt3_answer, re.DOTALL)
        album_description = album_description_match.group(1).strip()

        # Extract songs and descriptions
        song_matches = re.findall(r"(\d+\..*?)(?=Description:)\s*Description: (.*?)(?=\d+\.|$)", gpt3_answer, re.DOTALL)
        songs = [{"name": match[0].strip(), "description": match[1].strip()} for match in song_matches]

    with st.expander("Generated LLM output:"):
        st.write(gpt3_answer)

    st.header(album_name)
    st.subheader("Cover Description:")
    st.write(album_description)
    st.header("Songs:")
    for song in songs:
        st.subheader(song["name"])
        st.write(song["description"])
        st.write("")