import socket
import argparse

PORT = 10000


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

    # bind the socket to the passed ip
    s.bind((args.ip, PORT))
    print(f'socket was bind to {args.ip}')

    # tell the socket to listen
    s.listen(5)
    print('socket is listening')

    while 1:
        connection, address = s.accept()
        print('got connection from ', address)

        connection.send('Thank you for connecting'.encode())

        connection.close()

        break