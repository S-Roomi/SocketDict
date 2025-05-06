import socket as s
import argparse
import json
import select


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

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', required=True, help='The ip address the server should look to')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_arguments()

    # attempt to create socket
    try:
        server_socket = s.socket(s.AF_INET, s.SOCK_STREAM, s.IPPROTO_TCP)
        print('Socket was created successfully')
    except s.error:
        print(f'Socket failed to create. Error {s.error}')
        exit(-1)

    # bind the socket to the passed ip
    try:
        server_socket.bind((args.ip, PORT))
        print(f'Socket was bind to {args.ip}')
    except s.error:
        print(f'Bind failed. Error {s.error}')
        server_socket.close()
        exit(-1)

    # tell the socket to listen
    try:
        server_socket.listen(5)
        print(f'Socket is now listening')
    except s.error:
        print(f'Listen failed. Error {s.error}')
        server_socket.close()
        exit(-1)
    
    

    #create a list of sockets
    sockets_list = [server_socket]

    #create a dictionary of clients. Match connection to address
    clients = {}

    try:
        while True:
            read_sockets, _ , exception_sockets = select.select(sockets_list, [], [])
            
            for socket in read_sockets:

                # check if the given socket is the server socket, if so accept client
                if socket == server_socket:
                    connection, address = server_socket.accept()

                    # add client to socket_list and client dict
                    sockets_list.append(connection)
                    clients[connection] = address

                    print(f"Got connection from {address}")
                else:
                    # handle client
                    try: 
                        word = socket.recv(4096).decode()

                        if not word:
                            print(f"Client {clients[socket]} sent empty word ")
                            
                            sockets_list.remove(socket)
                            del clients[socket]
                            socket.close()

                        
                        print(f"Received word from {clients[socket]}: {word}")
                        definition = find_definition(word)
                        socket.send(definition.encode())

                    except:
                        # remove client if an error happens
                        print(f"Error with {clients[socket]}")
                        sockets_list.remove(socket)
                        del clients[socket]
                        socket.close()

            # iterate over the exception_sockets. I just removed them.
            for socket in exception_sockets:
                sockets_list.remove(socket)
                if socket in clients:
                    del clients[socket]
                socket.close()
        
    except KeyboardInterrupt: # handle keyboard interrupt ^C
        print("Connection closed")
        server_socket.close()
        exit(1)