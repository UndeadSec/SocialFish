import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 
def sendMail(subject, email, password, recipient, body, smtp, port):
	msg = MIMEMultipart()
	msg['From'] = email
	msg['To'] = recipient
	msg['Subject'] = subject
	 
	msg.attach(MIMEText(body, 'plain'))
	 
	try:
		server = smtplib.SMTP(smtp, int(port))
		server.starttls()
		server.login(email, password)
		text = msg.as_string()
		server.sendmail(email, recipient, text)
		server.quit()
		return 'ok'
	except Exception as err:
		pass	
		return err