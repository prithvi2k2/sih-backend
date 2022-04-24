# Importing the relevant libraries
# import websockets
# import asyncio

# import socketio


import socketio


# standard Python
sio = socketio.Client()


@sio.event()
def connect():
    print("I'm connected!")
    sio.emit(
        'Get_OnLocation', {"Status": "uppal",
                           "pid": 2})


@sio.event
def connect_error(error):
    print(error)


@sio.on('CasesUpadte',)
def on_message(data):
    print("sde")
    print('', data)


@sio.on('error_msg',)
def on_message(data):
    print("sde")
    print('Price', data)

    # sio.emit('getcase', {'userKey': '2'}, namespace='/chat')


head = {"x-access-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJjZjg0MzAzZi0zM2EwLTQyNzMtOTc5OC1hNWNjMGRjMWJkZTUiLCJleHAiOjE2NTE0ODAxMTR9.pzjex2XXyBLNNPy_T6poy62ZnZSby1kIg_jo-Jek03E",
        "X-API-Key": "Panther"}

sio.connect('http://127.0.0.1:3000',
            headers=head)
# The main function that will handle connection and communication
# with the server


# async def listen():
#     url = "https://secrep.herokuapp.com/"
#     # Connect to the server
#     async with websockets.connect(url) as ws:
#         # Send a greeting message
#         await ws.send("Hello Server!")
#         # Stay alive forever, listening to incoming msgs
#         while True:
#             msg = await ws.recv()
#             print(msg)

# # Start the connection
# asyncio.get_event_loop().run_until_complete(listen())
