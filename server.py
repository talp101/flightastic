import sys
import json
import requests
from flask import Flask, jsonify, request
from flightastic.flightatstic_search import FlightasticSearch

VERIFY_TOKEN = 'EAALRGUp9UBsBAKGXNOmu8yZCLihG92whrIu6ALq3edWz4ZAZC8LVKM8w97ZBYbBjPyvK6v8jxD0vlsAdqCZBLrbZBdIOxjsoqSH361bP4qDmVDAwLToMsErWGm4zqqZB2oTLVw32xpCz8zi25KxzzkfUGQdciQNRtZBvSn92eo0GdgZDZD'

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return jsonify({'success':True})

@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    log(sender_id)
                    send_message(sender_id, message_text)
    return "ok", 200

@app.route('/search_flight', methods=['POST'])
def search_flight():
    data = request.get_json()
    search = FlightasticSearch(originplace=data['originplace'],
                 destinationplace=data['destinationplace'],
                 outbounddate=data['outbounddate'],
                 inbounddate=data['inbounddate'],
                 stops=data['stops'],
                 adults=data['adults'])
    minimal_result = search.get_minimal_flight()
    flight_price = minimal_result['PricingOptions'][0]['Price']
    found_legit_flight = flight_price < data['max_price']
    response = jsonify({'found': found_legit_flight, 'minimal_price': flight_price})
    if found_legit_flight:
        full_purcashe_url = minimal_result['PricingOptions'][0]['DeeplinkUrl']
        short_url = requests.post("https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyDojzxFaQMBKigpppEUBMe6nr8hBxB8Fi8", data={"longUrl": full_purcashe_url}).json()['id']
        message_text =  short_url+ '\n' +  unicode(flight_price)
        send_message(data['fb_id'], message_text)
    return response

def send_message(recipient_id, message_text):
    params = {
        "access_token": VERIFY_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r =requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
    

def log(message):  # simple wrapper for logging to stdout on heroku
    print message
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
