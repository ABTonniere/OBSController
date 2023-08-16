import asyncio
import websockets
import os
import json
import socket

SERVER_IP = "localhost"
SERVER_PORT = 6059

exit = False

message = { "id" : os.getlogin() ,
            "ip" : socket.gethostbyname(socket.gethostname()) ,
            "data" : {
                "command" : "",
                "args" : ""
            }}


async def sendRequest(request):
    async with websockets.connect("ws://" + SERVER_IP + ":" + str(SERVER_PORT)) as websocket:

        await websocket.send(json.dumps(request))
        response = await websocket.recv()
        response = json.loads(response)

        return response
    


while exit == False:

    command = int(input("Enter command: \n1 - Get Clients\n2 - Change Current Scene\n3 - Exit\n"))

    match command:
        case 1:
            message["data"]["command"] = "getClients"
        
        case 2:
            message["data"]["command"] = "changeSceneByName"
            message["data"]["args"] = input("Enter scene name: ")

        case 3:
            exit = True


    if exit == False:
        
        data = asyncio.get_event_loop().run_until_complete(sendRequest(message))
        print(data)
        