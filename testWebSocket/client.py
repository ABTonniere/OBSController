import asyncio
import websockets
import os
import json


message = { "id" : os.getlogin() , "data" : {}}

async def test():
    async with websockets.connect('ws://localhost:6059') as websocket:

        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        print(response)

asyncio.get_event_loop().run_until_complete(test())