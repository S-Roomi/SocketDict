import socket
import argparse
import json
import os
import signal

#Port address. Can change to whatever fits your needs
PORT = 10000

# Dict to store Dictionary
DICTIONARY:dict = None

# I assume the dictionary file will be in the same working directory as the server files. If not, you can 
# change the variable below to whatever to fit your needs.
DICTIONARY_DIRECTORY:str = 'dictionary.json'

# Open given dictionary and store the json file in DICTIONARY
with open(DICTIONARY_DIRECTORY, 'r') as json_file:
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
    # return a dictionary search of a word. If nothing was found, return "Could not find definition".
    return str(DICTIONARY.get(word, "Could not find definition."))

def handle_client(connection, address) -> None:
    # this is the same code as in server 1. Put it into a function so I can pass it as parameter in signal.signal
    try:
        while True:
            word:str = None
            word = connection.recv(4096)

            if not word:
                print(f'Client {address} disconnected.')
                connection.close()
                break

            word = word.decode()

            print(f"Received word from {address}: {word}")
            definition:str = find_definition(word)
            connection.send(definition.encode())
    except Exception:
        print(f"Connection to {address} closed")
        connection.close()

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', required=True, help='the ip address the server should look to')
    return parser.parse_args()


if __name__ == '__main__':
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

            pid = os.fork()

            if pid == 0:
                handle_client(connection, address)
            else:
                connection.close()
    except KeyboardInterrupt:
        # close the socket created in parent process
        s.close()
        exit(0)