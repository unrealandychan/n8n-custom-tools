import requests

"""
This script is a simple example of how to use the Azure Text to Speech API
It requires a subscription key from Azure, which can be obtained from the Azure Portal
Without 3rd party libraries, it uses the requests library to make the API calls.
"""

def get_token(subscription_key):
    url = 'https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issueToken'
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, headers=headers)
    return response.text

def azure_tts(text, key):
    """
    :param text: The text to be converted to speech
    :param key: The access token from get_token
    :return: Binary Data of the audio file, convert to .wav
    """
    url = 'https://westeurope.tts.speech.microsoft.com/cognitiveservices/v1'
    headers = {
        'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
        'Content-Type': 'application/ssml+xml',
        'Authorization': f'Bearer {key}',
        'User-Agent': 'ttsRestfulAzure'
    }
    body = f"<speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Female' name='en-US-GuyNeural'>{text} </voice></speak>"
    response = requests.post(url, headers=headers, data=body)
    return response

def save_audio(response, filename):
    with open(filename, 'wb') as f:
        f.write(response.content)

def main():
    subscription_key = 'YOUR_SUBSCRIPTION_KEY'
    text = 'Hello, this is a test of the Azure Text to Speech API'
    token = get_token(subscription_key)
    response = azure_tts(text, token)
    save_audio(response, 'output.wav')