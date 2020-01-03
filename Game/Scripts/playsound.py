import aud

def play(file):
    sound = aud.Factory.file('Sounds/' + file + '.mp3')
    device = aud.device()
    device.play(sound)