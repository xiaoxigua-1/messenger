import json

from flask import Flask, request
import requests
__author__ = 'enginebai'

API_ROOT = '/api/'
FB_WEBHOOK = 'fb_webhook'

app = Flask(__name__)

token="EAALmiEjZACRoBANJKNvGZChZC3W8ove86iaNEeMiAnIz1hciEpX2arFNbDPuZAJ1ggUlWGPsYPoCCVaTasDOLslPs6KH4vxhJ6feIHST2BOEmhqE1RMhGE1ZBIZBRJtvICCD64fSfkxHIy9hyznuX2oHRK0JqHkmnS7vYinNRJU44fpmafNRjJ"

@app.route(API_ROOT + FB_WEBHOOK, methods=["GET"])
def fb_webhook():
    verification_code = token
    verify_token = request.args.get('hub.verify_token')
    if verification_code == verify_token:
        return request.args.get('hub.challenge')


@app.route(API_ROOT + FB_WEBHOOK, methods=['POST'])
def fb_receive_message():
    message_entries = json.loads(request.data.decode('utf8'))['entry']
    for entry in message_entries:
        for message in entry['messaging']:
            if message.get('message'):
                print("{sender[id]} says {message[text]}".format(**message))
                send_fb_message(to=int(message_entries["entry"]["messaging"][0]["sender"]["id"]), message="Hello, I'm enginebai.")
    return "Hi"
def send_fb_message(to, message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={token}'.format(token=token)
    response_message = json.dumps({"recipient":{"id": to}, 
                                   "message":{"text":message}})
    req = requests.post(post_message_url, 
                        headers={"Content-Type": "application/json"}, 
                        data=response_message)
    print("[{}] Reply to {}: {}", req.status_code, to, message)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
