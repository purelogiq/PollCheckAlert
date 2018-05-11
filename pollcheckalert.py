#!/usr/bin/python3
import requests
import smtplib
import time
from datetime import datetime
from pytz import timezone
from email.mime.multipart import MIMEMultipart

# SETUP
poll_frequency_seconds = 5 * 60 # CHANGE ME
data = None
old_data = None


def poll_check_alert():
    global data
    global old_data
    alert_message = None

    # POLL: Do something to update data and old_data
    old_data = data
    data = requests.get(
        'https://bugzilla.mozilla.org/rest/jobqueue_status',
        params={'Bugzilla_api_key': 'a bugzilla api key'} # CHANGE ME
    ).json()

    # CHECK: Check the data and set alert message/details if we should alert
    if old_data and data['total'] >= old_data['total'] and old_data['total'] > 0:
        tz = timezone('US/Eastern')
        current_time = datetime.now(tz).strftime('%c')
        alert_message = (
            'Job Queue Growing! - '
            + current_time
            + ' (old: %s, now: %s)' % (old_data['total'], data['total'])
        )

    # ALERT: Send off an alert if needed
    if alert_message:
        fromaddr = "example@gmail.com" # CHANGE ME
        toaddr = "example@gmail.com" # CHANGE ME
        msg = MIMEMultipart()
        msg['Subject'] = alert_message
        # If using gmail you'll have to enable less secure apps at
        # https://myaccount.google.com/lesssecureapps
        # might want to use a less important address as the sender
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "from email password") # CHANGE ME
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

while True:
    poll_check_alert()
    time.sleep(poll_frequency_seconds)
