import httpx
import json

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

request = httpx.Request(method="POST", url="https://api3.pvrcinemas.com/api/v1/booking/content/mshowtimes", headers=site_headers, json={"city":"Hyderabad","lat":"17.1827790564","lng":"78.60351551","dated":"2026-03-18","experience":"pxl"})

#print(request.headers)

client = httpx.Client()

response = client.send(request)
dict_response = response.json()
shows: list = dict_response["output"]["showTimeSessions"]
print(json.dumps(shows[0]))

#print(f"\n\033[32m{response.status_code}\033[0m\n\n{response.text}\n\n")
#print(f"{response.request.method}\n{response.request.headers}\n\n{response.request.content}")
