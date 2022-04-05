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
    "location": "here"


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

resp = requests.post("http://127.0.0.1:5000/Get_CaseInfo", json={"case_id": 'e50c1c86-f7be-4163-90f2-530f48110249'},
                     headers=header)
print(resp.text, resp.status_code, sep="\n")
