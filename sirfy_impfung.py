
import os 
import json
import urllib
import time
import mechanize
import ssl
from twilio.rest import Client
from getpass import getpass
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context

#flag to skip WhatsApp message - Set to False to use Twilio
skip_whatapp = False
test_whatsapp = True

cooldown_time = 15 # seconds

def test_twilio_message():

    client = init_twilio_client()

    twilio_number = os.environ['TWILIO_NUMBER']
    print(twilio_number)
    temp_dict = {}
    temp_dict['time'] = '10:00:00'
    temp_dict['Date'] = '01/01/2021'
    message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body='TESTING: Your appointment is coming up on {}  at {}'.format(temp_dict['Date'],
                                                                temp_dict['time']),      
                                    to=twilio_number 
                                ) 

    print(message)

def init_twilio_client():
    twilio_sid = os.environ['TWILIO_SID']
    twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']

    client = Client(twilio_sid, twilio_auth_token) 
    return client

def main():

    if not skip_whatapp:
        # set up twilio using https://www.twilio.com/blog/send-whatsapp-message-30-seconds-python
        client = init_twilio_client()

    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    params = {"versichert": "", "terminsuche": "", "uniqueident": "607feb7a343fb"}
    data = urllib.parse.urlencode(params)
    notified_id = []
    notify_wait = 0

    try:
        resp = br.open("https://onlinetermine.zollsoft.de/includes/searchTermine_app_feature.php", data)
        resp_dict = json.loads(BeautifulSoup(resp, 'html.parser').prettify())
        print(resp_dict)
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
            for termine in appt_dict and not skip_whatapp:
                if notify_wait > 6 and termine['id'] not in notified_id:
                    message = client.messages.create( 
                                        from_='whatsapp:+14155238886',  
                                        body='Your appointment is coming up on {}  at {}'.format(temp_dict['Date'],
                                                                    temp_dict['time']),      
                                        to=twilio_number 
                                    ) 
                    notified_id.append(termine['id'])
                    notify_wait = 0

        notify_wait +=1

    except Exception as exception:
        print(exception)

if __name__ == '__main__':
    while True:

        if test_whatsapp is True:
            print('test whatsapp message')
            test_twilio_message()

        main()
        time.sleep(cooldown_time)

