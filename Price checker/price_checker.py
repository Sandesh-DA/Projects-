
import smtplib
import ssl
import os
import urllib.request
from bs4 import BeautifulSoup 
import time

def check_price():
    fp = urllib.request.urlopen('https://www.amazon.in/Casio-Enticer-Analog-Watch-MTP-VD01D-1EVUDF-A1362/dp/B07C9GY2YY/ref=pd_vtp_h_pd_vtp_h_sccl_6/262-6773424-7206715?content-id=amzn1.sym.6c9a4279-ad42-4fd6-b9a9-3cd14ede34c9&pd_rd_i=B07C9GY2YY&psc=1')
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    heads = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}

    soup = BeautifulSoup(mystr,'html.parser')
    title  = soup.find('span',id='productTitle').text.strip()
    price = soup.find('span',class_="a-price-whole").get_text()
    converted_price = float(price.replace(',',''))

    if(converted_price < 2000): # price checker 
        send_mail()
    


def send_mail():
    smtp_port = 587                 # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    email_from = EMAIL_ADDRESS
    email_to = EMAIL_ADDRESS
    
    pswd = EMAIL_PASSWORD

    # content of message

    subject = 'Price fell down !'

    body = 'Check Amazon link https://www.amazon.in/Casio-Enticer-Analog-Watch-MTP-VD01D-1EVUDF-A1362/dp/B07C9GY2YY/ref=pd_vtp_h_pd_vtp_h_sccl_6/262-6773424-7206715?content-id=amzn1.sym.6c9a4279-ad42-4fd6-b9a9-3cd14ede34c9&pd_rd_i=B07C9GY2YY&psc=1'

    message = f'Subject : {subject}\n\n{body}'

    # Create context
    simple_email_context = ssl.create_default_context()


    try:
        # Connect to the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls(context=simple_email_context)
        TIE_server.login(email_from, pswd)
        print("Connected to server :-)")
    
        # Send the actual email
        print()
        print(f"Sending email to - {email_to}")
        TIE_server.sendmail(email_from, email_to, message)
        print(f"Email successfully sent to - {email_to}")

    # If there's an error, print it out
    except Exception as e:
        print(e)

    # Close the port
    finally:
        TIE_server.quit()


while (True):
    check_price()
    time.sleep(86400)





