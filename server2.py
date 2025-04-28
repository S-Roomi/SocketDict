import socket
import argparse
import json
import os
import sys
import signal

PORT = 10000
DICTIONARY:dict = None

with open('dictionary.json', 'r') as json_file:
    DICTIONARY = json.load(json_file)

# Didn't use signum or frame but they are required to be in the function definition.
def handle_child(signum, frame) -> None:
    while True:
        try:
            # Tell the os to wait for all child processes and the other parameter is for telling the os not to hang around / wait. Do a quick check then move on
            pid, status = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break
        except:
            break

def find_definition(word:str) -> str:
    return str(DICTIONARY.get(word, "Could not find definition."))

def handle_client(connection, address) -> None:
    try:
        while True:
            word:str = connection.recv(4096).decode()
            if not word:
                print(f'Client {address} disconnected.')
                break

            print(word)
            definition:str = find_definition(word)
            connection.send(definition.encode())
    except Exception as exception:
        print(f"[CHILD] Error: {exception}")
    finally:
        connection.close()
        os._exit(0)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', required=True, help='ip is the ip address the server should look to')
    return parser.parse_args()

def main():
    args = get_arguments()

    # prepare for when the os sends the server a signal that a child process as finished. 
    # call handle_child when signal is received
    signal.signal(signal.SIGCHLD, handle_child)

    # attempt to create socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        print('socket was created successfully')
    except socket.error:
        print(f'socket failed to create. Error {socket.error}')
        sys.exit(-1)

    # bind the socket to the passed ip
    try:
        s.bind((args.ip, PORT))
        print(f'socket was bind to {args.ip}')
    except socket.error:
        print(f'Bind failed. Error {socket.error}')
        s.close()
        sys.exit(-1)

    # tell the socket to listen
    try:
        s.listen(5)
        print(f'Socket is now listening')
    except socket.error:
        print(f'Listen failed. Error {socket.error}')
        s.close()
        sys.exit(-1)
    connection:socket = None

    try:
        while True:
            connection, address = s.accept()
            print('got connection from ', address)
            pid = os.fork()

            if pid == 0:
                # close 
                s.close()
                handle_client(connection, address)
            else:
                connection.close()
    except KeyboardInterrupt:
        print("Connection closed")
        s.close()
        sys.exit(0)

if __name__ == '__main__':
    main()