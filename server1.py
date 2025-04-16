import socket
import argparse
import json

PORT = 10000
DICTIONARY:dict = None

def find_definition(word:str):
    return str(DICTIONARY.get(word, "Could not find definition."))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', required=True, help='ip is the ip address the server should look to')
    args = parser.parse_args()

    with open('dictionary.json', 'r') as json_file:
        DICTIONARY = json.load(json_file)

    # attempt to create socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        print('socket was created successfully')
    except socket.error:
        print(f'socket failed to create. Error {socket.error}')
        exit(-1)

    # bind the socket to the passed ip
    try:
        s.bind((args.ip, PORT))
        print(f'socket was bind to {args.ip}')
    except socket.error:
        print(f'Bind failed. Error {socket.error}')
        s.close()
        exit(-1)

    # tell the socket to listen
    try:
        s.listen(5)
        print(f'Socket is now listening')
    except socket.error:
        print(f'Listen failed. Error {socket.error}')
        s.close()
        exit(-1)
    connection:socket = None
    try:
        while True:
            connection, address = s.accept()
            print('got connection from ', address)

            while True:
                word:str = None
                word = connection.recv(4096)

                word = word.decode()
                if not word:
                    print(f'Client {address} disconnected.')
                    break

                print(word)
                definition:str = find_definition(word)
                connection.send(definition.encode())
            
            s.close()
            print("Connection closed")
    except KeyboardInterrupt:
        s.close()
        exit(0)