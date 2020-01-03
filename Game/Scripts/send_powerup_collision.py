import bge
from bge import logic

controller = logic.getCurrentController()
own = controller.owner

sensor = own.sensors['Collision']

print('WORKS')

for obj in sensor.hitObjectList:
    if 'Player' in obj:
        own.sendMessage('powerup hit', own['Name'])
        own.endObject()