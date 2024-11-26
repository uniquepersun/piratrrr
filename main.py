from slack_sdk import WebClient
from flask import Request, Flask, jsonify, Response, request
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

@app.route('/pirate', methods=['POST'])
def slash():
    data = request.form
    print(data) # TODO: remove this print later!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    userid = data.get('user_id')
    message = data.get('text')
    channelid = data.get('channel_id')
    threadts = data.get('thread_ts')
    userinfo = client.users_info(user=userid)
    realname = userinfo['user']['real_name']
    username = data.get('user_name')
    userpicture = userinfo['user']['profile']['image_192']
    translatedmessage = translate(message)
    message = f"{username}({realname}) says: {translatedmessage}"

    try:
        client.chat_postMessage(
            channel=channelid,
            text=message,
            thread_ts=threadts
        )

    except SlackApiError as e:
        print(f"ERROR:{e.response['error']}")

    return Response(), 200
    
if __name__ == "__main__":
    app.run(port=3000)
