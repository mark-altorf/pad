import bge
from bge import logic
import client

controller = logic.getCurrentController()
own = controller.owner

current_gun = own['CurrentGun']
print('Gun: ', current_gun)

actuators = controller.actuators
sensors = controller.sensors

selfScroll = own.parent.parent['User'] == logic.globalDict['User']

if current_gun == -1:
    own.replaceMesh('Sniper')
    own['CurrentGun'] = 0
elif selfScroll:
    if sensors['Gun Below'].positive:
        current_gun -= 1
    elif sensors['Gun Above'].positive:
        current_gun += 1
    
    if current_gun < 0:
        current_gun = 3
    elif current_gun > 3:
        current_gun = 0
    
    own['CurrentGun'] = current_gun
    print('Actual current: ', own['CurrentGun'])
    
    if current_gun == 0:
        own.replaceMesh('Sniper')
    elif current_gun == 1:
        own.replaceMesh('Uzi')
    elif current_gun == 2:
        own.replaceMesh('Shotgun')
    
    packet = {
        'id': 12,
        'GunType': current_gun,
        'UUID': logic.globalDict['User'].get_uuid()
    }
    print('SENDING GUN SWITCH PACKET')
    logic.globalDict['clientObj'].send(packet)