# SocketDict

This project implements a client-server application where a client can look up a word and the server will return its definition. There is three versions of the server that have been implemented to demonstrate different ways a server can manage clients.

## Files

**Client** that connects to a server and requests definitions to words a user provides
**Server1**: A Basic single client server
**Server2**: A concurrent server that uses fork to handle multiple clients
**Server3**: Another concurrent server that uses select instead of fork to handle multiple clients
**Dictionary** A simple json file that stores a dictionary with a word linked to it's definition

## How to run

#### Prerequisites

- I used Python 3.12.0 but most versions 3.8 or higher would work
- A Linux or Mac OS is required for server2 because of the usage of fork
- Insure that a proper dictionary file is in the active directory. Additionally, you can pass a working directory to the DICTIONARY_DIRECTORY variable in code for all three of the servers.


#### Running

First, run the server. To do this, you will need to call python on the server file and pass the ip address as a parameter. An example of running a server on ip 127.0.0.1 is provide below for server 1, 2, and 3.

server1
```bash
python3 server1.py --ip=127.0.0.1
```
server2
```bash
python3 server2.py --ip=127.0.0.1
```
server3
```bash
python3 server3.py --ip=127.0.0.1
```

To run a client and have it access a server on port 10000, follow the code below.

```bash
python3 client.py --ip=127.0.0.1 --port=10000
```


## Test Cases

**For all the test cases, try with incorrect spellings, uppercase and lowercase characters, empty strings, etc. I included some but not all**

#### Test Case for Server1

Test valid connection and valid word. Then closing connection

```bash
python3 server1.py --ip=127.0.0.1
```

```bash
python3 client.py --ip=127.0.0.1 --port=10000

Please enter the word that you need defined: apple
```

Now test if another connection will interrupt current connection

In another shell
```bash
python3 client.py --ip=127.0.0.1 --port=10000
```

Test with incorrect spelling
```bash
python3 client.py --ip=127.0.0.1 --port=10000

Please enter the word that you need defined: apdlele
```
Test with empty word
```bash
python3 client.py --ip=127.0.0.1 --port=10000

Please enter the word that you need defined:
```

#### Test Case for Server2

```bash
python3 server2.py --ip=127.0.0.1
```

Test with one client
```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: apple
...
```

Test with two clients
```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: apple
...
```
```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: banana
...
```

Now try to connect multiple clients and see if they all get their word process and get their definitions. Try with correct and incorrect spelling. Empty strings

```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: apple
...
```
```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: banana
...
```
```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: peard
...
```
```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: peacha
...
```
```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: 
...
```



#### Test Case for Server3

```bash
python3 server3.py --ip=127.0.0.1
```

Test with 1 client

```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: apple
...
```

Test with multiple clients

```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: apple
...
```

```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: banana
...
```

```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: pear
...
```

```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: peach
...
```
```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: 
...
```
```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: incorrect word
...
```
```bash
python3 client.py --ip=127.0.0.1 --port=10000
Please enter the word that you need defined: asddsadasdas
...
```