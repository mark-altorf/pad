from bge import logic

cont = logic.getCurrentController()
own = cont.owner

def spawnNewPlayer(user_obj, spawningSelf=False):
    print('[ACTION] Spawning new player', user_obj.name)

    scene = logic.getCurrentScene()
    spawner = scene.objects['PlayerSpawner']
    avatar = scene.addObject('Player', spawner)
    avatar['User'] = user_obj
    user_obj.set_avatar(avatar)
    
    # set the name
    # avatar.sendMessage('Set name above head', user_obj.get_name(), 'PlayerName')
    
    if spawningSelf:
        logic.globalDict['Player'] = avatar
        logic.globalDict['User'] = user_obj
        logic.globalDict['PlayerView'] = avatar.children['PlayerView']
        for child in avatar.children:
            if child.name == 'PlayerModel':
                for child2 in child.children:
                    if child2.name == 'Glasses':
                        child2.visible = False
                print(child.name)
                child.visible = False

    return avatar

def set_active_camera(avatar):
    camera = avatar.children['PlayerView']
    scene = logic.getCurrentScene()
    scene.active_camera = camera