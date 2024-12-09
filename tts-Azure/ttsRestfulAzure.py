import requests

"""
This script is a simple example of how to use the Azure Text to Speech API
It requires a subscription key from Azure, which can be obtained from the Azure Portal
Without 3rd party libraries, it uses the requests library to make the API calls.
"""

## TODO: Add more voice choices and languages

def get_token(subscription_key):
    try:
        url = 'https://westeurope.api.cognitive.microsoft.com/sts/v1.0/issueToken'
        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, headers=headers)
        return response.text
    except Exception as e:
        print(f"Error getting token: {e}")
        return None

def azure_tts(text, key):
    """
    :param text: The text to be converted to speech
    :param key: The access token from get_token
    :return: Binary Data of the audio file, convert to .wav
    """
    try:
        url = 'https://westeurope.tts.speech.microsoft.com/cognitiveservices/v1'
        headers = {
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'Content-Type': 'application/ssml+xml',
            'Authorization': f'Bearer {key}',
            'User-Agent': 'ttsRestfulAzure'
        }
        body = f"<speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Female' name='en-US-GuyNeural'>{text} </voice></speak>"
        response = requests.post(url, headers=headers, data=body)
        if response.status_code == 200:
            raise Exception(f"Non 200 response: {response.text}")
        return response
    except Exception as e:
        print(f"Error in azure_tts: {e}")
        return None

def save_audio(response, filename):
    try:
        if not response:
            raise Exception("No response to save")
        with open(filename, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(f"Error saving audio: {e}")
# def main():
#     subscription_key = 'YOUR_SUBSCRIPTION_KEY'
#     text = 'Hello, this is a test of the Azure Text to Speech API'
#     token = get_token(subscription_key)
#     response = azure_tts(text, token)
#     save_audio(response, 'output.wav')