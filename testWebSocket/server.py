import asyncio
import websockets
import json
import socket
 
# create handler for each connection
 
async def handler(websocket, path):
 
    data = await websocket.recv()
 
    reply = json.loads(data)
 
    await websocket.send(socket.gethostbyname(socket.gethostname()))
    #print(socket.gethostbyname(socket.gethostname()))
    print(reply["id"])
 
 
 
start_server = websockets.serve(handler, "0.0.0.0", 6059)

 
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()