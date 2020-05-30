import smtplib
from email.mime.text import MIMEText

def send_mail(customer, dealer, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '07c52b8bed5cbd'
    password = '2d1a331dea128d'
    message = f"<h3>New Feedback Submission</h3><ul><li>Customer:{customer}</li><li>Dealer:{dealer}</li><li>Rating:{rating}</li><li>Comment:{comments}</li></ul>"

    sender_mail = 'email1@example.com'
    receiver_email = 'playtowin19@gmail.com'
    msg=MIMEText(message, 'html')
    msg['Subject'] = 'Lexus Feedback'
    msg['From'] = sender_mail
    msg['To'] = receiver_email

    #Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_mail, receiver_email, msg.as_string())