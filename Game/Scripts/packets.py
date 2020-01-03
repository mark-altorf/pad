import bge
from bge import logic
import packet_manager
import math
import playeronly
import time
import gunstandards

controller = logic.getCurrentController()
own = controller.owner

def shoot():
    
    if not playeronly.is_player(own.parent.parent):
        return
    
    mouse = logic.mouse
    input = bge.logic.KX_INPUT_ACTIVE
    
    button_sensor = controller.sensors['Shoot']
    
    if button_sensor.positive:    
        cur_gun = own['CurrentGun']
        
        cooldownname = 'Cooldown' + str(cur_gun)
        
        if ('hold' not in own or not own['hold']) and (cooldownname not in own or get_millis() > own[cooldownname]):
            if cur_gun == 1:
                print('Shooting uzi')
            cam_rot = own.parent.worldOrientation.to_euler()
            # radians to degrees
            yaw = cam_rot.z / math.pi * 180
            pitch = cam_rot.x / math.pi * 180
            roll = cam_rot.y / math.pi * 180

            # to prevent the reversed controls bug
            if abs(roll) > 20:
                yaw = 180 - yaw
            
            if 'CurrentPowerup' not in own:
                pwrup = ''
            else:
                pwrup = own['CurrentPowerup']
            packet = {
                'id': 5,
                'UUID' : logic.globalDict['User'].get_uuid(),
                'Yaw': yaw,
                'Pitch': pitch,
                'Type': cur_gun,
                'Powerup': pwrup == 'Ice' and own['PowerupTimer'] <= 6
            }
            
            cooldown = get_millis() + gunstandards.get_gun_firerate(cur_gun)
            own[cooldownname] = cooldown
            
            packet_manager.send_packet(packet)
            own['hold'] = True
        elif cur_gun == 1:
            # button is held, for uzi only
            pass
    else:
        if 'hold' not in own or own['hold']:
            # button released
            own['hold'] = False

def get_millis():
    return int(round(time.time() * 1000))