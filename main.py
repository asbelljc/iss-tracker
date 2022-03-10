from dotenv import load_dotenv
import os
import time
import requests
import smtplib
from datetime import datetime

load_dotenv()

SMTP = os.getenv('SMTP')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
MY_LAT = os.getenv('LATITUDE')
MY_LONG = os.getenv('LONGITUDE')


def is_iss_overhead():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data['iss_position']['latitude'])
    iss_longitude = float(data['iss_position']['longitude'])

    if (
        MY_LAT - 5 <= iss_latitude <= MY_LAT + 5
        and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5
    ):
        return True


def is_night():
    parameters = {'lat': MY_LAT, 'long': MY_LONG, 'formatted': 0}

    response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])
    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP(SMTP)
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg='Subject:Look Up👆\n\nThe ISS is overhead!',
        )
