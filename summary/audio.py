import requests
import os

endpoint = "https://api.assemblyai.com/v2/transcript"
json = {
    "audio_url": "",
    "auto_chapters": True
    "auto_highlights": True
}
headers = {
    "authorization": os.getenv("ASSEMBLYAI_API_KEY")),
    "content-type": "application/json"
}
response = requests.post(endpoint, json=json, headers=headers)
print(response.json())