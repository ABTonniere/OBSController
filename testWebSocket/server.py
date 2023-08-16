import asyncio
import websockets
import json
import socket
 
# create handler for each connection

clients = ["Gustavo", "Rafael", "Joao"]
 
async def handler(websocket, path):
 
    data = await websocket.recv()
 
    request = json.loads(data)

    if request["id"] not in clients:
        clients.append(request["id"])


    match request["data"] :
        
        case "getClients":
            await websocket.send(json.dumps(clients))

        case other:
            await websocket.send(json.dumps("Invalid command"))


    #await websocket.send()
    #print(socket.gethostbyname(socket.gethostname()))
    print(request["id"])
 
 
 
start_server = websockets.serve(handler, "0.0.0.0", 6059)

 
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()