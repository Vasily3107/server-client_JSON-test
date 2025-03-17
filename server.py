# server

import jsonpickle
import socket

from user import User
from db_functions import find_user_in_db, get_user_logins, add_user_to_db

IP = "127.0.0.1"
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(1)

conn, addr = server.accept()
print('user accepted \n')

data = jsonpickle.decode(conn.recv(1024))

print(f'received data: {data}\n')

act  = data['act']
user = data['user']

match act:
    case 'log in':
        if find_user_in_db(user):
            conn.send(b'Log in is successful')
        else:
            conn.send(b'Log in failure')

    case 'sign up':
        if user.login in get_user_logins():
            conn.send(b'Name is already taken')
        else:
            add_user_to_db(user)
            conn.send(b'Sign up is successful')

    case 'false call':
        conn.send(b'');

    case _:
        print(f'\n\n {act = } \n\n')
        conn.send(b'Server failure')
        conn.close()
        server.close()
        raise 'Act match default case'

print('server closed')
conn.close()
server.close()