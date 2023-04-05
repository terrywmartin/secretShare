import os
#import smtplib
import random
import array
    
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.utils.html import escape
#from email.message import EmailMessage
#from email.headerregistry import Address
#from email import encoders
#from email.mime.base import MIMEBase
#from email.mime.text import MIMEText
#from email.mime.multipart import MIMEMultipart

def get_email_connection():
 use_tls = True
 use_ssl = False
 fail_silently=False
 connection = get_connection(host=settings.EMAIL_HOST, 
                        port=settings.EMAIL_PORT, 
                        username=settings.EMAIL_HOST_USER, 
                        password=settings.EMAIL_HOST_PASSWORD, 
                        use_tls=use_tls,
                        use_ssl=use_ssl,
            fail_silently=fail_silently)
 return connection

def email_user(email_address, html):
    #email_username = str(os.getenv('EMAIL_USERNAME'))
    #email_password = str(os.getenv('EMAIL_PASSWORD'))
    from_email = str(os.getenv('FROM_EMAIL'))
    
    success = { 'result': 0, 'message': ''}
    try:
            #connection = get_email_connection()
            email = EmailMessage('Secret Share Invitation',html, from_email, [email_address]) #,connection=connection)
            email.content_subtype = 'html'
            resp = email.send(fail_silently=False)

            success['message']=resp

    except Exception as ex:
            success['result'] = 0
            success['message'] = ex 
            print(ex)
    return success
""" 
def email_user_old(email, html):
        email_username = str(os.getenv('EMAIL_USERNAME'))
        email_password = str(os.getenv('EMAIL_PASSWORD'))
        
        msg = MIMEMultipart("alternative")
        msg['Subject'] = 'Secret Share Invitation'
        msg['From'] =str(os.getenv('FROM_EMAIL'))
        msg['To'] = email
       
        part = MIMEText(html, 'html')
        msg.attach(part)
        
        success = { 'result': 0, 'message': ''}
        try:
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.starttls()
            smtp.login(email_username, email_password)
            smtp.sendmail(str(os.getenv('FROM_EMAIL')), email, msg.as_string())
            #smtp.send_message(msg)
            smtp.quit()
            success['result'] = 1
            success['message'] = 'success'
        except Exception as ex:
            success['result'] = 0
            success['message'] = ex
            print(ex)
        return success
 """
def generate_password():
    
    # maximum length of password needed
    # this can be changed to suit your password length
    MAX_LEN = 12
    
    # declare arrays of the character that we need in out password
    # Represented as chars to enable easy string concatenation
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']
    
    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']
    
    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
            '*', '(', ')', '<']
    
    # combines all the character arrays above to form one array
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
    
    # randomly select at least one character from each character set above
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)
    
    # combine the character randomly selected above
    # at this stage, the password contains only 4 characters but
    # we want a 12-character password
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
    
    
    # now that we are sure we have at least one character from each
    # set of characters, we fill the rest of
    # the password length by selecting randomly from the combined
    # list of character above.
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)
    
        # convert temporary password into array and shuffle to
        # prevent it from having a consistent pattern
        # where the beginning of the password is predictable
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)
    
    # traverse the temporary password array and append the chars
    # to form the password
    password = ""
    for x in temp_pass_list:
            password = password + x
            
    # return out password
    return password