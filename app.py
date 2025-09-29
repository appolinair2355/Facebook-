from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "mon_token_secret"  # le même que sur Facebook Developer
PAGE_ACCESS_TOKEN = "EAAP89LecNCIBP..."  # <-- mets ton token ici

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Vérification du webhook
        token_sent = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token_sent == VERIFY_TOKEN:
            return challenge
        return "Invalid verification token"
    else:
        # Réception des messages
        data = request.get_json()
        if "entry" in data:
            for entry in data["entry"]:
                if "messaging" in entry:
                    for messaging_event in entry["messaging"]:
                        if "message" in messaging_event:
                            sender_id = messaging_event["sender"]["id"]
                            message_text = messaging_event["message"].get("text")
                            if message_text:
                                send_message(sender_id, f"Tu as dit: {message_text}")
        return "Message reçu", 200

def send_message(recipient_id, message_text):
    """Envoie un message via l'API Facebook Messenger"""
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post(url, params=params, json=data)

if __name__ == "__main__":
    # Render fournit automatiquement le PORT dans ses variables d'environnement
    port = int(os.environ.get("PORT", 10000))  # 10000 par défaut
    app.run(host="0.0.0.0", port=port)
