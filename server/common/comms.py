from .utils import Bet
from enum import Enum
import socket

MAX_SIZE = 8000
TYPE_SEPARATOR = "|"
BET_FIELD_SEPARATOR = ","


class Type(Enum):
    ACK = 0
    BET = 1


def split_packet(packet: str):
    p_type, bet_raw = packet.split(sep=TYPE_SEPARATOR)
    p_type = Type(int(p_type))

    bet_arr = bet_raw.split(BET_FIELD_SEPARATOR)

    return p_type, bet_arr


def read_bet(file):

    for packet in file:
        packet.strip()
        p_type, bet_arr = split_packet(packet)

        if p_type != Type.BET:
            raise TypeError

        # file.close()
        return Bet.from_list(bet_arr)


def send_ack(client_socket: socket.socket, bet_document, bet_number):
    client_socket.sendall((f"{Type.ACK.value}|{bet_document},{bet_number}\n").encode())
