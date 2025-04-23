# my-venv/bin/pip install package-name
from flask import Flask, render_template, abort, request, redirect, session, url_for
import os
import requests
import smtplib
from email.message import EmailMessage
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

@app.route('/papers/')
def papers():
    return render_template('papers.html')

@app.route('/papers/<path:sub_path>')
def sub_papers(sub_path):
    return render_template('sub_papers.html', sub_path=sub_path)

@app.route('/simulations')
def simulations():
    return render_template('simulations.html')

@app.route('/data_science')
def data_science():
    return render_template('data_science.html')

@app.route('/lab_reports')
def lab_reports():
    return render_template('lab_reports.html')

@app.route('/electrical_engineering')
def electrical_engineering():
    return render_template('electrical_engineering.html')

def send_email(email, message):
    msg = EmailMessage()
    msg['Subject'] = "Website Message"
    msg['From'] = "evilscientist3111@gmail.com"
    msg['To'] = "corey.anderson311@gmail.com"
    msg.set_content("email: " + email + "\n" +
                    "message: " + message)

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(os.environ.get('EMAIL_USER'), os.environ.get('EMAIL_PASS'))
        server.send_message(msg)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        email = request.form["email"]
        message = request.form["message"]
        send_email(email, message)
        session["contact_message"] = "Thank you for your message!"
        return redirect(url_for("contact"))
    
    msg = session.pop("contact_message", None)
    return render_template("contact.html", contact_message=msg)

@app.context_processor
def inject_path():
    return dict(current_path=request.endpoint)

if __name__ == '__main__':
    app.run(debug=True) 