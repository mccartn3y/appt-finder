# Munich COVID-19 Vaccincation Appointment Alert

The python script in this file checks for appointments for COVID-19 vaccinations with [Dr. Sirfy](https://sirfy.de/sirfy-de-corona-impfung-muenchen/#termin) in Laim, München.

It optionally sends a WhatsApp message with the appointment date via Twilio. To use the Twilio service:
1. follow [this tutorial](https://www.twilio.com/blog/send-whatsapp-message-30-seconds-python) to set up an sandbox account with twilio.
2. create a file "twilio.auth" containing your twilio authentication code and authorised number in the format
```{"auth_token": "<AUTH_CODE>", "to": "whatsapp:+49<PHONE_NUMBER>"}```
3. set the `skip_whatapp` flag in the code to `False`