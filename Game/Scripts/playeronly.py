import bge
from bge import logic
import packet_manager

def is_player(own=None):
    if own == None:
        controller = logic.getCurrentController()
        own = controller.owner
    return own['User'].get_uuid() == logic.globalDict['User'].get_uuid()

def and_():

    controller = logic.getCurrentController()
    own = controller.owner
    # check if sensors are true
    for sensor in own.sensors:
        if not sensor.positive:
            return
    if is_self():
        for actuator in own.actuators:
            controller.activate(actuators)

def and_inner():

    controller = logic.getCurrentController()
    own = controller.owner
    # check if sensors are true
    for sensor in own.sensors:
        if not sensor.positive:
            return
    if is_self(1):
        for actuator in own.actuators:
            controller.activate(actuators)

def and_doubleinner():

    controller = logic.getCurrentController()
    own = controller.owner
    # check if sensors are true
    for sensor in own.sensors:
        if not sensor.positive:
            return
    if is_self(2):
        for actuator in own.actuators:
            controller.activate(actuators)