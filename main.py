import requests
import datetime as dt
import smtplib
import time

MY_LAT = 30.585163
MY_LONG = 36.238415
MY_EMAIL = "hassan_tariq74@outlook.com"
MY_PASS = "n;dsfrv"

def iss_is_above():
    responses = requests.get("http://api.open-notify.org/iss-now.json")
    responses.raise_for_status()
    datas = responses.json()
    iss_lat = float(datas["iss_position"]["latitude"])
    iss_lng = float(datas["iss_position"]["longitude"])
    if MY_LAT-5 <= iss_lat <= MY_LAT+5 and MY_LONG-5 <= iss_lng <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = data["results"]["sunrise"].split("T")[1].split(":")[0]
    sunset = data["results"]["sunset"].split("T")[1].split(":")[0]

    time_now = dt.datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_night() and iss_is_above():
        connection = smtplib.SMTP("smtp.office365.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASS)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Look Up!!\n\nThe iss is above u."
        )

