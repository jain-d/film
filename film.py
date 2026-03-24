import os
import sys
from time import sleep
from pathlib import Path
import httpx
import logging
from twilio.rest import Client as TwilioClient

def check_listing():
    site_headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-encoding": "gzip, deflate, br, zstd",
        "Accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
        "appversion": "1.0",
        "Cache-control": "no-cache",
        "chain": "PVR",
        "city": "Hyderabad",
        "Content-length": "102",
        "Content-type": "application/json",
        "country": "INDIA",
        "Dnt": "1",
        "Origin": "https://www.pvrcinemas.com",
        "platform": "WEBSITE",
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        "Sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Microsoft Edge\";v=\"145\", \"Chromium\";v=\"145\"",
        "Sec-ch-ua-mobile": "?0",
        "Sec-ch-ua-platform": "\"Windows\"",
        "Sec-fetch-dest": "empty",
        "Sec-fetch-mode": "cors",
        "Sec-fetch-site": "same-site",
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"
    }

    request = httpx.Request(method="POST", url="https://api3.pvrcinemas.com/api/v1/booking/content/mshowtimes", headers=site_headers, json={"city":"Hyderabad","lat":"17.1827790564","lng":"78.60351551","dated":"2026-03-23","experience":"pxl"})


    timeout = httpx.Timeout(connect=5.0, read=20.0, write=10.0, pool=5.0)
    client = httpx.Client(timeout=timeout)
    response = client.send(request)
    return response

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
file_path = Path.cwd() / "workspace/film/calls"
#file_path = "./calls"
with open(file_path, "r") as file:
    content = int(file.read())

if content < 5:
    og_number = os.getenv("OG_NUMBER")
    dj_number = os.getenv("MY_NUMBER")
    mb_number = os.getenv("MB_NUMBER")
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    tw_client = TwilioClient(account_sid, auth_token)

    times = 0
    while times < 3:
        times += 1
        response = check_listing()
        if response.status_code == 200:
            break
        sleep(3)

    if response.status_code == 504:
        logging.error("Stopped after 5 504s.")
        sys.exit()

    dict_response = response.json()
    shows: list = dict_response["output"]["showTimeSessions"]

    if shows and shows[0]["movie"]["filmName"] == "DHURANDHAR THE REVENGE (HINDI) (A)" and shows[0]["movieCinemaSessions"][0]["cinema"]["theatreId"] == "371":
        logging.warning("LISTING FOUND")
        call_one = tw_client.calls.create(to=dj_number, from_=og_number, twiml="<Response><Say>The show is Listed. BOOK NOW. over and out.</Say></Response>")
        message_one = tw_client.messages.create(to=dj_number, from_=og_number, body="The show is Listed. BOOK NOW!")
        call_two = tw_client.calls.create(to=mb_number, from_=og_number, twiml="<Response><Say>The show is Listed. BOOK NOW. over and out.</Say></Response>")
        message_two = tw_client.messages.create(to=mb_number, from_=og_number, body="The show is Listed. BOOK NOW!")
        logging.info("INFORMED USERS")
        with open(file_path, "w") as file:
            content += 1
            file.write(str(content))
    else:
        logging.info("NO LISTING")
else:
    logging.info("Job Completed")
