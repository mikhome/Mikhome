import os
import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    prenom = request.form.get("prenom", "")
    nom = request.form.get("nom", "")
    email = request.form.get("email", "")
    message = request.form.get("message", "")

    headers = {
        "accept": "application/json",
        "api-key": os.environ["BREVO_API_KEY"],
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "name": "MikHome",
            "email": "contact@mikhome.fr"
        },
        "to": [
            {
                "email": "contact@mikhome.fr"
            }
        ],
        "replyTo": {
            "email": email
        },
        "subject": "Nouvelle demande de devis - MikHome",
        "textContent": f"""
Nouvelle demande depuis le site MikHome.

Prénom : {prenom}
Nom : {nom}
Email : {email}

Message :

{message}
"""
    }

    try:
        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers=headers,
            json=payload,
            timeout=15
        )
        print(response.status_code)
        print(response.text)
        response.raise_for_status()
    except Exception as e:
        print("ERREUR BREVO :", repr(e))
        raise

    return redirect("/#contact")

if __name__ == "__main__":
    app.run(debug=True)
