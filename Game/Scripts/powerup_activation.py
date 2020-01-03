import bge
from bge import logic
import GameLogic as g

cont = logic.getCurrentController()
own = cont.owner
bodies = cont.sensors['Message'].bodies
print('message received')

getScene = {}
for a in g.getSceneList():
    getScene[a.name] = a

healthbar = getScene['HUD'].objects['healthbar'] #hud
resetBar = 0.82
scaleBar = 0.082

if len(bodies) > 0 and own['User'] == logic.globalDict['User']:
    type = bodies[0]
    if type == 'Heart':
        if own['Health'] < 100: #cant gain if health is full
            gain = min((100 - own['Health'], 10)) / 10
            healthbar.localScale.x += scaleBar * gain #bar itself increases
            own['Health'] += gain * 10 #gaining health
    else:
        own['CurrentPowerup'] = type
        own['PowerupTimer'] = 0