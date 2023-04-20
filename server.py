import socket

from config import *
from engine import recv, send, get_hi

print('Starting server.', end='')
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
print('.', end='')
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
print('.')
server.bind(('', PORT))
print('Server started!', end='\n\n')

if SENDER == Sender.CLIENT:
    received = recv(server)
    with open(OUT_FILE, 'w') as file:
        file.write(received)
else:
    address = get_hi(server)
    server.settimeout(TIMEOUT)
    with open(IN_FILE, 'r') as file:
        send(server, file.read(), address)
