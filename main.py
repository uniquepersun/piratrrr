from slack_sdk import WebClient
from flask import Flask, Response, request
import requests
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
slack_bot_token=os.environ.get("SLACK_BOT_TOKEN")
client = WebClient(slack_bot_token)

def translate(msg):
    url = "https://pirater-api.onrender.com/translate/"
    data = {"text": f"${msg}"}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return(response.json()["pirate_translation"])
    else:
        print("thar be a error in translating;", response.status_code, response.text)
        return("thar be a error in translating;", response.status_code, response.text)

@app.route('/pirate', methods=['POST'])
def slash(ack):
    ack()
    data = request.form
    userid = data.get('user_id')
    message = data.get('text')
    channelid = data.get('channel_id')
    userinfo = client.users_info(user=userid)
    userpictureurl = userinfo['user']['profile']['image_48']
    username = data.get('user_name')
    message = translate(message)

    try:
        client.chat_postMessage(
            channel=channelid,
            text=message,
            username=username,
            icon_url=userpictureurl

        )

    except SlackApiError as e:
        print(f"ERROR:{e.response['error']}")

    return Response(), 200
    
if __name__ == "__main__":
    app.run(port=3000)
