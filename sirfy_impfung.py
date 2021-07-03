
import os 
import json
import urllib
import time
import mechanize
import ssl
from twilio.rest import Client
from datetime import datetime
from bs4 import BeautifulSoup



ssl._create_default_https_context = ssl._create_unverified_context

#flag to skip WhatsApp message - Set to False to use Twilio
skip_whatapp = False
run_test_whatsapp = False#True
run_test_appt2dict = False
load_twilio_config = True

#Use thjis list to filter out aapointments from the log and messaging service
incl_kwrds = ['zweite', 'comirnaty']

if load_twilio_config:
    os.environ['TWILIO_SID'] = 'ACd94c1924c79aead0dcf7df3fa4b74c67'

    # load authentication token and destination number from json
    with open("twilio.auth", "r") as file:
        dic = json.load(file)
    os.environ['TWILIO_AUTH_TOKEN'] = dic['auth_token']
    os.environ['TWILIO_NUMBER'] = dic['to'] 

cooldown_time = 5 # seconds


def test_twilio_message():

    client = init_twilio_client()

    
    print(os.environ['TWILIO_NUMBER'])
    temp_dict = {}
    temp_dict['des'] = 'Paracetamoxifrusibendroneomycin vaccine'
    temp_dict['Date'] = '01/01/2021'
    message =  send_twilio(temp_dict['Date'], temp_dict['des'], client)

    print(message)

def send_twilio(date, desc, client):

	twilio_number = os.environ['TWILIO_NUMBER']
	message = client.messages.create( 
                                    from_='whatsapp:+14155238886',  
                                    body='Your {} appointment is coming up on {}'.format(desc,
                                                                date),      
                                    to=twilio_number 
                                    )
	print("Message send to {} successful".format(twilio_number))
	return message


def init_twilio_client():
    twilio_sid = os.environ['TWILIO_SID']
    twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']

    client = Client(twilio_sid, twilio_auth_token) 
    return client

def appt2dict(termine):
    temp_dict = {}
    temp_dict['Date'] = termine[0]
    temp_dict['time'] = termine[1]
    temp_dict['id'] = termine[2]
    temp_dict['doc'] = termine[3]
    temp_dict['desc'] = termine[4]
    if any([x.lower() in temp_dict['desc'].lower() for x in incl_kwrds]):
        print("{}: Appointment for {} on {} at {} with {}".format(datetime.now().strftime("%d/%m/%y %H:%M:%S"),
                                                        temp_dict['desc'],
                                                        temp_dict['Date'],
                                                        temp_dict['time'],
                                                        temp_dict['doc']))
    return temp_dict

def test_appt2dict():
	termine = ['01/01/2021', '14:00', '0001', 'Dr. Sirfy', 'Paracetamoxifrusibendroneomycin vaccine']
	print(appt2dict(termine))

def main():

    if skip_whatapp is not True:
        twilio_number = os.environ['TWILIO_NUMBER']
        # set up twilio using https://www.twilio.com/blog/send-whatsapp-message-30-seconds-python
        client = init_twilio_client()

    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    params = {"versichert": "", "terminsuche": "", "uniqueident": "607feb7a343fb"}
    data = urllib.parse.urlencode(params)
    #notified_id = []
    global notified_id
    global notify_wait
    #notify_wait = 0
    resp_dict = {'termine':None}
    try:
        resp = br.open("https://onlinetermine.zollsoft.de/includes/searchTermine_app_feature.php", data)
        resp_dict = json.loads(BeautifulSoup(resp, 'html.parser').prettify())

        if len(resp_dict['termine']) > 0:
            global appt_dict
            #appt_dict = []
            for termine in resp_dict['termine']:
                appt_dict.append(appt2dict(termine))

            # send message if one hasn't been sent about this appointment and in the last 30 secs
            for termine in appt_dict:
                if notify_wait > 6 and termine['id'] not in notified_id and not skip_whatapp and any([x.lower() in termine['desc'].lower() for x in incl_kwrds]):
                    message =  send_twilio(termine['Date'], termine['desc'], client) 
                    notified_id.append(termine['id'])
                    notify_wait = 0

        notify_wait +=1

    except Exception as exception:
        print(resp_dict['termine'])
        print(exception)


if __name__ == '__main__':

    if run_test_whatsapp is True:
        print('test whatsapp message')
        test_twilio_message()
        print('whatsapp message test complete')
    if run_test_appt2dict is True:
        print('test appointment printout')
        test_appt2dict()
        print('appointment printout test complete')
    global appt_dict
    global notify_wait
    global notified_id
    appt_dict = []
    notify_wait=0
    notified_id = []
    while True:
        main()
        time.sleep(cooldown_time)

