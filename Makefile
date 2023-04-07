venv: 
	python3 -m pip install --upgrade pip
	python3 -m venv .venv && \
	. .venv/bin/activate && \
	 pip install -r requirements.txt

activate: 
	. .venv/bin/activate

clean: 
	rm -rf .venv