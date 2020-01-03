import bge
from bge import logic
import client
import server

scene = bge.logic.getCurrentScene()
cont = bge.logic.getCurrentController()
owner = cont.owner

packet_methods = []

print('Reading script again')

def prepare_network():
    logic.globalDict['networkPrepared'] = True
    bodies = cont.sensors['Start Game'].bodies
    if len(bodies) > 0 and owner['started'] is False and len(packet_methods) == 0:
        owner['started'] = True
        message = bodies[len(bodies) - 1]
        print('[MANAGER] Instantiating')

        if message == 'SERVER':
            # this user is hosting a room
            print('[SERVER] Starting server')
            server_obj = server.Server()

            logic.globalDict['isServer'] = True
            logic.globalDict['clientObj'] = server_obj

            packet_methods.append(server_obj)

            message = server.getServer(server_obj).get_full_ip()
        else:
            split = message.split(':')
            message = (split[0], int(split[1]))
            logic.globalDict['isServer'] = False

        print('[CLIENT] Starting client')
        client_obj = client.Client(message)
        logic.globalDict['clientObj'] = client_obj
        packet_methods.append(client_obj)

        # create client and join specified server
        client_obj.hostIP = message[0]
        client_obj.hostPort = int(message[1])

        print('[CLIENT] Connected to ' + client_obj.hostIP + ':' + str(client_obj.hostPort))

        client.join(client_obj)


def handle_packets():
    i = 0
    if isinstance(packet_methods[i], server.Server):
        # print('handle server')
        server.handle_packets(packet_methods[i])
        i += 1
    # print('handle client')
    client.handle_packets(packet_methods[i])


def send_packet(packet):
    packet_methods[len(packet_methods) - 1].send(packet)