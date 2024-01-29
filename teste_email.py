import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_port = 587
smtp_server = "email-ssl.com.br"
email_sender = "informativo@selecao.vitoriasupervarejo.com.br"
password = '6A%X&#yNrv262B%4QVYxpR8*'
email_receiver = "lorenzotbolfe@gmail.com"


msg = MIMEMultipart()
msg['From'] = email_sender
msg['To'] = email_receiver
msg['Subject'] = 'Assunto do E-mail'

# Corpo do e-mail
body = 'Conteúdo do seu e-mail aqui.'
msg.attach(MIMEText(body, 'plain'))

# Iniciar uma conexão segura com o servidor SMTP do Gmail
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()

# Login no servidor SMTP do Gmail
server.login(email_sender, password)

# Enviar e-mail
text = msg.as_string()
server.sendmail(email_sender, email_receiver, text)

# Encerrar a conexão com o servidor SMTP do Gmail
server.quit()

print('E-mail enviado com sucesso!')



# message = """\
# Subject: Hi there

# This message is sent from Python."""



# try:
#     with smtplib.SMTP_SSL(smtp_server, port) as server:
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message)
#         server.quit()
#         print("tudo ok")
# except Exception as e:
#     print(e)