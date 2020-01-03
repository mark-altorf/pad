import time


def game_timer(x):
    timer_game = abs(int(x))

    while timer_game > 0:
        m, s = divmod(timer_game, 60)
        h, m = divmod(m, 60)
        time_left = str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)
        print(time_left + "\r")  # insert code to sent time to game
        time.sleep(1)
        timer_game -= 1
        if timer_game == 0:
            print("end game")  # insert code to stop blender game

while True:
    uin = input(">> ")
    try:
        game_timer(uin)
    except KeyboardInterrupt:
        break
