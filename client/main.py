import asyncio
import json
import pprint

from websockets.sync.client import connect

pp = pprint.PrettyPrinter(indent=4)

def sendPacket(json_request):
    with connect("ws://localhost:4455") as websocket:
        pp.pprint(json_request)
        websocket.send(json_request)
        message = websocket.recv()
        print(f"Received: {message}")
        return message

def changeScene(scene_name):
    request = {}
    request['op'] = 6
    data = {}
    data['requestType'] = "SetCurrentProgramScene"
    data['requestId'] = 1
    data['requestData'] = {"sceneName" : scene_name}
    request['d'] = json.dumps(data)
    sendPacket(json.dumps(request))

def authenticate():
    ##No password needed for the first versions of this project
    sendPacket({})
    request = {}
    request['op'] = 1
    data = {}
    data['rpcVersion'] = 1
    data['eventSubscriptions'] = 33
    request['d'] = json.dumps(data)
    pp.pprint(json.dumps(request))


    sendPacket(json.dumps(request))



authenticate()
##changeScene("scene")