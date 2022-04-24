import pymongo
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
    "wallet_addr": "0x5ecB3aD7071169A933F22CF3D1360a1a26D22737"
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

# json=body ,
police = ['Begumpet', 'Bowenpally', 'Bollaram', 'Trimulgherry', 'Sulthan_Bazar', 'Chaderghat', 'Afzalgunj', 'Kachiguda', 'Nallakunta', 'Malakpet', 'Saidabad', 'Amberpet', 'Abids', 'Narayanguda', 'Begum_Bazar', 'Gandhinagar', 'Musheerabad', 'Chikkadpally', 'Nampally', 'Ramgopalpet', 'Saifabad', 'Banjara_Hills', 'Jubilee_Hills', 'Panjagutta', 'SR_Nagar', 'Asifnagar', 'Humayunnagar', 'Lunger_House', 'Golconda', 'Tappachabutra',
          'Shahinayathgunj', 'Habeebnagar', 'Kulsumpura', 'Mangalhat', 'Gopalapuram', 'Tukaramgate', 'Lalaguda', 'Chilakalguda', 'Mahankali', 'Marredupally', 'Karkhana', 'Charminar', 'Bahadurpura', 'Kamatipura', 'Hussaini_Alam', 'Kalapattar', 'Mirchowk', 'Dabeerpura', 'Moghalpura', 'Rein_Bazar', 'Falaknuma', 'Chandrayangutta', 'Shalibanda', 'Chatrinaka', 'Kanchanbagah', 'Bhavani_Nagar', 'Madannapet', 'Santoshnagar']


# for i in police:
police_user = {
    "PatrolID": "Lalaguda",
    "location": "Lalaguda",
    "password": "Lalaguda"
}

url = ["http://127.0.0.1:3000/upload_Data",
       "http://127.0.0.1:3000/patrol/get_cases",
       "http://127.0.0.1:3000/patrol/case_status",
       "http://127.0.0.1:3000/signup",
       "http://127.0.0.1:3000/login",
       "http://127.0.0.1:3000/patrol/login"
       ]

# resp = requests.post(url[5],  headers=header, json=police_user)
# #

# print(resp.text)
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client["secrep"]

pipeline = [
    {
        '$match': {
            '_id': 'cf84303f-33a0-4273-9798-a5cc0dc1bde5'}
    }
]
with db.patrol.watch(pipeline) as stream:
    print("dfdgf")
    for insert_change in stream:
        print(insert_change)
        resume_token = stream.resume_token
