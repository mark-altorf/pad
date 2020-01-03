import bge
from bge import logic
import packet_manager

# object variables
controller = logic.getCurrentController()
own = controller.owner
camera = own.children['PlayerView']

constraints = bge.constraints.getCharacter(own)
character = bge.types.KX_CharacterWrapper

keyboard = logic.keyboard
keyInput = bge.logic.KX_INPUT_ACTIVE

speed = .1
if keyInput == keyboard.events[bge.events.LEFTSHIFTKEY]:
    speed /= 2

velocity = {
    'W': 0,
    'S': 0,
    'A': 0,
    'D': 0,
    'J': False,
    'Yaw': camera.worldOrientation.to_euler().z
}

# print('Camera Rot: ' + str(camera.worldOrientation.to_euler().z))
moved = False

    #chat system
if keyInput == keyboard.events[bge.events.ENTERKEY]:
    own.sendMessage('enter was hit')
    logic.globalDict['typing'] = False
    
if keyInput == keyboard.events[bge.events.TKEY]:
    logic.globalDict['typing'] = True

if logic.globalDict['typing'] == False:
    if keyInput == keyboard.events[bge.events.WKEY]:
        moved = True
        velocity['W'] = speed
    if keyInput == keyboard.events[bge.events.SKEY]:
        moved = True
        velocity['S'] = speed
    if keyInput == keyboard.events[bge.events.AKEY]:
        moved = True
        velocity['A'] = speed
    if keyInput == keyboard.events[bge.events.DKEY]:
        moved = True
        velocity['D'] = speed

    if keyInput == keyboard.events[bge.events.SPACEKEY]:
        moved = True
        velocity['J'] = True

if moved and own['Self'] and logic.globalDict['typing'] == False:

    # send move packet
    packet = {
        'id': 2,
        'UUID': own['User'].get_uuid(),
        'Motion': velocity
    }
    print('[CLIENT] Sending move packet')
    packet_manager.send_packet(packet)
    