import socket
from _thread import *
import pickle
from game import Game

server = "192.168.0.110"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(10)
print("Waiting for a connection, Server Started")

connected = set()
rooms={}
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    #userRoom = conn.recv(1024).decode()
    
    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    
    # if userRoom:
    #     if int(userRoom) in rooms:
    #         if len(list(rooms)[int(userRoom)]) % 2 ==1:
    #             print("Joined A Room")
    #             rooms[int(userRoom)].append(conn)  
    #         else:
    #             print("Room Full Create new Room")
    #             rooms[int(userRoom)]=conn
                
           
    
    
    # if userRoom % 2 == 1:
    #     games[userRoom] = Game(userRoom)
    #     print("Creating a new game...")
    # else:
    #     games[userRoom].ready = True
    #     p = 1


    start_new_thread(threaded_client, (conn, p, gameId))