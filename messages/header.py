from messages.ISerializable import ISerializable
import struct


class _PGW_MSG_HEAD(ISerializable):
    def __init__(self, buf=None):
        self.struct_fmt = '!BBH'
        self.struct_len = struct.calcsize(self.struct_fmt)

        if buf is None:
            self.gw_magic = b'\x47'[0]
            self.gw_msgid = 0
            self.length = 0
            return

        unpacked = struct.unpack(self.struct_fmt, buf)
        self.gw_magic = unpacked[0]
        self.gw_msgid = unpacked[1]
        self.length = unpacked[2]

    def PrintDump(self):
        print('[{0}]'.format(self.__class__.__name__), end=' ')
        print('gw_magic : ', self.gw_magic, end=', ')
        print('gw_msgid : ', self.gw_msgid, end=', ')
        print('length : ', self.length, end=', ')
        print('', end='\n')

    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.gw_magic,
                self.gw_msgid,
                self.length,
            ))

    def GetSize(self):
        return self.struct_len


def test_header_1():
    hBuffer = b'\x47\x01\x00\x10'
    header = _PGW_MSG_HEAD(hBuffer)
    print(header.gw_magic)
    print(header.gw_msgid)
    print(header.length)


def test_header_2():
    header = _PGW_MSG_HEAD(None)
    print(header.gw_magic)
    print(header.gw_msgid)
    print(header.length)


def main():
    test_header_1()
    test_header_2()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
