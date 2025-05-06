import socket
import argparse
import json

PORT = 10000
# Dict to store Dictionary
DICTIONARY:dict = None

# I assume the dictionary file will be in the same working directory as the server files. If not, you can 
# change the variable below to whatever to fit your needs.
DICTIONARY_DIRECTORY:str = 'dictionary.json'

# Open given dictionary and store the json file in DICTIONARY
with open(DICTIONARY_DIRECTORY, 'r') as json_file:
    DICTIONARY = json.load(json_file)

def find_definition(word:str):
    # return a dictionary search of a word. If nothing was found, return "Could not find definition"
    return str(DICTIONARY.get(word, "Could not find definition."))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', required=True, help='ip is the ip address the server should look to')
    args = parser.parse_args()



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

    # tell the socket to listen and have no backlog
    try:
        s.listen(0)
        print(f'Socket is now listening')
    except socket.error:
        print(f'Listen failed. Error {socket.error}')
        s.close()
        exit(-1)
    connection:socket = None
    try:
        while True:
            # accept new client
            connection, address = s.accept()
            print('got connection from ', address)
            
            # handle client
            try:
                while True:

                    word:str = None
                    word = connection.recv(4096)

                    if not word:
                        print(f'Client {address} disconnected.')
                        connection.close()
                        break

                    word = word.decode()

                    print(word)
                    definition:str = find_definition(word)
                    connection.send(definition.encode())
            except Exception:
                # if some error happens, close the connection
                print(f"Connection to {address} closed")
                connection.close()
                     
    except KeyboardInterrupt: # handle keyboard interrupt ^C
        s.close()
        exit(0)