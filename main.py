from flask import Flask, render_template, request, flash, redirect, url_for
import datetime
import ssl, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from flask_sqlalchemy import SQLAlchemy

year = datetime.datetime.today().year

app = Flask(__name__)

# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
app.config['SECRET_KEY'] = "Your secret key"
# app.config['SECRET_KEY'] = os.environ.get('secret_key')


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://flourishing_emails_user:y6SiCT8NeRTcENoawL8VbGVJVmhglMbE@dpg-ckjgr6j6fquc7398tg6g-a/flourishing_emails"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# os.environ.get("flourishing_db")
db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)


with app.app_context():
    db.create_all()

email = "hello@yourflourishlife.com"
password = "FloRich1!"
# password = os.environ.get("flourishemailpassword")
context = ssl.create_default_context()

msg = MIMEMultipart()
msg['Subject'] = "Welcome to the Flourish Rapidly Community."
body = """
Hello,
Thanks for subscribing to your flourish life newsletter. As a welcome gift, check out this free document.
"""

msg.attach(MIMEText(body, "plain"))

filename = "Social Media guidelines burgeon careers.pdf"
attachment = open("Social Media guidelines burgeon careers.pdf", "rb")

part = MIMEBase("application", "octet-stream")
part.set_payload(attachment.read())
encoders.encode_base64(part)

part.add_header("Content-Disposition", f"attachment; filename={filename}")
msg.attach(part)
host = "mail.privateemail.com"

text = msg.as_string()


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email_to_subscribe = request.form.get('email')
        if len(email_to_subscribe) > 0:
            email_to_add = User.query.filter_by(email=email_to_subscribe).first()
            if email_to_add:
                flash("You've already subscribed!")
                return redirect(url_for('home'))
            else:
                email_to_add = User(
                    email=email_to_subscribe
                )
                db.session.add(email_to_add)
                db.session.commit()
                with smtplib.SMTP_SSL(host, 465, context=context) as connection:
                    connection.ehlo()
                    connection.login(email, password)
                    connection.sendmail(
                        from_addr=email,
                        to_addrs=f"{email_to_subscribe}",
                        msg=text,
                    )
    return render_template("index.html", year=year)


@app.route("/about-me", methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        email_to_subscribe = request.form.get('email')
        if len(email_to_subscribe) > 0:
            email_to_add = User.query.filter_by(email=email_to_subscribe).first()
            if email_to_add:
                flash("You've already subscribed!")
                return redirect(url_for('home'))
            else:
                email_to_add = User(
                    email=email_to_subscribe
                )
                db.session.add(email_to_add)
                db.session.commit()
                with smtplib.SMTP_SSL(host, 465, context=context) as connection:
                    connection.ehlo()
                    connection.login(email, password)
                    connection.sendmail(
                        from_addr=email,
                        to_addrs=f"{email_to_subscribe}",
                        msg=text,
                    )
    return render_template('about.html', year=year)


@app.route("/courses", methods=['GET', 'POST'])
def courses():
    if request.method == 'POST':
        email_to_subscribe = request.form.get('email')
        if len(email_to_subscribe) > 0:
            email_to_add = User.query.filter_by(email=email_to_subscribe).first()
            if email_to_add:
                flash("You've already subscribed!")
                return redirect(url_for('home'))
            else:
                email_to_add = User(
                    email=email_to_subscribe
                )
                db.session.add(email_to_add)
                db.session.commit()
                with smtplib.SMTP_SSL(host, 465, context=context) as connection:
                    connection.ehlo()
                    connection.login(email, password)
                    connection.sendmail(
                        from_addr=email,
                        to_addrs=f"{email_to_subscribe}",
                        msg=text,
                    )
    return render_template('courses.html', year=year)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        contact_email = request.form.get("contact-email")
        if contact_email is not None:
            with smtplib.SMTP_SSL(host="mail.privateemail.com", port=465, context=context) as connection:
                connection.ehlo()
                connection.login(user=email, password=password)
                connection.sendmail(
                    from_addr=email,
                    to_addrs=email,
                    msg=f"Subject:Email from {request.form.get('name')}\n\n{request.form.get('name')}, {request.form.get('contact-email')}, sent you this message:"
                        f" {request.form.get('message')}"
                )
    if request.method == 'POST':
        email_to_subscribe = request.form.get('email')
        if email_to_subscribe is not None:
            email_to_add = User.query.filter_by(email=email_to_subscribe).first()
            if email_to_add:
                flash("You've already subscribed!")
                return redirect(url_for('home'))
            else:
                email_to_add = User(
                    email=email_to_subscribe
                )
                db.session.add(email_to_add)
                db.session.commit()
                with smtplib.SMTP_SSL(host, 465, context=context) as connection:
                    connection.ehlo()
                    connection.login(email, password)
                    connection.sendmail(
                        from_addr=email,
                        to_addrs=f"{email_to_subscribe}",
                        msg=text,
                    )
    return render_template("contact.html", year=year)


if __name__ == "__main__":
    app.run(debug=True,)
