from flask import Flask, request, jsonify  # Flask pentru crearea API-ului
import smtplib  # Pentru trimiterea emailurilor
import os  # Pentru Envionment Variables

# Initializare aplicatie Flask
app = Flask(__name__)

# Endpoint principal pentru verificare functionare API


@app.route('/')
def home():
    return jsonify({"message": "API is running"}), 200


# Endpoint pentru trimiterea emailurilor prin Mailgun SMTP
@app.route('/send-email', methods=['POST'])
def send_email():
    # Preluare date din cererea POST (in format JSON)
    data = request.json

    # Verificare daca toate campurile necesare sunt prezente
    if not data or 'to' not in data or 'subject' not in data or 'message' not in data:
        return jsonify({"error": "Missing fields"}), 400

    # Citire date autentificare SMTP din variabile de mediu
    # Adresa de email (Credentiale de autentificare) pentru Mailgun
    sender_email = os.getenv("EMAIL_USER")
    # API Key (Parola) pentru Mailgun
    sender_password = os.getenv("EMAIL_PASS")

    smtp_server = "smtp.mailgun.org"  # Serverul SMTP Mailgun

    try:
        # Conectare securizata la serverul SMTP (pe portul 465)
        with smtplib.SMTP_SSL(smtp_server, 465) as server:
            server.login(sender_email, sender_password)  # Autentificare

            # Crearea mesajului
            message = f"Subject: {data['subject']}\n\n{data['message']}"

            # Trimiterea emailului
            server.sendmail(sender_email, data['to'], message)

        return jsonify({"message": "Email sent successfully"}), 200

    # In caz de eroare (ex: autentificare greșită, SMTP indisponibil)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Pornirea serverului Flask pe toate interfetele (necesar pentru Cloud Run)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
