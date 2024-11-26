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
    return Response(), 200
    
if __name__ == "__main__":
    app.run(port=3000)
