import requests

header = {
    "X-API-Key" : "Panther",
    "x-access-token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI3YTBiNTQ4ZS1lOTMzLTRiZGItYTM4NC00ZTBhOTI4ODY5MTAiLCJleHAiOjE2NTAyMjY4OTl9.SUEN6I6l8c6S2zzTo7OsIEa79BJiG1DAQ-vrim2mYs4",
    'Content-type': 'multipart/form-data'
}
file = {
    "filee" : open(rf"C:\Users\jayendra\Music\Alan Walker, K-391 & Emelie Hollow - Lily.mp3" , "rb")
}

user_body = {
    "user" : "jayendra",
    "pw" : "some_stuff",
    "new_addr" : "0x5ecB3aD7071169A933F22CF3D1360a1a26D22737"
}

body = {
    "desc" :"ae",
    "victims" :"wdef",
    "ofenders":"wdef",
        
}
import json
data={
        'file': ("filename", open(rf"C:\Users\jayendra\Music\Alan Walker, K-391 & Emelie Hollow - Lily.mp3" , "rb"), "audio/x-wav"),
        'json': (None, json.dumps(body), 'application/json')
        }

files = [
    ('file1', ("random.json", open(rf"C:\Users\jayendra\Music\Alan Walker, K-391 & Emelie Hollow - Lily.mp3" , "rb"), "audio/x-wav")),
    ('file2', ("stuff.jpeg", open(rf"C:\Users\jayendra\Music\Alan Walker, K-391 & Emelie Hollow - Lily.mp3" , "rb"), "audio/x-wav")),
    ('file3', ("lmao.txt", open(rf"C:\Users\jayendra\Music\Alan Walker, K-391 & Emelie Hollow - Lily.mp3" , "rb"), "audio/x-wav")),
    ('file4', ("filename.mp4", open(rf"C:\Users\jayendra\Music\Alan Walker, K-391 & Emelie Hollow - Lily.mp3" , "rb"), "audio/x-wav")),
    ('file5', ("filename.mp3", open(rf"C:\Users\jayendra\Music\Alan Walker, K-391 & Emelie Hollow - Lily.mp3" , "rb"), "audio/x-wav")),
    ('data', ('data', json.dumps(body), 'application/json')),
]

#json=body , files=file

resp = requests.post("http://127.0.0.1:5000/upload_Data"  , files=files)
print(resp.text , resp.status_code , sep="\n")