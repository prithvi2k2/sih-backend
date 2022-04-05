from datetime import datetime
import json
import requests

header = {
    "X-API-Key": "Panther",
    "x-access-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJkMjY1YWY1My1iODRiLTQ5N2YtOGQwOS1kNTAzMTQzMTAzMTQiLCJleHAiOjE2NTAzMTQ3NDR9.aq1U6A13H6Gs7hMIkcGg0q1tFmvPBXwM8_dxlK0WLhs",

}
file = {
    "filee": open(rf"C:\Users\jayendra\Music\Alan Walker, K-391 & Emelie Hollow - Lily.mp3", "rb")
}

user_body = {
    "user": "mikasa",
    "pw": "some_stuff",
    "new_addr": "0x5ecB3aD7071169A933F22CF3D1360a1a26D22737"
}

body = {
    "desc": "ae",
    "victims": "wdef",
    "time": str(datetime.now()),
    "classified_ByUser": "titan_attack",
    "location": "Saidabad"


}
data = {
    'file': ("filename", open(rf"C:\Users\jayendra\Music\Alan Walker, K-391 & Emelie Hollow - Lily.mp3", "rb"), "audio/x-wav"),
    'json': (None, json.dumps(body), 'application/json')
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
resp = requests.post("http://127.0.0.1:5000/upload_Data",
                     headers=header, files=files)
