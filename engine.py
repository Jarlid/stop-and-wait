from random import randint
import socket

from config import LOST_PERCENTAGE, BATCH_SIZE, ACK_STRING, ACK_SIZE


def data_split(data: bytes):
    return [data[i:i + BATCH_SIZE] for i in range(0, len(data), BATCH_SIZE)]


def pack(data_portion: bytes, index):
    return bytes([index]) + data_portion


def unpack(packet: bytes):
    return packet[0], packet[1:]


def troubled_sendto(self, thing, address):
    if randint(0, 99) >= LOST_PERCENTAGE:
        self.sendto(thing, address)


def try_sendto(self, thing, address, index, num, num_all):
    while True:
        try:
            troubled_sendto(self, pack(thing, index), address)

            ack, _ = self.recvfrom(ACK_SIZE + 1)
            ack_index, ack_data = unpack(ack)
            if ack_index != (index + 1) % 2 or ack_data.decode('ascii') != ACK_STRING:
                continue
            print(f'Successfully sent package #{num} (out of {num_all}).')
            break

        except socket.timeout:
            pass


def send(self, data, address):
    data = data_split(data.encode('ascii'))

    for num, data_portion in enumerate(data):
        try_sendto(self, data_portion, address, num % 2, num + 1, len(data))

    try_sendto(self, b'\0', address, len(data) % 2, 0, len(data))


def try_recvfrom(self, index, num):
    while True:
        got, address = self.recvfrom(BATCH_SIZE + 1)
        got_index, got_data = unpack(got)
        print(got_index, index)
        if got_index != index:
            troubled_sendto(self, pack(ACK_STRING.encode('ascii'), index), address)
            continue

        print(f'Got package #{num}.')
        troubled_sendto(self, pack(ACK_STRING.encode('ascii'), (index + 1) % 2), address)
        return got_data


def recv(self):
    to_ret = b''
    num = 0

    while True:
        got = try_recvfrom(self, num % 2, num + 1)
        if got == b'\0':
            break
        to_ret += got
        num += 1

    return to_ret.decode('ascii')
