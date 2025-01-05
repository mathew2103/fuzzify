import requests

def alt_ipa(name):
    url = "http://172.30.48.1:1234/v1/chat/completions"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json; charset=utf-8",
        "Accept-Charset": "utf-8"
    }
    data = {
        "model": "ipafuzzylamav4",
        "messages": [
            # {"role": "system", "content": si},
            {"role": "user", "content": name}
        ],
        # "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }
    
    response = requests.post(
        url, 
        json=data,  # requests automatically handles UTF-8 encoding
        headers=headers,
        verify=True
    )
    response.encoding = 'utf-8'  # force UTF-8 encoding for response
    response.raise_for_status()        
    response_data = response.json()
    return [response_data['choices'][0]['message']['content']]