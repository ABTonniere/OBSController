import logging
logging.basicConfig(level=logging.DEBUG)
import asyncio
import simpleobsws
import websockets
import json
import socket



parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)

ws = simpleobsws.WebSocketClient(url = 'ws://localhost:3945', password = '', identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.



clients = {}
##with open("utilisateurs.json", "r") as file:
    ##clients = json.load(file)
"""
async def make_request():
    await ws.connect() # Make the connection to obs-websocket
    await ws.wait_until_identified() # Wait for the identification handshake to complete

    request = simpleobsws.Request('SetCurrentProgramScene',{ "sceneName": "scene2"}) # Build a Request object

    ret = await ws.call(request) # Perform the request
    if ret.ok(): # Check if the request succeeded
        print("Request succeeded! Response data: {}".format(ret.responseData))

    await ws.disconnect() # Disconnect from the websocket server cleanly
"""

async def changeSceneByName(name):
    await ws.connect() # Make the connection to obs-websocket
    await ws.wait_until_identified() # Wait for the identification handshake to complete

    request = simpleobsws.Request('SetCurrentProgramScene',{ "sceneName": name}) # Build a Request object

    ret = await ws.call(request) # Perform the request
    if ret.ok(): # Check if the request succeeded
        print("Request succeeded! Response data: {}".format(ret.responseData))

    await ws.disconnect() # Disconnect from the websocket server cleanly



 
# WebSocket handler function
async def handler(websocket, path):
    try:
        data = await websocket.recv()
        request = json.loads(data)

        command = request["data"]["command"]

        match command:

            case "connected":
                #vérifie si l'utilisateur est connecté
                if request["id"] in clients.keys():
                    await websocket.send(json.dumps("Connected"))
                else:
                    await websocket.send(json.dumps("Not connected"))
            
            case "signUp":
                if request["id"] not in clients.keys():
                    clients[request["id"]] = request["data"]["args"]
                    await websocket.send(json.dumps("Signed up"))
                else:
                    await websocket.send(json.dumps("Already signed up"))

            case "getUsername":
                await websocket.send(json.dumps(clients[request["id"]]))

            case "getClients":
                await websocket.send(json.dumps(clients))
    
            case "changeSceneByName":
                await changeSceneByName(request["data"]["args"])
                await websocket.send(json.dumps("Scene changed"))
    
            case "changeToMyScene":
                await changeSceneByName(clients[request["id"]])
                await websocket.send(json.dumps("Scene changed successfully"))
    
            case _:
                await websocket.send(json.dumps("Invalid command"))



        logging.info("%s : %s", request["id"], command)
    except websockets.exceptions.ConnectionClosed as e:
        logging.info("Connection closed: %s", e)
    except Exception as e:
        logging.error("Error in handler: %s", e)
 
 
 
start_server = websockets.serve(handler, "0.0.0.0", 6059)

 
#asyncio.get_event_loop().run_until_complete(make_request())

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()





