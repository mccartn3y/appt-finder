import sys
import pickle
from getpass import getpass
import mechanize
from bs4 import BeautifulSoup
import json
import urllib
import time

# set up twilio using https://www.twilio.com/blog/send-whatsapp-message-30-seconds-python
from twilio.rest import Client
account_sid = 'ACd94c1924c79aead0dcf7df3fa4b74c67'

# load authentication token and destination number from json
with open("twilio.auth", "r") as file:
    dic = json.load(file)
auth_token = dic['auth_token']
num = dic['to']
client = Client(account_sid, auth_token) 

br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
params = {"versichert": "", "terminsuche": "", "uniqueident": "607feb7a343fb"}
data = urllib.parse.urlencode(params)

while True:
    resp = br.open("https://onlinetermine.zollsoft.de/includes/searchTermine_app_feature.php", data)
    resp_dict = json.loads(BeautifulSoup(resp, 'html.parser').prettify())
    if len(resp_dict['terminsuchen']) >0 or len(resp_dict['termine']) > 0:
        print(resp_dict)
        message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='Your appointment is coming up on July 21 at 3PM',      
                              to=num 
                          ) 
    time.sleep(10)
    
