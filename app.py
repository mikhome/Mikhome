import os
import smtplib
from email.message import EmailMessage

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

    msg = EmailMessage()
    msg["Subject"] = "Nouvelle demande de devis - MikHome"
    msg["From"] = os.environ["SMTP_USER"]
    msg["To"] = os.environ["SMTP_USER"]
    msg["Reply-To"] = email

    msg.set_content(f"""
Nouvelle demande depuis le site MikHome.

Prénom : {prenom}
Nom : {nom}
Email : {email}

Message :
{message}
""")

    try:
        with smtplib.SMTP("smtp.mail.ovh.net", 587, timeout=15) as smtp:
            smtp.starttls()
            smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
            smtp.send_message(msg)
    except Exception as e:
        print("ERREUR SMTP :", repr(e))
        raise

    return redirect("/#contact")

if __name__ == "__main__":
    app.run(debug=True)
