import urllib
from builtins import Exception, str

import vk_api
import time
import json
import requests

token = ""

vk = vk_api.VkApi(token=token)
vk._auth_token()

api_endpoint = 'https://api.wit.ai/speech'
wit_access_token = ''


def ReadAudio(AUDIO_FILE):
    with open(AUDIO_FILE, 'rb') as f:
        audio = f.read()
        return audio


def RecognizeSpeech(AUDIO_FILE, num_seconds=5):
    audio = ReadAudio(AUDIO_FILE)
    headers = {
        'Accept': 'audio/x-mpeg-3',
        'authorization': 'Bearer ' + wit_access_token,
        'Content-Type': 'audio/mpeg3'}
    resp = requests.post(api_endpoint, headers=headers, data=audio)
    data = json.loads(resp.content)
    text = data['_text']
    return text


if __name__ == '__main__':
    while True:
        try:
            messages = vk.method("messages.getConversations", {"offset": 0, "count": 200, "filter": "all"})
            if messages['count'] >= 1:
                id = messages['items'][0]['last_message']['from_id']
                try:
                    try:
                        audio_msg = messages["items"][0]["last_message"]["attachments"][0]["audio_message"]["link_mp3"]
                    except:
                        audio_msg = messages["items"][0]["last_message"]["fwd_messages"][0]["attachments"][0]["audio_message"]["link_mp3"]
                    vk.method('messages.setActivity', {"user_id": id, 'type': 'typing'})
                    audio = urllib.request.urlretrieve(audio_msg, 'mp.mp3')
                    text = RecognizeSpeech('mp.mp3', 4)
                    if text != '':
                        vk.method("messages.send", {"peer_id": id, "message": str(text)})
                    else:
                        vk.method("messages.send", {"peer_id": id, "message": "Я не понял тебя!"})
                        continue
                except Exception as Error:
                    vk.method("messages.send", {"peer_id": id, "message": "Отправь голосовое сообщение!"})
        except Exception as error:
            time.sleep(1)
