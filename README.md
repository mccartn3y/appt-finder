# Munich COVID-19 Vaccincation Appointment Alert

The python script in this file checks for appointments for COVID-19 vaccinations with [Dr. Sirfy](https://sirfy.de/sirfy-de-corona-impfung-muenchen/#termin) in Laim, München.

It optionally sends a WhatsApp message with the appointment date via Twilio. To use the Twilio service:
1. follow [this tutorial](https://www.twilio.com/blog/send-whatsapp-message-30-seconds-python) to set up an sandbox account with twilio.
1. Ensure to activate the WhatsApp Sandbox from [Whatsapp Sandbox](https://www.twilio.com/console/sms/whatsapp/sandbox) page by sending the unique message to Twilio number.
2. Create/Set the `TWILIO_SID`,`TWILIO_AUTH_TOKEN` and `TWILIO_NUMBER` environment variables tha values used in the Whatsapp Sandbox.
3. set the `skip_whatapp` flag in the code to `False`
