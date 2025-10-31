import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify

app = Flask(__name__)

# Get your secret key (email password or app key) from environment variables
EMAIL_USER = os.environ.get("NOGANDEV_EMAIL")
EMAIL_PASS = os.environ.get("NOGANDEV_KEY")  # your app password / API key
TO_EMAIL = os.environ.get("TO_EMAIL")        # where the message should go

@app.route("/api/server", methods=["POST"])
def receive_message():
    data = request.get_json()

    if not data or "email" not in data or "name" not in data or "message" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    sender_name = data["name"]
    sender_email = data["email"]
    message = data["message"]

    try:
        msg = MIMEText(f"Name: {sender_name}\nEmail: {sender_email}\n\nMessage:\n{message}")
        msg["Subject"] = f"New message from {sender_name}"
        msg["From"] = EMAIL_USER
        msg["To"] = TO_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, TO_EMAIL, msg.as_string())

        return jsonify({"status": "success", "message": "Email sent successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# for local testing
if __name__ == "__main__":
    app.run(debug=True)
