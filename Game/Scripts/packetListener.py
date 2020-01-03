import socket
import pickle


class PacketListener:
    BUFFER_SIZE = 1024

    def __init__(self, port=0, host=False):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._ip = socket.gethostbyname(socket.getfqdn())
        self._port = port
        self._prefix = '[SERVER] ' if host else '[CLIENT] '
        self.define_socket(host)

    # define socket
    def define_socket(self, host=False):
        self._socket.setblocking(False)
        port = 0
        if self._port < 0 or self._port > 65535:
            port = self._port
        self._socket.bind((self._ip, self._port))
        if host:
            print(self._prefix + 'Server IP: ' + str(self._socket.getsockname()[0]) + ':' + str(self._socket.getsockname()[1]))

    def listen_for_packets(self):
        # using a while loop in case of multiple packets received
        while True:
            try:
                # listen for incoming packets
                data, addr = self._socket.recvfrom(self.BUFFER_SIZE)
                address = addr[0] + ':' + str(addr[1])
                print(self._prefix + 'Received packet from ' + address)
                msg = pickle.loads(data)
                print(self._prefix + 'Packet content: ' + str(msg))
                return msg, addr

            except socket.error:
                # this is called when data is set to an invalid value, meaning there are no more packets to read
                return None

    def get_full_ip(self):
        return self._socket.getsockname()

    def get_port(self):
        return self._socket.getsockname()[1]

    def send(self, packet_data, destination):
        self._socket.sendto(packet_data, destination)
