import bge
from bge import logic

def send_start_client_msg():

    scene = bge.logic.getCurrentScene()
    cont = bge.logic.getCurrentController()

    click_sensor = cont.sensors['Click']
    hover_sensor = cont.sensors['Hover']

    if click_sensor.positive and hover_sensor.positive:
        
        owner = cont.owner

        # get entered IP address
        ipAddress = scene.objects['Text Prompt']['Text']
        # print('Entered: ' + ipAddress)
        
        if len(ipAddress) == 0:
            return

        # load arena scene
        cont.activate(cont.actuators['Load Arena'])

        owner.sendMessage('start', ipAddress)

def send_start_server_msg():
    cont = bge.logic.getCurrentController()
    
    click_sensor = cont.sensors['Click']
    hover_sensor = cont.sensors['Hover']

    if click_sensor.positive and hover_sensor.positive:
        
        owner = cont.owner
        
        # load arena scene
        cont.activate(cont.actuators['Load Arena'])

        print('message sent!')
        owner.sendMessage('start', 'SERVER')
