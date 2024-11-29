from slack_bolt import App
import os
from dotenv import load_dotenv
import requests

load_dotenv()
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")

)
def translate(msg):
    url = "https://pirater-api.onrender.com/translate/"
    data = {"text": f"${msg}"}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return(response.json()["pirate_translation"])
    else:
        print("thar be a error in translating; ", response.status_code, response.text)
        return("thar be a error in translating; ", response.status_code, response.text)

@app.command("/pirate")
def slashpirate(ack, body, client):
    ack()
    usermessage = body.get("text","")
    userid = body.get("user_id")
    
    try:
        response = client.users_info(user=userid)
        if response['ok']:
            user_info = response['user']
            displayname = user_info['profile'].get('display_name')
            pfp = user_info['profile'].get('image_192')
        else:
            print("errr fetching user info ", response['error'])
    
    except Exception as e:
        print("error fetching userinfo:", e)
    
    channelid = body.get("channel_id")
    pirate_message = translate(usermessage)
    client.chat_postMessage(
        channel=channelid,
        username=displayname,
        text=pirate_message,
        icon_url=pfp
    )