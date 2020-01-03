from bge import logic
import gunstandards
import packet_manager
import playeronly
import random
import client
import GameLogic as g

list = logic.getCurrentController().sensors['Collision'].hitObjectList

death_msgs = (
    '%victim% has been killed by %killer%',
    '%victim%\'s life was brought to an end by %killer%',
    '%killer% ended %victim%\'s life',
    '%killer% killed %victim%',
    '%killer% shot %victim%'
)

getScene = {}
for a in g.getSceneList():
    getScene[a.name] = a

healthbar = getScene['HUD'].objects['healthbar'] #hud
resetBar = 0.82

if len(list) > 0:
    snowball = list[0]

    controller = logic.getCurrentController()
    own = controller.owner
    damage = gunstandards.get_gun_damage(snowball['Type'])
    if snowball['Powerup']:
        damage = damage + 10
    health = own['Health']
    
    health = health - damage
    own['Health'] = health
    
    print('Hit', own['User'].get_name(), '! New health: ', health)
    
    if own['User'] == logic.globalDict['User']:
        healthbar.localScale.x -= resetBar / 100 * damage
        if healthbar.localScale.x <= 0 or health <= 0:
            healthbar.localScale.x = resetBar
                
    if health <= 0:
        # reset position and health, and add a score to the shooter
        shooter = snowball['Shooter'].get_avatar()
        points = shooter['Points']
        shooter['Points'] = points + 1
        print('Point got! New points: ', shooter['Points'])
        
        death_msg = str(random.choice(death_msgs)).replace('%victim%', own['User'].get_name()).replace('%killer%', snowball['Shooter'].get_name())
        
        packet_manager.send_packet({
            'id': 69,
            'sender': '',
            'message': death_msg})
        
        if snowball['Shooter'] == logic.globalDict['User']:
            packet_manager.send_packet({
                'id': 11,
                'victim': own['User'].get_name(),
                'killer': snowball['Shooter'].get_name()})
        
        own.worldPosition = logic.getCurrentScene().objects['PlayerSpawner'].worldPosition
        own['Health'] = 100