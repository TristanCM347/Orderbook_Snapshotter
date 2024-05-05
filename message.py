import struct
from typing import BinaryIO


def decode_symbol(encoded: bytes) -> str:
    return encoded.decode().rstrip("\x00")


class Header(object):
    """Contains header information about a message."""

    ENCODING = "<LLc"

    def __init__(self, seq_num: int, msg_size: int, msg_type: str):
        self.seq_num = seq_num
        self.msg_size = msg_size
        self.msg_type = msg_type

    @classmethod
    def unpack(cls, buf: bytes):
        seq_num, msg_size, msg_type = struct.unpack(cls.ENCODING, buf)
        return Header(seq_num, msg_size, msg_type.decode())


class OrderAdd(object):
    """Contains details of an order book add event."""
    
    TYPE = "A"
    ENCODING = "<3sQc3sQi4s"

    def __init__(self, symbol: str, order_id: int, side: str, volume: int, price: int):
        self.symbol = symbol
        self.order_id = order_id
        self.side = side
        self.volume = volume
        self.price = price

    @classmethod
    def unpack(cls, buf: bytes):
        symbol, order_id, side, _, volume, price, _ = struct.unpack(cls.ENCODING, buf)
        return OrderAdd(decode_symbol(symbol), order_id, side.decode(), volume, price)


class OrderUpdate(object):
    """Contains details of an order book update event."""
    
    TYPE = "U"
    ENCODING = "<3sQc3sQi4s"

    def __init__(self, symbol: str, order_id: int, side: str, volume: int, price: int):
        self.symbol = symbol
        self.order_id = order_id
        self.side = side
        self.volume = volume
        self.price = price

    @classmethod
    def unpack(cls, buf: bytes):
        symbol, order_id, side, _, volume, price, _ = struct.unpack(cls.ENCODING, buf)
        return OrderUpdate(decode_symbol(symbol), order_id, side.decode(), volume, price)


class OrderDelete(object):
    """Contains details of an order book delete event."""

    TYPE = "D"
    ENCODING = "<3sQc3s"

    def __init__(self, symbol: str, order_id: int, side: str):
        self.symbol = symbol
        self.order_id = order_id
        self.side = side

    @classmethod
    def unpack(cls, buf: bytes):
        symbol, order_id, side, _ = struct.unpack(cls.ENCODING, buf)
        return OrderDelete(decode_symbol(symbol), order_id, side.decode())


class OrderTraded(object):
    """Contains details of an order being traded."""

    TYPE = "E"
    ENCODING = "<3sQc3sQ"

    def __init__(self, symbol: str, order_id: int, side: str, volume: int):
        self.symbol = symbol
        self.order_id = order_id
        self.side = side
        self.volume = volume

    @classmethod
    def unpack(cls, buf: bytes):
        symbol, order_id, side, _, volume = struct.unpack(cls.ENCODING, buf)
        return OrderTraded(decode_symbol(symbol), order_id, side.decode(), volume)


def gen_from(bin: BinaryIO):
    """
    gen_from is a generator that reads from given buffer untill fully consumed.
    returns a Header and [OrderAdd | OrderUpdate | OrderDelete | OrderTraded]
    """

    header_size = struct.calcsize(Header.ENCODING)

    while True:
        buf = bin.read(header_size)
        if not buf:
            return

        header = Header.unpack(buf)
        buf = bin.read(header.msg_size - 1)
        if len(buf) < (header.msg_size - 1):
            raise Exception(f"Incomplete message size({header.msg_size}) read({len(buf)})")

        if header.msg_type == 'A':
            unpack = OrderAdd.unpack
        elif header.msg_type == 'U':
            unpack = OrderUpdate.unpack
        elif header.msg_type == "D":
            unpack = OrderDelete.unpack
        elif header.msg_type == "E":
            unpack = OrderTraded.unpack
        else:
            raise Exception(f"Unknown header code: {header.msg_type}")

        yield header, unpack(buf)
