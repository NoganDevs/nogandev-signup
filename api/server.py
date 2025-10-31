import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# 🔹 Quick test route
@app.route("/api/test", methods=["GET"])
def test_route():
    response = jsonify({"status": "ok", "message": "Python server is responding!"})
    response.headers["Access-Control-Allow-Origin"] = "*"  # allow all origins
    return response

# Environment variables
EMAIL_USER = os.environ.get("NOGANDEV_EMAIL")
EMAIL_PASS = os.environ.get("NOGANDEV_KEY")  # your app password / API key
TO_EMAIL = os.environ.get("TO_EMAIL")        # where the message should go

# 🔹 Main message route
@app.route("/api/server", methods=["POST", "OPTIONS"])
def receive_message():
    # Handle preflight CORS request
    if request.method == "OPTIONS":
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    # Parse JSON
    data = request.get_json()
    if not data or "email" not in data or "name" not in data or "message" not in data:
        response = jsonify({"error": "Missing required fields"})
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response, 400

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

        response = jsonify({"status": "success", "message": "Email sent successfully!"})
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response
    except Exception as e:
        response = jsonify({"status": "error", "message": str(e)})
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response, 500

# ⚠️ Only for local testing
if __name__ == "__main__":
    app.run(debug=True)
