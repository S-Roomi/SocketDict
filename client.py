import socket
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', required=True, type=str, help='ip is the ip address the server is running on')
    parser.add_argument('--port', required=True, type=int,help="the port the server is running on")
    args = parser.parse_args()

    h = socket.gethostbyname(args.ip)
    if h == None:
        print("gethostbyname failed to locate ", args.ip)
        exit(-1)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    except socket.error:
        print(f'socket call failed. Error {socket.error}')


    try:
        s.connect((h, args.port))
    except socket.error as error:
        print("connect() failed: ", error)
        exit(-1)

    try:
        while True:

            word = input('Please enter the word that you need defined: ').strip().lower()
            
            if not word:
                print('Empty input.')
                break

            s.send(word.encode())


            definition:str = s.recv(4096).decode()
            if not definition:
                print('Server closed connection')


            print(f'Server replied: {definition}')
    except KeyboardInterrupt:
        s.close()
        exit(0)