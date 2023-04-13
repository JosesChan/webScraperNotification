import pandas
import re
import os
import smtplib



sender = "Private Person <from@example.com>"
receiver = "A Test User <to@example.com>"

message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From: {sender}

This is a test e-mail message."""

with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
    server.login(os.environ.get('MAIL_USER'), os.environ.get('MAIL_PASS'))
    server.sendmail(sender, receiver, message)


# Get lists of urls from url_list.txt
def getListURL():
    url_file = open('url_list.txt','r')
    urlData = url_file.read()
  
    # Split urls by lines
    urlList = urlData.split("\n")
    url_file.close()

    # Return content without empty lines
    return filter(lambda x: not re.match(r'^\s*$', x), urlList)

# export the dataframe as CSV
def exportCSV(exportDataframe):
    exportDataframe.to_csv("Available Stock.csv")