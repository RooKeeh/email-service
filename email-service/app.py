from flask import Flask, request, jsonify
import smtplib
import os

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({"message": "API is running"}), 200


@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    if not data or 'to' not in data or 'subject' not in data or 'message' not in data:
        return jsonify({"error": "Missing fields"}), 400

    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    smtp_server = "smtp.mailgun.org"

    try:
        with smtplib.SMTP(smtp_server, 465) as server:
            server.login(sender_email, sender_password)
            message = f"Subject: {data['subject']}\n\n{data['message']}"
            server.sendmail(sender_email, data['to'], message)

        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
