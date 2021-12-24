from requests import get
import mysql.connector
import smtplib

ip = get('https://api.ipify.org').content.decode('utf8')
ipf = format(ip)

data = [host="", user="", password="", database=""]

mydb = mysql.connector.connect(data)
d = mysql.connector.connect(data)

# grabbing the old ip
mycursor = mydb.cursor()

mycursor.execute("SELECT ip FROM ips WHERE id = '1'")
current = ""
myresult = mycursor.fetchone()
current = myresult[0]


# once it has then new ip it update the old
m = d.cursor()

sql = "UPDATE ips SET ip = '" + ip + "' WHERE id = '1'"

m.execute(sql)

d.commit()

print("Record Updated")

# smtp setup
sender_email = ""  # Enter your address
password = ""
body = "The server public IP has changed. Please update DDNS. Original IP: " + current + " | New IP: " + ip

to = []
subject = 'DDNS Update Alert'

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sender_email, ", ".join(to), subject, body)
if ip != current:
    try:
        server = smtplib.SMTP_SSL('mail.smtp2go.com', 465)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, to, email_text)
        server.close()

        print("Email sent!")
    except:
        print("Something went wrong...")
