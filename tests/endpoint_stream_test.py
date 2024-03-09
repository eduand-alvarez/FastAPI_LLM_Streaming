import requests

# Sending the query in the get request parameter

query = "Once upon a time, there existed a fisherman at sea,"
#chat_model = 'Intel/neural-chat-7b-v3-3'
chat_model = 'Intel/neural-chat-7b-v1-1'

url = "http://localhost:5004/query-stream/"
params = {"query": query,"selected_model":chat_model}

with requests.get(url, json = params, stream=True) as r:
    for chunk in r.iter_content(1024):
        print(chunk)