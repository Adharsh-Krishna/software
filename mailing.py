import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



def send_mail_attachment(sender,receiver,subject,body,attachment_name,password):

	msg = MIMEMultipart()
	msg['From'] = sender
	msg['To'] = receiver
	msg['Subject'] = subject

	msg.attach(MIMEText(body, 'plain'))
	slash_index=attachment_name.rfind("/")
	filename = attachment_name[slash_index+1:]
	attachment = open(attachment_name, "rb")

	p = MIMEBase('application', 'octet-stream')
	p.set_payload((attachment).read())
	encoders.encode_base64(p)
	p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	msg.attach(p)

	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(sender, password)
	text = msg.as_string()
	s.sendmail(sender, receiver, text)
	s.quit()


def send_code(receiver,subject,body,code):
	print receiver
	print subject,body
	print code
	sender="xxx"
	password="yyy"
	msg= MIMEMultipart()
	msg['From']=sender
	msg['To']=receiver
	msg['Subject']=subject
	body=body + str(code)
	msg.attach(MIMEText(body,'plain'))
	
	server=smtplib.SMTP('smtp.gmail.com',587)
	server.starttls()
	server.login(sender,password)
	text=msg.as_string()
	server.sendmail(sender,receiver,text)
	server.quit()

