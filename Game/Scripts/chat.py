import bge
import packet_manager
from bge import logic

scene = bge.logic.getCurrentScene()
cont = bge.logic.getCurrentController()

reciverSensor = cont.sensors['reciver']

if reciverSensor:
    owner = cont.owner
    body = reciverSensor.bodies
    message = body[0]
    sendable_message = str(message)
    packet_manager.send_packet({'id': 69, 'message': sendable_message, 'sender': logic.globalDict['User'].get_name()})
    logic.globalDict['ChatClosed'] = True