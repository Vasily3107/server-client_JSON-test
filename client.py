# client

from os import system
def cls(): system('cls')
def wait(): input('\nPress "Enter" to continue...')

import jsonpickle
import socket

from user import User


def log_in():
    cls()
    print('Logging in:\n')
    login    = input('   Login: ')
    password = input('Password: ')

    client.send(
        jsonpickle.encode({
            'act' : 'log in',
            'user': User(login, password)
            }).encode()
        )

    cls()
    print('Log in info sent\n')

    res = client.recv(1024).decode()
    print(f'Server response: {res}')


def sign_up():
    cls()
    print('Signing up:\n')
    login            = input('           Login: ')
    password         = input('        Password: ')
    confirm_password = input('Confirm password: ')

    repeat_text = f'Signing up:\n           Login: {login}'
    while password != confirm_password:
        cls()
        print('Password confirmation falure:\n')
        print(f'{password} =/= {confirm_password}')
        wait()

        cls(); print(repeat_text)
        password         = input('        Password: ')
        confirm_password = input('Confirm password: ')

    client.send(
        jsonpickle.encode({
            'act' : 'sign up',
            'user': User(login, password)
            }).encode()
        )

    cls()
    print('Sign up info sent\n')

    res = client.recv(1024).decode()
    print(f'Server response: {res}')


if __name__ == '__main__':
    IP = "127.0.0.1"
    PORT = 12345

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))

    print('Main menu:\n',
          '1 - log in',
          '2 - sign up\n', sep='\n')

    match input('Enter choise: '):
        case '1':
            log_in()

        case '2':
            sign_up()

        case _:
            cls()
            print('bad input')
            client.send(
                jsonpickle.encode({
                    'act' : 'false call',
                    'user': None
                    }).encode()
            )
            client.recv(1024)

    client.close()