import smtplib
import datetime
import weather, local, california, national_world

from local import client
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail():
    from_Email = 'newsbotemailer@gmail.com'
    to_Email = 'myemail@gmail.com'
    password = 'mypassword'

    message = MIMEMultipart()
    message['Subject'] = "Good morning! Here is your news digest for today!"
    message['From'] = from_Email
    message['To'] = to_Email

    body = weather.w_news(), local.l_news(), california.c_news(), national_world.n_w_news()

    mime = MIMEText(body, 'alternative')
    message.attach(mime)

    try: #block to catch potential problems
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(from_Email, password)
        server.sendmail(from_Email, to_Email, message.as_string())
        server.quit()
        print('success')
    except Exception as element:
        print('failure')
        print(element)

    client.collection.remove()

if datetime.datetime.now().hour == 7: #sends an email every day at seven in the morning
    send_mail()