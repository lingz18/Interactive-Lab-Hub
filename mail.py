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

	filename = "output.mkv"
	attachment = open("~/lingz/Interactive-Lab-Hub/output.mkv", "rb")



	# msgText = MIMEText('<img src="/home/pi/test.jpg">', 'html')
	# msgAlternative.attach(msgTlsext)

	# attachment = "test.jpg"
	# fp = open(attachment, 'rb')
	# msgImage = MIMEImage(fp.read())
	# fp.close()
	p = MIMEBase('application', 'octet-stream')
	p.set_payload((attachment).read())
	encoders.encode_base64(p)
	p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	msgRoot.attach(p)

	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.starttls()
	smtp.login(fromEmail, fromEmailPassword)
	smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
	smtp.quit()