import json
import requests


def clear_history(controller_addr):
    requests.post(controller_addr + "/refresh_all_workers")
    print("History cleared")


def query(prompt, model_name, max_new_tokens, temperature, worker_addr):
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
