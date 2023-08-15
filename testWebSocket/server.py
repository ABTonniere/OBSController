import asyncio
import websockets
import json
 
# create handler for each connection
 
async def handler(websocket, path):
 
    data = await websocket.recv()
 
    reply = json.loads(data)
 
    await websocket.send(reply["id"])
    print(reply.keys())
 
 
 
start_server = websockets.serve(handler, "localhost", 6059)

 
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()