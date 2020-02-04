from messages.header import _PGW_MSG_HEAD
from define.pgw_define import _MESSAGE_ID
from define.pgw_define import _CALL_TYPE
from messages.ISerializable import ISerializable

class_to_msgid = {msg_id.name: msg_id.value for msg_id in _MESSAGE_ID}


class _MESSAGE(ISerializable):
    def __init__(self, body=None):
        if body is None:
            self.header = ISerializable()
            self.body = ISerializable()
            return
        self.header = _PGW_MSG_HEAD()
        self.header.gw_magic = b'\x47'[0]
        self.header.gw_msgid = class_to_msgid.get(body.__class__.__name__, -1)
        self.header.length = body.GetSize()
        self.body = body

    def GetBytes(self):
        # self.buffer = bytes(self.GetSize())
        return self.header.GetBytes() + self.body.GetBytes()

    def GetSize(self):
        return self.header.GetSize() + self.body.GetSize()


def main():
    from body import _CALL_SETUP_REQ, _CALL_SETUP_RES
    req = _CALL_SETUP_REQ()
    req.Init(_CALL_TYPE._CT_RPC)
    req_msg = _MESSAGE(req)
    print(req_msg.GetBytes())

    res = _CALL_SETUP_RES()
    res.Init(_CALL_TYPE._CT_PRIVATE)
    res.result = 0
    res.reserve2 = 1
    res.s_call_id = 2
    res.r_call_id = 3
    res.media_ip = 4
    res.media_port = 5
    res.PrintDump()

    header = _PGW_MSG_HEAD()
    header.gw_msgid = _MESSAGE_ID._CALL_SETUP_RES.value
    header.length = res.GetSize()

    msg = _MESSAGE()
    msg.body = res
    msg.header = header
    print(msg.GetBytes())
    print(msg.GetSize())

    msg2 = _MESSAGE(res)
    print(msg2.GetBytes())
    print(msg2.GetSize())


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
