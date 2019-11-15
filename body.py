from message import ISerializable
import struct
from define import _CALL_TYPE


# PRIVATE : BBHIIIIH
# GROUP : BBHIIIIH
# EMER : BBHIIIIH
# UDG : BBHIIIHH?s
# ALERT : BBHIII
# RPC : BBHIIIIHH


class _CALL_SETUP_REQ(ISerializable):
    def __init__(self, buf, calltype=None):
        if buf is not None and calltype is not None:    # buf와 calltype 동시는 불가
            return
        if calltype is not None and isinstance(calltype, _CALL_TYPE):
            self.init_fmt(calltype)
            self.init_request(calltype)
            return
        if buf is not None:
            calltype = _CALL_TYPE(buf[0:1][0])  # first bit is CallType
            self.init_fmt(calltype)
            unpacked = struct.unpack(self.struct_fmt, buf[0:self.struct_len])
            self.set_request(calltype, list(unpacked))

            if calltype is _CALL_TYPE.CT_UDG:
                member_list_fmt = str.format('{0}I', self.mem_cnt)
                before_len = self.struct_len
                self.struct_fmt += member_list_fmt
                self.struct_len = struct.calcsize(self.struct_fmt)
                unpacked = struct.unpack(member_list_fmt, buf[before_len: self.struct_len])
                self.mem_list = list(unpacked)
                self.data += self.mem_list

    def init_fmt(self, calltype):
        if calltype == _CALL_TYPE.CT_PRIVATE:
            self.struct_fmt = '!BBHIIIIH'
            self.struct_len = struct.calcsize(self.struct_fmt)
        elif calltype == _CALL_TYPE.CT_GROUP:
            self.struct_fmt = '!BBHIIIIH'
            self.struct_len = struct.calcsize(self.struct_fmt)
        elif calltype == _CALL_TYPE.CT_EMER:
            self.struct_fmt = '!BBHIIIIH'
            self.struct_len = struct.calcsize(self.struct_fmt)
        elif calltype == _CALL_TYPE.CT_UDG:
            self.struct_fmt = '!BBHIIIHH'
            self.struct_len = struct.calcsize(self.struct_fmt)
        elif calltype == _CALL_TYPE.CT_ALERT:
            self.struct_fmt = '!BBHIII'
            self.struct_len = struct.calcsize(self.struct_fmt)
        elif calltype == _CALL_TYPE.CT_RPC:
            self.struct_fmt = '!BBHIIIIHH'
            self.struct_len = struct.calcsize(self.struct_fmt)
        return

    def init_request(self, calltype):
        if calltype is _CALL_TYPE.CT_PRIVATE:
            self.set_request(calltype, [0] * 8)
        elif calltype is _CALL_TYPE.CT_GROUP:
            self.set_request(calltype, [0] * 8)
        elif calltype is _CALL_TYPE.CT_EMER:
            self.set_request(calltype, [0] * 8)
        elif calltype is _CALL_TYPE.CT_UDG:
            self.set_request(calltype, [0] * 8)
        elif calltype is _CALL_TYPE.CT_ALERT:
            self.set_request(calltype, [0] * 6)
        elif calltype is _CALL_TYPE.CT_RPC:
            self.set_request(calltype, [0] * 9)
        return

    def set_request(self, calltype, datas):
        if calltype is _CALL_TYPE.CT_PRIVATE:   # message count = 8
            self.data = datas
            self.call_type = calltype.value     # datas[0]
            self.priority = datas[1]
            self.reserve2 = datas[2]
            self.s_call_id = datas[3]
            self.o_ssid = datas[4]
            self.t_ssid = datas[5]
            self.media_ip = datas[6]
            self.media_port = datas[7]
        elif calltype is _CALL_TYPE.CT_GROUP or calltype is _CALL_TYPE.CT_EMER:   # message count = 8
            self.data = datas
            self.call_type = calltype.value     # datas[0]
            self.priority = datas[1]
            self.reserve2 = datas[2]
            self.s_call_id = datas[3]
            self.o_ssid = datas[4]
            self.bunch_group = datas[5]
            self.media_ip = datas[6]
            self.media_port = datas[7]
        elif calltype is _CALL_TYPE.CT_UDG:     # message count = 8
            self.data = datas
            self.call_type = calltype.value     # datas[0]
            self.priority = datas[1]
            self.reserve2 = datas[2]
            self.s_call_id = datas[3]
            self.o_ssid = datas[4]
            self.media_ip = datas[5]
            self.media_port = datas[6]
            self.mem_cnt = datas[7]
        elif calltype is _CALL_TYPE.CT_ALERT:   # message count = 6
            self.data = datas
            self.call_type = calltype.value
            self.reserve1 = datas[1]
            self.reserve2 = datas[2]
            self.s_call_id = datas[3]
            self.o_ssid = datas[4]
            self.t_ssid = datas[5]
        elif calltype is _CALL_TYPE.CT_RPC:     # message count = 9
            self.data = datas
            self.call_type = calltype.value
            self.reserve1 = datas[1]
            self.reserve2 = datas[2]
            self.s_call_id = datas[3]
            self.o_ssid = datas[4]
            self.t_ssid = datas[5]
            self.media_ip = datas[6]
            self.media_port = datas[7]
            self.rpc_para = datas[8]
        return

    def GetBytes(self):
        if self.data is None:
            return bytes(self.GetSize())
        self.data = [
            self.call_type,
            self.priority,
            self.reserve2,
            self.s_call_id,
            self.o_ssid,
            self.t_ssid,
            self.media_ip,
            self.media_port,
        ]
        return struct.pack(self.struct_fmt, *self.data)

    def GetSize(self):
        self.struct_len = struct.calcsize(self.struct_fmt)
        return self.struct_len


def test_call_setup_req_1():
    call_type = 1
    priority = 2
    reserve2 = 3
    s_call_id = 4
    o_ssid = 5
    t_ssid = 6
    media_ip = 7
    media_port = 8
    buf = struct.pack("!BBHIIIIH", *(
        call_type,
        priority,
        reserve2,
        s_call_id,
        o_ssid,
        t_ssid,
        media_ip,
        media_port
    ))
    call_setup_req = _CALL_SETUP_REQ(buf)
    print(call_setup_req.GetSize())
    print(call_setup_req.GetBytes())


def test_call_setup_req_4():
    call_type = 4
    priority = 2
    reserve2 = 3
    s_call_id = 4
    o_ssid = 5
    media_ip = 7
    media_port = 8
    mem_cnt = 4
    member_1 = 100
    member_2 = 200
    member_3 = 300
    member_4 = 400
    buf = struct.pack("!BBHIIIHH4I", *(
        call_type,
        priority,
        reserve2,
        s_call_id,
        o_ssid,
        media_ip,
        media_port,
        mem_cnt,
        member_1,
        member_2,
        member_3,
        member_4
    ))
    call_setup_req = _CALL_SETUP_REQ(buf)
    print(call_setup_req.GetSize())
    print(call_setup_req.GetBytes())
    print(call_setup_req.data)
    print(call_setup_req.call_type)
    print(call_setup_req.priority)
    print(call_setup_req.reserve2)
    print(call_setup_req.s_call_id)
    print(call_setup_req.o_ssid)
    print(call_setup_req.media_ip)
    print(call_setup_req.media_port)
    print(call_setup_req.mem_cnt)
    print(call_setup_req.mem_list)


def test_call_setup_req_5():
    call_type = 5
    priority = 2
    reserve2 = 3
    s_call_id = 4
    o_ssid = 5
    t_ssid = 6
    buf = struct.pack("!BBHIII", *(
        call_type, priority, reserve2, s_call_id, o_ssid, t_ssid
    ))
    call_setup_req = _CALL_SETUP_REQ(buf)
    print(call_setup_req.GetSize())
    print(call_setup_req.GetBytes())


def test_call_setup_req_make():
    for calltype in _CALL_TYPE:
        req = _CALL_SETUP_REQ(None, calltype)
        print(req.GetSize())
        print(req.GetBytes())


def main():
    test_call_setup_req_make()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
