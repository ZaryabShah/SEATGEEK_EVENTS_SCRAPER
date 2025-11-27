from curl_cffi import requests
import json

url = "https://seatgeek.com/api/events"

# Querystring params
params = {
    "page": "2",
    "listing_count.gte": "1",
    "lat": "33.435505062124",
    "lon": "-112.06298828125",
    "range": "34mi",
    "sort": "datetime_local.asc",
    "client_id": "MTY2MnwxMzgzMzIwMTU4",
}

# Headers copied from your browser request
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://seatgeek.com/cities/phoenix",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Cookie": "vroom-ulid=; sg_l=en-US; sg_c=USD; sixpack_client_id=; SeatGeekEntrance=category=entrance%3Bdt=%3Bap=%3BadId=; sg_user_session_id=; rskxRunCookie=0; rCookie=; _gcl_au=; _ga=; _ketch_consent_v1_=; FPID=; FPAU=; _tt_enable_cookie=1; _ttp=; _fbp=; _gtmeec=; sd_client_id=; fc_storage_location=cookie; fc_pid_variable=fc_pid; _li_dcdm_c=.seatgeek.com; _lc2_fpi=; _lc2_fpi_js=; _bts=; fcd_li_attempted_whitelist_domain=seatgeek.com; fcd_li_last_attempted_whitelist=2025-11-26T23:53:56.697Z; fc_session=; _li_ss=CgA; sg_uuid=; sg_session=; sd_identity={\"userId\":\"\",\"traits\":{\"personId\":null}}; IR_gbd=seatgeek.com; FPLC=; sg-exit-intent-modal=true; ttcsid=; ttcsid_C4TLGV5G6B59DEMSOHN0=; _bti=; FPGSID=; _swb_consent_=; _ga_44M3TK17XS=; _ga_MYEXKXLE1H=; lastRskxRun=; forterToken=; IR_20501=; _uetsid=; _uetvid=; IR_PI=; datadome=t08eaNgUg8cYZ2zaXfLCv9mGpOzsbUORJDsC20WxSYbzegwAxczUwb5Z6Ap81ojVskGkI5G7xQN56FrmBPDmHSd9VxuMl4r~W4gHNqjy_n6WTvh2ewu1XY0RcCiNUZK5; _dd_s=",
    # "mparticle-session-id": "3095FB20-3153-4883-CDB1-EFADD8AAC74C",
    # "sixpack-client-id": "21c7c087-3eda-43a0-9d08-1b2b7cba4404",
    # "x-sg-currency-code": "USD",
    # "x-sg-forter-token": "480b2413ef2b4df59ed346d2861c38fb_1764201638700__UDF43-m4_23ck_",
    # "x-sg-locale": "en-US",
    # "x-sg-sift-session-id": "21c7c087-3eda-43a0-9d08-1b2b7cba4404",
    # "x-sg-user-session-id": "f19bdde1-03ef-47e0-a6c4-ae4d84a15612",
    # Optional networky headers (usually not strictly required for it to work):
    "Sec-CH-UA": "\"Chromium\";v=\"142\", \"Google Chrome\";v=\"142\", \"Not_A Brand\";v=\"99\"",
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": "\"Windows\"",
}

# Make the request
resp = requests.get(url, params=params, headers=headers)

# Raise if non-200, then parse JSON
resp.raise_for_status()
data = resp.json()

# Pretty-print JSON output
with open("output.json", "w") as f:
    json.dump(data, f, indent=4)