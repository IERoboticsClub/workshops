# environments

env-mac-chatbot: 
	python3 -m pip install --upgrade pip
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip install -r ai-chatbot-assistant/requirements.txt

env-win-chatbot:
	python -m pip install --upgrade pip
	python -m venv venv &
	. venv\Scripts\activate &
	pip install -r ai-chatbot-assistant/requirements.txt

env-lin-chatbot:
	python3 -m pip install --upgrade pip
	python3 -m venv venv &&
	. venv/bin/activate &&
	pip install -r ai-chatbot-assistant/requirements.txt

activate: 
	. venv/bin/activate

clean: 
	rm -rf venv

# Path: ai-chatbot-assistant

run-chatbot: 
	streamlit run ai-chatbot-assistant/Home.py