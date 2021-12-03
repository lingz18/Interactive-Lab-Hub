import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Email you want to send the update from (only works with gmail)
fromEmail = 'zl.tonyzhong@gmail.com'
# You can generate an app password here to avoid storing your password in plain text
# https://support.google.com/accounts/answer/185833?hl=en
fromEmailPassword = 'Lzzhfhd18.!?'

# Email you want to send the update to
toEmail = 'lz555@cornell.edu'

def sendEmail():
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = 'Fall Detected!'
	msgRoot['From'] = fromEmail
	msgRoot['To'] = toEmail
	msgRoot.preamble = 'Fall detected!'

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)
	msgText = MIMEText('Fall detected!')
	msgAlternative.attach(msgText)

	# msgText = MIMEText('<img src="cid:image1">', 'html')
	# msgAlternative.attach(msgText)

	# msgImage = MIMEImage(image)
	# msgImage.add_header('Content-ID', '<image1>')
	# msgRoot.attach(msgImage)

	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.starttls()
	smtp.login(fromEmail, fromEmailPassword)
	smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
	smtp.quit()