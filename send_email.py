###EMAIL SENDER SCRIPT###

#STEP1: IMPORT MODULES
import smtplib                                          #built-in python library that defines an SMTP client session object
from email.message import EmailMessage 
import os                                               #import OS

#--- Import Scripts and Functions ---
from build_email import generate_daily_report           #from build_email.py script
from config import *        					        #from config.py // email addresses, passwords

#STEP2: CONNECT TO EMAIL SERVER
server = smtplib.SMTP('smtp.gmail.com', 587)            #connect to Gmail's SMTP server on port 587
server.ehlo()                                           #extended hello to upgrade to secure if necessary
server.starttls()                                       #transport layer security
server.login(sender_email, app_password)                #from config

#STEP3: MESSAGE CONTENT
msg = EmailMessage()                                            #build email container. call it msg
email_data = generate_daily_report()                            #function from build_email.py
msg['Subject'] = email_data['subject']                          #grab subject
msg.set_content(email_data['text'])                             #grab text
msg.add_alternative(email_data['html'], subtype = 'html')       #grab html
print("email sent!! ")


#STEP5: SEND EMAIL
server.sendmail(from_addr = sender_email,                #send email
              to_addrs = receiver_email,
              msg = msg.as_string())
server.quit()                                            #close connetion





##DOCUMENTATION##
#importing the attribute from the module helps with formatting. reference: https://www.reddit.com/r/learnpython/comments/5hkasq/whenwhy_should_i_use_from_module_import_instead/
#utilized this guide: https://www.linkedin.com/pulse/how-send-gmail-using-python-himanshu-singh-fdqcf/
#Port465. starts encrypted  
#Port 587. unencrypted lane. Then computer asks to to secure through starttls
#Master guide: https://www.geeksforgeeks.org/python/how-to-send-automated-email-messages-in-python/

#timkim.emailbot@gmail.com 5tgb%TGB