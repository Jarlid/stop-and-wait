import socket

from config import *
from engine import send, recv

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.settimeout(TIMEOUT)
address = ('127.0.0.1', PORT)

if SENDER == Sender.CLIENT:
    with open(IN_FILE, 'r') as file:
        send(client, file.read(), address)
else:
    pass
