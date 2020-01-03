NAME_KEY = 'Name'
UUID_KEY = 'UUID'
ADDR_KEY = 'Address'

class User:

    '''
    socket is None when the object is used in the client class.

    Only the server needs to associate sockets with users. The client doesn't do that.
    '''
    def __init__(self, name, addr, new_uuid):
        self.uuid = new_uuid
        self.name = name
        self.addr = addr
        self.character = None

    def serialize(self):
        return {
            UUID_KEY: self.uuid,
            NAME_KEY: self.name,
            ADDR_KEY: self.addr,
        }

    def get_full_ip(self):
        return self.addr

    def get_ip(self):
        return self.get_full_ip()[0]

    def get_port(self):
        return self.get_full_ip()[1]

    def get_uuid(self):
        return self.uuid

def deserialize(data):
    return User(data[NAME_KEY], None, data[UUID_KEY])
