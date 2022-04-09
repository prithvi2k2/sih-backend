import threading
import socket
from datetime import datetime
import json
from xmlrpc.client import Server
import requests

user_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiIxNTYwMWY3MjdlZTEzOWMyY2VkNjhjZmYwMmU5NmRlNjEyYzdkYzg1ODc0MjBjYzY4YzdhOTdhMDE0NjUyNDFjIiwiZXhwIjoxNjUwNzQwMzcxfQ.EV5cmhTToRZVCDlqaiRFXS0BrfKjHI0SlGmTnSOy_bE"

police_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI5YjMwZWE1OS0yNzBkLTQ5ODItYjMwNy02MGUzOGU4MWEzMjkiLCJleHAiOjE2NTA3NDI4OTd9.m37AH91-K5TtrqEsi72ABloEtl0BxGztUrTTFwkiga4"

header = {
    "X-API-Key": "Panther",
    "x-access-token": police_token,

}
file = {
    "filee": open(rf"C:\Users\jayendra\Music\Alan Walker, K-391 & Emelie Hollow - Lily.mp3", "rb")
}

user_body = {
    "user": "mikasa",
    "password": "some_stuff",
    "new_addr": "0x5ecB3aD7071169A933F22CF3D1360a1a26D22737"
}

body = {
    "desc": "testing whole obj",
    "victims": "wdef",
    "time": str(datetime.now()),
    "classified_ByUser": "titan_attack",
    "location": "uppal"
}

files = [
    ('file1', ("random.json", open(
        rf"C:\Users\jayendra\Music\Alan Walker, K-391 & Emelie Hollow - Lily.mp3", "rb"), "audio/x-wav")),
    ('file2', ("stuff.jpeg", open(
        rf"C:\Users\jayendra\Music\Alan Walker, K-391 & Emelie Hollow - Lily.mp3", "rb"), "audio/x-wav")),
    ('file3', ("lmao.txt", open(
        rf"C:\Users\jayendra\Music\Alan Walker, K-391 & Emelie Hollow - Lily.mp3", "rb"), "audio/x-wav")),
    ('file4', ("filename.mp4", open(
        rf"C:\Users\jayendra\Music\Alan Walker, K-391 & Emelie Hollow - Lily.mp3", "rb"), "audio/x-wav")),
    ('file5', ("filename.mp3", open(
        rf"C:\Users\jayendra\Music\Alan Walker, K-391 & Emelie Hollow - Lily.mp3", "rb"), "audio/x-wav")),
    ('data', ('data', json.dumps(body), 'application/json')),
]

#json=body ,
police = ['Begumpet', 'Bowenpally', 'Bollaram', 'Trimulgherry', 'Sulthan_Bazar', 'Chaderghat', 'Afzalgunj', 'Kachiguda', 'Nallakunta', 'Malakpet', 'Saidabad', 'Amberpet', 'Abids', 'Narayanguda', 'Begum_Bazar', 'Gandhinagar', 'Musheerabad', 'Chikkadpally', 'Nampally', 'Ramgopalpet', 'Saifabad', 'Banjara_Hills', 'Jubilee_Hills', 'Panjagutta', 'SR_Nagar', 'Asifnagar', 'Humayunnagar', 'Lunger_House', 'Golconda', 'Tappachabutra',
          'Shahinayathgunj', 'Habeebnagar', 'Kulsumpura', 'Mangalhat', 'Gopalapuram', 'Tukaramgate', 'Lalaguda', 'Chilakalguda', 'Mahankali', 'Marredupally', 'Karkhana', 'Charminar', 'Bahadurpura', 'Kamatipura', 'Hussaini_Alam', 'Kalapattar', 'Mirchowk', 'Dabeerpura', 'Moghalpura', 'Rein_Bazar', 'Falaknuma', 'Chandrayangutta', 'Shalibanda', 'Chatrinaka', 'Kanchanbagah', 'Bhavani_Nagar', 'Madannapet', 'Santoshnagar']


# for i in police:
police_user = {
    "AuthorityID": "Lalaguda",
    "location": "Lalaguda",
    "password": "Lalaguda"
}

url = ["http://127.0.0.1:5000/upload_Data",
       "http://127.0.0.1:5000/patrol/get_cases",
       "http://127.0.0.1:5000/patrol/case_status"
       ]

resp = requests.get(url[1],
                    headers=header, json=police_user)


print(resp.text)
