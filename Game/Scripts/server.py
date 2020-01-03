import json
import socket
import select
import errno
import uuid
import time
import random
from network_globals import *

from user import User

class Server:

    users = {}
    time_left = 36000
    playerNames = {'p1': "palyer 1", 'p2': "player 2", 'p3': "player 3", 'p4': "player 4"}
    Score = {'s1': 0, 's2': 0, 's3': 0, 's4': 0}
    Kills = {'k1': 0, 'k2': 0, 'k3': 0, 'k4': 0}
    Deaths = {'d1': 0, 'd2': 0, 'd3': 0, 'd4': 0}
    playersActive = {'p1a': False, 'p2a': False, 'p3a': False, 'p4a': False}

    def __init__(self):
        self.timer = 0
        self.numberOfPlayers = 1
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try :
            hostname = socket.gethostbyname(socket.getfqdn())
        except:
            try:
                hostname = socket.gethostbyname(socket.gethostname())
            except:
                hostname = '127.0.0.1'
        self.server_socket.bind((hostname, 0))
        self.server_socket.setblocking(False)
        self.address = self.server_socket.getsockname()
        print('[SERVER] Hosting on: ', self.address)

    def get_full_ip(self):
        return self.address

    def is_not_registered(self, addr):
        for usr in self.users.values():
            usr_addr = usr.get_full_ip()
            if usr_addr[0] == addr[0] and usr_addr[1] == addr[1]:
                return False
        return True

    def handle_packets(self):
        self.handle_powerups()
        if self.timer % 60 == 0:
            self.broadcast({'id': 8, 'time': self.time_left - self.timer})
        self.timer += 1
        
        # as long as there is data in the buffer
        while True:
            try:
                data, addr = self.server_socket.recvfrom(buffersize)
                data = parse(data)
                self.handle_packet(data, addr)

            except socket.error:
                # no more data in the buffer
                break
            
    def handle_powerups(self):
        poweruptype = random.randint(1, 3)
        placepowerup = random.randint(1, 4)
        
        if self.timer % 150 == 0:
            powerup = {
                   'poweruptype' : poweruptype,
                   'placepowerup' : placepowerup,
                   'timer' : self.timer,
                   'id' : 7
                   }
            self.broadcast(powerup)
                          
    def handle_packet(self, data, addr):
        id = data['id']
        # player hasn't joined before!
        if self.is_not_registered(addr):

            if id != 0:
                prints('Packet was not a join packet but was still used as one!')

            self.create_player(data, addr)

        if id == 1:

            self.player_quit(data)

        elif id == 2:

            self.player_move(data)

        elif id == 3:

            self.view_player_list(data['User'])

        elif id == 4:

            # a client is sending their current location to a new client so they can be spawned on the new client
            self.send_loc_to_new_client(data)

        elif id == 5:
            
            self.shoot(data)

        elif id == 69:
            self.chatting(data)
            
        elif id == 11:
            self.kill(data['victim'], data['killer'])
        
        elif id == 12:
            self.updateGuns(data)
            
        elif id == 13:
            self.broadcast({'id': 13, 
        'p1': self.playerNames['p1'],
        'p2': self.playerNames['p2'],
        'p3': self.playerNames['p3'],
        'p4': self.playerNames['p4'],
        's1': self.Score['s1'],
        's2': self.Score['s2'],
        's3': self.Score['s3'],
        's4': self.Score['s4'],
        'k1': self.Kills['k1'],
        'k2': self.Kills['k2'],
        'k3': self.Kills['k3'],
        'k4': self.Kills['k4'],
        'd1': self.Deaths['d1'],
        'd2': self.Deaths['d2'],
        'd3': self.Deaths['d3'],
        'd4': self.Deaths['d4'],
        'numberOfPlayers': self.numberOfPlayers 
        }) 

    def create_player(self, msg, addr):

        # add ip with player name
        new_uuid = msg['UUID']
        user_obj = User(msg['Name'], addr, new_uuid)
        self.users[new_uuid] = user_obj
        
        if not self.playersActive['p1a']:
            self.playerNames['p1'] = msg['Name']
            self.playersActive['p1a'] = True
            self.numberOfPlayers = 1
        elif not self.playersActive['p2a']:
            self.playerNames['p2'] = msg['Name']
            self.playersActive['p2a'] = True
            self.numberOfPlayers  = 2
        elif not self.playersActive['p3a']:
            self.playerNames['p3'] = msg['Name']
            self.playersActive['p3a'] = True
            self.numberOfPlayers = 3
        else:
            self.playerNames['p4'] = msg['Name']
            self.playersActive['p4a'] = True
            self.numberOfPlayers  = 4

        print('[SERVER] ' + msg['Name'] + ' has joined the game!')
        print('[SERVER] Current player count: ', len(self.users))

        self.broadcast({
            'id': 0,
            'User': user_obj.serialize(),
            'Position': None
        })

        # request position of all players except the joining one
        if len(self.users) > 1:
            self.broadcast({
                'id': 4,
                'Requester': new_uuid
            })
    
    def updateGuns(self, data):
        self.broadcast(data)
    
    def shoot(self, data):
        self.broadcast(data)
    
    def broadcast(self, packet_info):
        for user_obj in self.users.values():
            self.send_to(packet_info, user_obj.get_full_ip())

    def broadcast_except(self, packet_info, ip):
        for user_obj in self.users.values():
            if user_obj.get_ip()[0] != ip[0] and user_obj.get_port != ip[1]:
                self.send_to(packet_info, user_obj.get_full_ip())

    def send_to(self, packet_info, socket):
        self.server_socket.sendto(ready_packet(packet_info), socket)

    def send_loc_to_new_client(self, msg):
        prints('Sending loc to new client')
        user_obj = self.users[msg['Requester']]
        self.send_to({
            'id': 0,
            'User': self.users[msg['UUID']].serialize(),
            'Position': msg['Position'],
            'Yaw': msg['Yaw']
        }, user_obj.get_full_ip())

    def player_quit(self, data):
        self.broadcast(data)
        del self.users[data['UUID']]

    def player_move(self, msg):
        self.broadcast({
            'id': 2,
            'UUID': msg['UUID'],
            'Motion': msg['Motion']
        })

    def view_player_list(self, socket):
        self.send_to({
            'id': 3,
            'List': json.dumps(list(self.users.values()))
        }, socket)

    def chatting(self, msg):
        sender = '>> '
        if len(msg['sender']) > 0:
            sender = '[' + msg['sender'] + ']: '
        self.broadcast({
            'id': msg['id'],
            'message': sender + msg['message']
        })
    
    def kill(self, victim, killer):
        # add deaths
        if victim == self.playerNames['p1']:
            self.Deaths['d1'] += 1
            self.Score['s1'] -= 25
        if victim == self.playerNames['p2']:
            self.Deaths['d2'] += 1
            self.Score['s2'] -= 25
        if victim == self.playerNames['p3']:
            self.Deaths['d3'] += 1
            self.Score['s3'] -= 25
        if victim == self.playerNames['p4']:
            self.Deaths['d4'] += 1
            self.Score['s4'] -= 25
            # add kills
        if killer == self.playerNames['p1']:
            self.Score['s1'] += 100
            self.Kills['k1'] += 1
        if killer == self.playerNames['p2']:
            self.Score['s2'] += 100
            self.Kills['k2'] += 1
        if killer == self.playerNames['p3']:
            self.Score['s3'] += 100
            self.Kills['k3'] += 1
        if killer == self.playerNames['p4']:
            self.Score['s4'] += 100
            self.Kills['k4'] += 1           
    

def handle_packets(server):
    server.handle_packets()

def getServer(server):
    return server

def prints(msg):
    print('[SERVER] ', msg)
    

