<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

# AI - Music Album Generator 🎶

Welcome to the AI Music Album Generation Workshop! Here, we leverage the power of AI to conceptualize and create a unique music album from scratch.


## Objective
This workshop aims to demonstrate the use of AI to generate a conceptual music album, inclusive of album name, album art, and individual song titles, descriptions, and sounds.

The workshop will utilize three main models: 

- A textual generator (like [ChatGPT](https://openai.com/research/instruction-following)) using [prompt engineering](https://www.promptingguide.ai/).
- An image generator model (like [Stable Diffusion XL](https://huggingface.co/blog/sdxl_jax)).
- A sound & music generator model (like [AudioCraft](https://ai.meta.com/blog/audiocraft-musicgen-audiogen-encodec-generative-ai-audio/)).


## Workflow

1. **Album Concept Generation**:
   - Utilize a Large Language Model (LLM) to produce an album concept.
   - This will include the album's name, a description for the artwork, and details for six individual songs.

2. **Album Art Creation**:
   - With the generated description, use an image generation AI model to create the album cover.

3. **Music Creation**:
   - Generate six distinct songs based on the provided song names and descriptions using a music generator AI model.


## Run the User Interface Locally in your computer

#### 1. Upgrade your `pip` (installer interface for python packages)

```bash
python3 -m pip install --upgrade pip
```

#### 2. Create & activate a virtual environment
```bash
python3 -m venv venv && source venv/bin/activate
```

#### 3. Install the dependencies
```bash
pip install -r ai-music-album/requirements.txt
```

#### 4. Run the application
```bash
streamlit run ai-music-album/app.py
```

## Run Music Generation (AudioCraft) Locally in your computer
Follow the instructions in the official [AudioCraft MusicGen Repository](https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md) to run the Gradio interface or the python notebook locally in your computer.

Enjoy your unique AI-generated music album! 🎶



<!-- MARKDOWN LINKS & IMAGES [![Name][Shield]][url] -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/IERoboticsClub/workshops.svg?style=for-the-badge
[contributors-url]: https://github.com/IERoboticsClub/workshops/graphs/contributors 
[forks-shield]: https://img.shields.io/github/forks/IERoboticsClub/workshops.svg?style=for-the-badge
[forks-url]: https://github.com/IERoboticsClub/workshops/network/members
[stars-shield]: https://img.shields.io/github/stars/IERoboticsClub/workshops.svg?style=for-the-badge
[stars-url]: https://github.com/IERoboticsClub/workshops/stargazers
[issues-shield]: https://img.shields.io/github/issues/IERoboticsClub/workshops.svg?style=for-the-badge
[issues-url]: https://github.com/IERoboticsClub/workshops/issues
[license-shield]: https://img.shields.io/github/license/IERoboticsClub/workshops.svg?style=for-the-badge
[license-url]: https://github.com/IERoboticsClub/workshops/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/company/ie-robotics-club/