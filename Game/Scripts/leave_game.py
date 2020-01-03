import bge
from bge import logic

controller = logic.getCurrentController()
own = controller.owner

def restart():
    controller.activate(controller.actuators['Restart'])