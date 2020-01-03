import bge
from bge import logic

controller = logic.getCurrentController()
own = controller.owner

if 'Player' in logic.globalDict and own == logic.globalDict['Player'].children['PlayerView']:
    controller.activate(own.actuators['Mouse'])