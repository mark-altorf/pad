import json

buffersize = 2048

def ready_packet(data):
    return (json.dumps(data)).encode()

def parse(packet):
    return json.loads(packet.decode())