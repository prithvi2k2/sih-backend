from numpy import tri
import websockets
import asyncio
import websockets_routes
from config import db


router = websockets_routes.Router()
PORT = 5001

print("Server listening on Port " + str(PORT))


@router.route('/classified/{case_type}/{pid}')
async def echo(websocket, path):
    print("A client just connected")
    try:
        Flag = True
        async for message in websocket:
            print("Received message from client: " + message)
            case_type, pid = path.params["case_type"], path.params["pid"]
            try:
                page_id = int(pid)
                cases = db.reports.find(
                    {"classified_ByUser": 'titan_attack'}).limit(20)

            except:
                Flag = False
            while Flag:
                await websocket.send("Pong: " + cases)
                await asyncio.sleep(10)
                cases = db.reports.find(
                    {"classified_ByUser": 'titan_attack'}).limit(20)

    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")

server = router.serve("localhost", PORT)


asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
