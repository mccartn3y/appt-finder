import sys
import pickle
from getpass import getpass
import mechanize
from bs4 import BeautifulSoup
import json
import urllib
import time

#flag to skip WhatsApp message - Set to False to use Twilio
skip_whatapp = True

if not skip_whatapp:
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
notified_id = []
notify_wait = 0
while True:
    try:
        resp = br.open("https://onlinetermine.zollsoft.de/includes/searchTermine_app_feature.php", data)
        resp_dict = json.loads(BeautifulSoup(resp, 'html.parser').prettify())
        if len(resp_dict['termine']) > 0:
            appt_dict = []
            for termine in resp_dict['termine']:
                temp_dict = {}
                temp_dict['Date'] = termine[0]
                temp_dict['time'] = termine[1]
                temp_dict['id'] = termine[2]
                temp_dict['doc'] = termine[3]
                temp_dict['desc'] = termine[4]
                appt_dict.append(temp_dict)
                print("{}: Appointment for {} on {} at {} with {}".format(datetime.now().strftime("%d/%m/%y %H:%M:%S"),
                                                                      temp_dict['desc'],
                                                                      temp_dict['Date'],
                                                                      temp_dict['time'],
                                                                      temp_dict['doc']))
            # send message if one hasn't been sent about this appointment and in the last 30 secs
            for termine in appt_dict and not skip_whatapp::
                if notify_wait > 6 and termine['id'] not in notified_id:
                    message = client.messages.create( 
                                          from_='whatsapp:+14155238886',  
                                          body='Your appointment is coming up on {}  at {}'.format(temp_dict['Date'],
                                                                      temp_dict['time']),      
                                          to=num 
                                      ) 
                    notified_id.append(termine['id'])
                    notify_wait = 0
        notify_wait +=1
    except:
        pass
    time.sleep(5)
    
