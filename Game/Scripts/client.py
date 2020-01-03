import uuid
import bge
from bge import logic
import random
import mathutils
import math
import socket
from network_globals import *

import packetActionTaker
import user

scene = bge.logic.getCurrentScene()


class Client:

    users = {}

    def __init__(self, host):
        self.own_uuid = str(uuid.uuid4())

        # print uuid used
        prints('Used uuid \'' + self.own_uuid + '\'')

        # choose random name (for testing purposes)
        self.name = logic.globalDict['Name']

        # create socket
        self.sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sckt.setblocking(False)
        self.server_addr = host

        # TODO: Shutdown packet
        # atexit.register(self.send_shutdown_packet)

        # globaldicts for chat system
        logic.globalDict['typing'] = False
        logic.globalDict['message1active'] = False
        logic.globalDict['message2active'] = False
        logic.globalDict['message3active'] = False
        logic.globalDict['message1'] = ''
        logic.globalDict['message2'] = ''
        logic.globalDict['message3'] = ''
        logic.globalDict['timeMessage1'] = 0
        logic.globalDict['timeMessage2'] = 0
        logic.globalDict['timeMessage3'] = 0
        self.message_timer = 600
        
        
        # dict for score screen
        self.playerNames = {'p1': '', 'p2': '', 'p3': '', 'p4': ''}
        self.Score = {'s1': 0, 's2': 0, 's3': 0, 's4': 0}
        self.Kills = {'k1': 0, 'k2': 0, 'k3': 0, 'k4': 0}
        self.Deaths = {'d1': 0, 'd2': 0, 'd3': 0, 'd4': 0}
        self.playersActive = {'p1a': False, 'p2a': False, 'p3a': False, 'p4a': False}

    def handle_packets(self):

        # as long as there is data in the buffer
        while True:
            try:
                data, addr = self.sckt.recvfrom(buffersize)
                data = parse(data)
                self.handle_packet(data, addr)

            except socket.error:
                # no more data in the buffer
                break

    def handle_packet(self, data, addr):
        id = data['id']
        if id != 2:
            prints('Received packet ' + str(id))
        # player hasn't joined before!
        if id == 0:

            # create player and set active camera if it's themselves
            user_obj = user.deserialize(data['User'])
            prints(user_obj.name + ' has joined the game!')

            self.users[user_obj.get_uuid()] = user_obj

            spawningSelf = user_obj.get_uuid() == self.own_uuid
            user_obj.character = packetActionTaker.spawnNewPlayer(user_obj, spawningSelf)

            if spawningSelf:
                # set active camera
                user_obj.character['Self'] = True
                packetActionTaker.set_active_camera(user_obj.character)
            else:
                user_obj.character['Self'] = False
                # set position of new player
                pos = data['Position']
                if pos is not None:
                    user_obj.character.worldPosition = pos

        if id == 1:

            self.player_quit(data['UUID'])

        elif id == 2:

            self.move_player(self.users[data['UUID']], data['Motion'])

        elif id == 3:
            # TODO: Return player list
            pass

        elif id == 4:
            # if requester UUID is equal to own UUID, ignore this packet
            if self.own_uuid == data['Requester']:
                prints('Ignoring packet 4')
                return
            
            user_obj = self.users[self.own_uuid]
            pos = user_obj.character.position
            packet = {
                'id': 4,
                'UUID': self.own_uuid,
                'Position': (pos.x, pos.y, pos.z),
                'Yaw': user_obj.character.worldOrientation.to_euler().z,
                'Requester': data['Requester']
            }
            self.send(packet)
        elif id == 5:
            self.shoot(data)
        elif id == 7:
            self.handle_powerups(data)
        elif id == 8:
            timer_game = data['time']
            self.timer(timer_game)
            # remove_message(self, timer_game)
        elif id == 69:
            message = data['message']
            chatting(self, message)
            
        elif id == 11:
            victim = data['victim']
            killer = data['killer']
            update_score_screen(self, victim, killer)
        
        elif id == 12:
            self.updateGun(data)
        
        elif id == 13:
            self.updateScoreScreen(data)
                
    def handle_powerups(self, data):
        prints('Spawning powerup!')
        if data['poweruptype'] == 1:
            if data['placepowerup'] == 1:
                scene.addObject('Heart', 'Spawn1')
            if data['placepowerup'] == 2:
                scene.addObject('Heart', 'Spawn2')
            if data['placepowerup'] == 3:
                scene.addObject('Heart', 'Spawn3')
            if data['placepowerup'] == 4:
                scene.addObject('Heart', 'Spawn4')
            
        if data['poweruptype'] == 2:
            if data['placepowerup'] == 1:
                scene.addObject('Candy', 'Spawn1')
            if data['placepowerup'] == 2:
                scene.addObject('Candy', 'Spawn2')
            if data['placepowerup'] == 3:
                scene.addObject('Candy', 'Spawn3')
            if data['placepowerup'] == 4:
                scene.addObject('Candy', 'Spawn4')

        if data['poweruptype'] == 3:
            if data['placepowerup'] == 1:
                scene.addObject('IceCrystal', 'Spawn1')
            if data['placepowerup'] == 2:
                scene.addObject('IceCrystal', 'Spawn2')
            if data['placepowerup'] == 3:
                scene.addObject('IceCrystal', 'Spawn3')
            if data['placepowerup'] == 4:
                scene.addObject('IceCrystal', 'Spawn4')


    def send(self, packet):
        # prints('Sending to ' + str(self.server_addr))
        self.sckt.sendto(ready_packet(packet), self.server_addr)

    def shoot(self, data):
        user_obj = self.users[data['UUID']]
        avatar = user_obj.get_avatar()
        
        # set yaw and pitch
        if not(user_obj.get_uuid() == logic.globalDict['User'].get_uuid()):
            yaw = data['Yaw'] / 180 * math.pi
            pitch = data['Pitch'] / 180 * math.pi
            avatar.children['PlayerView'].worldOrientation = mathutils.Euler((pitch, 0, yaw), 'XYZ').to_matrix()
        
        gun = avatar.children['PlayerView'].children['Gun']
        bullet = logic.getCurrentScene().addObject('Snowball', gun)
        bullet['Type'] = data['Type']
        bullet['Powerup'] = data['Powerup']
        bullet['Shooter'] = self.users[data['UUID']]
        if data['Type'] == 0:
            playsound.play('sniper')
        elif data['Type'] == 1:
            playsound.play('uzi')
        else:
            playsound.play('shotgun')
    
    def updateGun(self, data):
        user_obj = self.users[data['UUID']]
        avatar = user_obj.get_avatar()
        
        gun = avatar.children['PlayerView'].children['Gun']
        current_gun = data['GunType']
    
    def player_quit(self, uuid):
        avatar = self.users[uuid].character
        avatar.endObject()
        del self.users[uuid]

    def updateScoreScreen(self, data):
        numberOfPlayers = data['numberOfPlayers']
        cont = bge.logic.getCurrentController()
        owner = cont.owner
        if numberOfPlayers > 0:
            owner.sendMessage('p1', str(data['p1']))
            owner.sendMessage('d1', str(data['d1']))
            owner.sendMessage('s1', str(data['s1']))
            owner.sendMessage('k1', str(data['k1']))
        if numberOfPlayers > 1:
            owner.sendMessage('p2', str(data['p2']))
            owner.sendMessage('d2', str(data['d2']))
            owner.sendMessage('s2', str(data['s2']))
            owner.sendMessage('k2', str(data['k2']))
        if numberOfPlayers > 2:
            owner.sendMessage('p3', str(data['p3']))
            owner.sendMessage('d3', str(data['d3']))
            owner.sendMessage('s3', str(data['s3']))
            owner.sendMessage('k3', str(data['k3']))
        if numberOfPlayers > 3:
            owner.sendMessage('p4', str(data['p4']))
            owner.sendMessage('d4', str(data['d4']))
            owner.sendMessage('s4', str(data['s4']))
            owner.sendMessage('k4', str(data['k4']))

    def move_player(self, user_obj, velocity):

        # prints('MOVING: ' + user_obj.name)

        # apply movement
        player_object = user_obj.character
        # camera = player_object.children[0]

        # set yaw and pitch
        # degrees to radians
        yaw = velocity['Yaw'] / 180 * math.pi
        
        player_object.worldOrientation = mathutils.Euler((0, 0, yaw + math.pi / 2), 'XYZ').to_matrix()
        
        if not(user_obj.get_uuid() == logic.globalDict['User'].get_uuid()):
            
            pitch = velocity['Pitch'] / 180 * math.pi
            
            player_object.children['PlayerView'].worldOrientation = mathutils.Euler((pitch, 0, yaw), 'XYZ').to_matrix()

        w = velocity['W']
        s = velocity['S']
        a = velocity['A']
        d = velocity['D']

        # WASD
        if w != 0:
            player_object.applyMovement((w, 0, 0), True)
        elif s != 0:
            player_object.applyMovement((-s, 0, 0), True)

        if a != 0:
            player_object.applyMovement((0, a, 0), True)
        if d != 0:
            player_object.applyMovement((0, -d, 0), True)

        # jump
        if velocity['J']:
            constraints = bge.constraints.getCharacter(player_object)
            character = bge.types.KX_CharacterWrapper
            character.jump(constraints)

    
    def timer(self, timer_game):
        cont = bge.logic.getCurrentController()
        owner = cont.owner
        prints(timer_game)
        # ticks to seconds
        timer_game = timer_game / 60
        # minutes from seconds
        m = int(timer_game / 60)
        s = timer_game % 60
        time_left = str(m).zfill(2) + ":" + str(s).zfill(2)
        owner.sendMessage('time', time_left)
        prints(time_left)
        if timer_game == 0:
            owner.sendMessage('end game', 'leave game')
            self.send({'id': 1, 'Name': client.name, 'UUID': client.own_uuid, 'Points': self.users[self.own_uuid].get_avatar()['Points']})
            prints("end game")

def join(client):
    # join
    packet = {
        'id': 0,
        'Name': client.name,
        'UUID': client.own_uuid
    }
    prints('Sending join packet...')
    client.send(packet)
    client.send({'id': 69, 'message': 'The server IP is ' + logic.globalDict['ip'], 'sender': ''})


def chatting(self, message):
    cont = bge.logic.getCurrentController()
    owner = cont.owner
    if (message != '') and (message != logic.globalDict['message1']):
        if logic.globalDict['message1active'] == False:
            logic.globalDict['message1'] = message
            logic.globalDict['message1active'] = True
            logic.globalDict['timeMessage1'] = self.message_timer
            owner.sendMessage('first', message)
        elif logic.globalDict['message2active'] == False:
            logic.globalDict['message2'] = logic.globalDict['message1']
            logic.globalDict['message1'] = message
            logic.globalDict['message2active'] = True
            logic.globalDict['timeMessage2'] = logic.globalDict['timeMessage1']
            logic.globalDict['timeMessage1'] = self.message_timer
            owner.sendMessage('first', logic.globalDict['message1'])
            owner.sendMessage('second', logic.globalDict['message2'])
        else:
            logic.globalDict['message3'] = logic.globalDict['message2']
            logic.globalDict['message2'] = logic.globalDict['message1']
            logic.globalDict['message1'] = message
            logic.globalDict['message3active'] = True
            logic.globalDict['timeMessage3'] = logic.globalDict['timeMessage2']
            logic.globalDict['timeMessage2'] = logic.globalDict['timeMessage1']
            logic.globalDict['timeMessage1'] = self.message_timer
            owner.sendMessage('first', logic.globalDict['message1'])
            owner.sendMessage('second', logic.globalDict['message2'])
            owner.sendMessage('third', logic.globalDict['message3'])


def remove_message(self, time):
    cont = bge.logic.getCurrentController()
    owner = cont.owner
    self.message_timer = time
    if (logic.globalDict['timeMessage3'] - 30) == self.message_timer:
        logic.globalDict['message3active'] = False
        logic.globalDict['message3'] = ''
        owner.sendMessage('third', logic.globalDict['message3'])
    if (logic.globalDict['timeMessage2'] - 30) == self.message_timer:
        logic.globalDict['message2active'] = False
        logic.globalDict['message2'] = ''
        owner.sendMessage('second', logic.globalDict['message2'])
    if (logic.globalDict['timeMessage1'] - 30) == self.message_timer:
        logic.globalDict['message1active'] = False
        logic.globalDict['message1'] = ''
        owner.sendMessage('first', logic.globalDict['message1'])

def handle_packets(client):
    client.handle_packets()

def prints(msg):
    print('[CLIENT]', msg)
