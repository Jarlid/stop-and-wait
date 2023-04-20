from enum import Enum


class Sender(Enum):
    CLIENT = 0
    SERVER = 1


SENDER = Sender.SERVER

PORT = 6666
TIMEOUT = 1.0
LOST_PERCENTAGE = 30
HI_STRING = 'HI!'
ACK_STRING = 'ACK'

BATCH_SIZE = 1024

IN_FILE = 'alice.txt'
OUT_FILE = 'out.txt'
