from message import ISerializable
import struct


class Header(ISerializable):
    def __init__(self, buf):
        self.struct_fmt = '!BBH'
        self.struct_len = struct.calcsize(self.struct_fmt)

        if buf is None:
            self.GW_MAGIC = 0
            self.GW_MSGID = 0
            self.LENGTH = 0
            return

        unpacked = struct.unpack(self.struct_fmt, buf)
        self.GW_MAGIC = unpacked[0]
        self.GW_MSGID = unpacked[1]
        self.LENGTH = unpacked[2]

    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.GW_MAGIC,
                self.GW_MSGID,
                self.LENGTH,
            ))

    def GetSize(self):
        return self.struct_len


def test_header_1():
    hBuffer = b'\x47\x01\x00\x10'
    header = Header(hBuffer)
    print(header.GW_MAGIC)
    print(header.GW_MSGID)
    print(header.LENGTH)


def test_header_2():
    header = Header(None)
    print(header.GW_MAGIC)
    print(header.GW_MSGID)
    print(header.LENGTH)


def main():
    test_header_1()
    test_header_2()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
