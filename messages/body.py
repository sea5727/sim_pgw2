from messages.ISerializable import ISerializable
import struct
import socket
from define.pgw_define import _CALL_TYPE
from pgw2memory import calltype_switcher


__all__ = [
    '_GW_STATUS',
    '_CALL_SETUP_REQ',
    '_CALL_SETUP_RES',
    '_MEDIA_ON_REQ',
    '_MEDIA_ON_RES',
    '_MEDIA_ON_RES',
    '_MEDIA_OFF_REQ',
    '_MEDIA_OFF_RES',
    '_MEDIA_ON_NOTI',
    '_MEDIA_OFF_NOTI',
    '_CALL_LEAVE_REQ',
    '_CALL_LEAVE_RES',
    '_CALL_END_NOTI',
    '_BUNCH_INFO',
    ]

# PRIVATE : BBHIIIIH
# GROUP : BBHIIIIH
# EMER : BBHIIIIH
# UDG : BBHIIIHH?s
# ALERT : BBHIII
# RPC : BBHIIIIHH


class _GW_STATUS(ISerializable):
    """
    This is request message for call reave
    """
    KeepAliveRequest = 1
    KeepAliveResponse = 2
    ChangeState = 3

    Undefined = 0
    ConnectedWithPTALKServer = 1
    DisconnectedWithPTALKServer = 2

    def __init__(self, buf=None):
        if buf is None:
            return
        self.struct_fmt = '!BB'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))
        self.set_msg(self.datas)

    def Init(self):
        self.struct_fmt = '!BB'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = [0] * 2
        self.set_msg(self.datas)
        return self

    def set_msg(self, datas):
        self.cmd = datas[0]
        self.state = datas[1]
        self.message_names = ['cmd', 'state']

    def StringDump(self):
        dump = ''
        dump += '[{0}] '.format(self.__class__.__name__)
        dump += 'cmd : [{0}] '.format(self.cmd)
        dump += 'state : [{0}] '.format(self.state)
        return dump
        
    def PrintDump(self):
        print(self.StringDump())

    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.cmd,
                self.state,
            ))

    def GetSize(self):
        return self.struct_len


class _CALL_SETUP_REQ(ISerializable):
    """
    This is request message for call setup
    """
    def __init__(self, buf=None):
        if buf is None:
            return

        calltype = _CALL_TYPE(buf[0:1][0])  # first bit is CallType
        classname = calltype_switcher.get(calltype.value, lambda: "Invalid CallType")
        getattr(self, classname).init(self, buf)
        getattr(self, classname).set_msg(self, self.datas)

    def Init(self, calltype=None):
        if calltype is None:
            calltype = _CALL_TYPE._CT_PRIVATE.value
        if type(calltype) is _CALL_TYPE:
            calltype = calltype.value
        classname = calltype_switcher.get(calltype, lambda: "Invalid CallType")
        getattr(self, classname).init(self)
        getattr(self, classname).set_msg(self, self.datas)
        return self

    def StringDump(self):
        classname = calltype_switcher.get(self.call_type, lambda: "Invalid CallType")
        return getattr(self, classname).StringDump(self)

    def PrintDump(self):
        classname = calltype_switcher.get(self.call_type, lambda: "Invalid CallType")
        return getattr(self, classname).PrintDump(self)

    def GetBytes(self):
        classname = calltype_switcher.get(self.call_type, lambda: "Invalid CallType")
        return getattr(self, classname).GetBytes(self)

    def GetSize(self):
        classname = calltype_switcher.get(self.call_type, lambda: "Invalid CallType")
        return getattr(self, classname).GetSize(self)

    class _CT_PRIVATE(ISerializable):
        """
        This is inner class of _CALL_SETUP_REQ class for message structure
        """
        def init(self, buf=None):
            self.struct_fmt = '!BBHIIIIH'
            self.struct_len = struct.calcsize(self.struct_fmt)
            if buf is None:
                self.datas = [0] * 8
            else:
                self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))

        def set_msg(self, datas):
            self.call_type = _CALL_TYPE._CT_PRIVATE.value
            self.priority = datas[1]
            self.reserve2 = datas[2]
            self.s_call_id = datas[3]
            self.o_ssid = datas[4]
            self.t_ssid = datas[5]
            self.media_ip = datas[6]
            self.media_port = datas[7]
            self.message_names = [
                'call_type',
                'priority',
                's_call_id',
                'o_ssid',
                't_ssid',
                'media_ip',
                'media_port'
            ]

        def StringDump(self):
            dump = ''
            dump += '[{0}]  '.format(self.__class__.__name__)
            dump += 'call_type : [{0}]  '.format(self.call_type)
            dump += 'priority : [{0}]  '.format(self.priority)
            dump += 'reserve2 : [{0}]  '.format(self.reserve2)
            dump += 's_call_id : [{0}]  '.format(self.s_call_id)
            dump += 'o_ssid : [{0}]  '.format(self.o_ssid)
            dump += 't_ssid : [{0}]  '.format(self.t_ssid)
            dump += 'media_ip : [{0}]  '.format(socket.inet_ntoa(struct.pack('I', self.media_ip)))
            dump += 'media_port : [{0}]  '.format(self.media_port)
            return dump
        
        def PrintDump(self):
            print(self.StringDump())

        def GetBytes(self):
            return struct.pack(
                self.struct_fmt,
                *(
                    self.call_type,
                    self.priority,
                    self.reserve2,
                    self.s_call_id,
                    self.o_ssid,
                    self.t_ssid,
                    self.media_ip,
                    self.media_port,
                ))

        def GetSize(self):
            return self.struct_len

    class _CT_GROUP(ISerializable):
        """
        This is inner class of _CALL_SETUP_REQ class for message structure
        """
        def init(self, buf=None):
            self.struct_fmt = '!BBHIIIIH'
            self.struct_len = struct.calcsize(self.struct_fmt)
            if buf is None:
                self.datas = [0] * 8
            else:
                self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))

        def set_msg(self, datas):
            self.call_type = _CALL_TYPE._CT_GROUP.value
            self.priority = datas[1]
            self.reserve2 = datas[2]
            self.s_call_id = datas[3]
            self.o_ssid = datas[4]
            self.bunch_group = datas[5]
            self.media_ip = datas[6]
            self.media_port = datas[7]
            self.message_names = [
                'call_type',
                'priority',
                's_call_id',
                'o_ssid',
                'bunch_group',
                'media_ip',
                'media_port'
            ]

        def StringDump(self):
            dump = ''
            dump += '[{0}]  '.format(self.__class__.__name__)
            dump += 'call_type : [{0}]  '.format(self.call_type)
            dump += 'priority : [{0}]  '.format(self.priority)
            dump += 'reserve2 : [{0}]  '.format(self.reserve2)
            dump += 's_call_id : [{0}]  '.format(self.s_call_id)
            dump += 'o_ssid : [{0}]  '.format(self.o_ssid)
            dump += 'bunch_group : [{0}]  '.format(self.bunch_group)
            dump += 'media_ip : [{0}]  '.format(socket.inet_ntoa(struct.pack('I', self.media_ip)))
            dump += 'media_port : [{0}]  '.format(self.media_port)
            return dump
            
        def PrintDump(self):
            print(self.StringDump())

        def GetBytes(self):
            return struct.pack(
                self.struct_fmt,
                *(
                    self.call_type,
                    self.priority,
                    self.reserve2,
                    self.s_call_id,
                    self.o_ssid,
                    self.bunch_group,
                    self.media_ip,
                    self.media_port,
                ))

        def GetSize(self):
            return self.struct_len

    class _CT_EMER(ISerializable):
        """
        This is inner class of _CALL_SETUP_REQ class for message structure
        """
        def init(self, buf=None):
            self.struct_fmt = '!BBHIIIIH'
            self.struct_len = struct.calcsize(self.struct_fmt)
            if buf is None:
                self.datas = [0] * 8
            else:
                self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))

        def set_msg(self, datas):
            self.call_type = _CALL_TYPE._CT_EMER.value
            self.priority = datas[1]
            self.reserve2 = datas[2]
            self.s_call_id = datas[3]
            self.o_ssid = datas[4]
            self.bunch_group = datas[5]
            self.media_ip = datas[6]
            self.media_port = datas[7]
            self.message_names = [
                'call_type',
                'priority',
                's_call_id',
                'o_ssid',
                'bunch_group',
                'media_ip',
                'media_port'
            ]

        def StringDump(self):
            dump = ''
            dump += '[{0}] '.format(self.__class__.__name__)
            dump += 'call_type : [{0}] '.format(self.call_type)
            dump += 'priority : [{0}] '.format(self.priority)
            dump += 'reserve2 : [{0}] '.format(self.reserve2)
            dump += 's_call_id : [{0}] '.format(self.s_call_id)
            dump += 'o_ssid : [{0}] '.format(self.o_ssid)
            dump += 'bunch_group : [{0}] '.format(self.bunch_group)
            dump += 'media_ip : [{0}] '.format(socket.inet_ntoa(struct.pack('I', self.media_ip)))
            dump += 'media_port : [{0}] '.format(self.media_port)
            return dump

        def PrintDump(self):
            print(self.StringDump())

        def GetBytes(self):
            return struct.pack(
                self.struct_fmt,
                *(
                    self.call_type,
                    self.priority,
                    self.reserve2,
                    self.s_call_id,
                    self.o_ssid,
                    self.bunch_group,
                    self.media_ip,
                    self.media_port,
                ))

        def GetSize(self):
            return self.struct_len

    class _CT_UDG(ISerializable):
        """
        This is inner class of _CALL_SETUP_REQ class for message structure
        """
        def init(self, buf=None):
            self.struct_fmt = '!BBHIIIHH'
            self.struct_len = struct.calcsize(self.struct_fmt)
            if buf is None:
                self.datas = [0] * 8
                self.datas.append([])
            else:
                self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))
                member_count = self.datas[7]
                if member_count > 0:
                    fmt = str.format('{0}I', member_count)
                    fmt_size = struct.calcsize(fmt)
                    mem_list = list(struct.unpack('!' + fmt, buf[self.struct_len: self.struct_len + fmt_size]))
                    self.datas.append(mem_list)
                    self.struct_fmt += fmt
                    self.struct_len = struct.calcsize(self.struct_fmt)
                else:
                    self.datas.append([])

        def set_msg(self, datas):
            self.call_type = _CALL_TYPE._CT_UDG.value
            self.priority = datas[1]
            self.reserve2 = datas[2]
            self.s_call_id = datas[3]
            self.o_ssid = datas[4]
            self.media_ip = datas[5]
            self.media_port = datas[6]
            self.mem_cnt = datas[7]
            self.mem_list = datas[8]
            self.message_names = [
                'call_type',
                'priority',
                's_call_id',
                'o_ssid',
                'bunch_group',
                'media_ip',
                'media_port',
                'mem_cnt',
                'mem_list',
            ]

        def StringDump(self):
            dump = ''
            dump += '[{0}] '.format(self.__class__.__name__)
            dump += 'call_type : [{0}] '.format(self.call_type)
            dump += 'priority : [{0}] '.format(self.priority)
            dump += 'reserve2 : [{0}] '.format(self.reserve2)
            dump += 's_call_id : [{0}] '.format(self.s_call_id)
            dump += 'o_ssid : [{0}] '.format(self.o_ssid)
            dump += 'media_ip : [{0}] '.format(socket.inet_ntoa(struct.pack('I', self.media_ip)))
            dump += 'media_port : [{0}] '.format(self.media_port)
            dump += 'mem_cnt : [{0}] '.format(self.mem_cnt)
            dump += 'mem_list : [{0}] '.format(self.mem_list)
            return dump

        def PrintDump(self):
            print(self.StringDump())

        def GetBytes(self):
            if self.mem_cnt > 0:
                self.struct_fmt = str.format('!BBHIIIHH{0}I', self.mem_cnt)
            return struct.pack(
                self.struct_fmt,
                *(
                    self.call_type,
                    self.priority,
                    self.reserve2,
                    self.s_call_id,
                    self.o_ssid,
                    self.media_ip,
                    self.media_port,
                    self.mem_cnt,
                    *self.mem_list
                ))

        def GetSize(self):
            if self.mem_cnt > 0:
                self.struct_fmt = str.format('!BBHIIIHH{0}I', self.mem_cnt)
            self.struct_len = struct.calcsize(self.struct_fmt)
            return self.struct_len

    class _CT_ALERT(ISerializable):
        """
        This is inner class of _CALL_SETUP_REQ class for message structure
        """
        def init(self, buf=None):
            self.struct_fmt = '!BBHIII'
            self.struct_len = struct.calcsize(self.struct_fmt)
            if buf is None:
                self.datas = [0] * 6
            else:
                self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))

        def set_msg(self, datas):
            self.call_type = _CALL_TYPE._CT_ALERT.value
            self.reserve1 = datas[1]
            self.reserve2 = datas[2]
            self.s_call_id = datas[3]
            self.o_ssid = datas[4]
            self.t_ssid = datas[5]
            self.message_names = [
                'call_type',
                's_call_id',
                'o_ssid',
                't_ssid',
            ]

        def StringDump(self):
            dump = ''
            dump += '[{0}] '.format(self.__class__.__name__)
            dump += 'call_type : [{0}] '.format(self.call_type)
            dump += 'reserve1 : [{0}] '.format(self.reserve1)
            dump += 'reserve2 : [{0}] '.format(self.reserve2)
            dump += 's_call_id : [{0}] '.format(self.s_call_id)
            dump += 'o_ssid : [{0}] '.format(self.o_ssid)
            dump += 't_ssid : [{0}] '.format(self.t_ssid)
            return dump

        def PrintDump(self):
            print(self.StringDump())

        def GetBytes(self):
            return struct.pack(
                self.struct_fmt,
                *(
                    self.call_type,
                    self.reserve1,
                    self.reserve2,
                    self.s_call_id,
                    self.o_ssid,
                    self.t_ssid,
                ))

        def GetSize(self):
            return self.struct_len

    class _CT_RPC(ISerializable):
        """
        This is inner class of _CALL_SETUP_REQ class for message structure
        """
        def init(self, buf=None):
            self.struct_fmt = '!BBHIIIIHH'
            self.struct_len = struct.calcsize(self.struct_fmt)
            if buf is None:
                self.datas = [0] * 9
            else:
                self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))

        def set_msg(self, datas):
            self.call_type = _CALL_TYPE._CT_RPC.value
            self.reserve1 = datas[1]
            self.reserve2 = datas[2]
            self.s_call_id = datas[3]
            self.o_ssid = datas[4]
            self.t_ssid = datas[5]
            self.media_ip = datas[6]
            self.media_port = datas[7]
            self.rpc_para = datas[8]
            self.message_names = [
                'call_type',
                's_call_id',
                'o_ssid',
                't_ssid',
                'media_ip',
                'media_port',
                'rpc_para',
            ]

        def StringDump(self):
            dump = ''
            dump += '[{0}] '.format(self.__class__.__name__)
            dump += 'call_type : [{0}] '.format(self.call_type)
            dump += 'reserve1 : [{0}] '.format(self.reserve1)
            dump += 'reserve2 : [{0}] '.format(self.reserve2)
            dump += 's_call_id : [{0}] '.format(self.s_call_id)
            dump += 'o_ssid : [{0}] '.format(self.o_ssid)
            dump += 't_ssid : [{0}] '.format(self.t_ssid)
            dump += 'media_ip : [{0}] '.format(socket.inet_ntoa(struct.pack('I', self.media_ip)))
            dump += 'media_port : [{0}] '.format(self.media_port)
            dump += 'rpc_para : [{0}] '.format(self.rpc_para)
            return dump

        def PrintDump(self):
            print(self.StringDump())

        def GetBytes(self):
            return struct.pack(
                self.struct_fmt,
                *(
                    self.call_type,
                    self.reserve1,
                    self.reserve2,
                    self.s_call_id,
                    self.o_ssid,
                    self.t_ssid,
                    self.media_ip,
                    self.media_port,
                    self.rpc_para,
                ))

        def GetSize(self):
            return self.struct_len


class _CALL_SETUP_RES(ISerializable):
    """
    This is response message for call setup
    """
    def __init__(self, buf=None):
        if buf is None:
            return

        calltype = _CALL_TYPE(buf[0:1][0])  # first bit is CallType
        classname = calltype_switcher.get(calltype.value, lambda: "Invalid CallType")
        getattr(self, classname).init(self, buf)
        getattr(self, classname).set_msg(self, self.datas)

    def Init(self, calltype=None):
        if calltype is None:
            calltype = _CALL_TYPE._CT_PRIVATE.value
        if type(calltype) is _CALL_TYPE:
            calltype = calltype.value
        classname = calltype_switcher.get(calltype, lambda: "Invalid CallType")
        getattr(self, classname).init(self)
        getattr(self, classname).set_msg(self, self.datas)
        # self._CT_COMMON.init(self)
        # self._CT_COMMON.set_msg(self, self.datas)
        return self

    def StringDump(self):
        classname = calltype_switcher.get(self.call_type, lambda: "Invalid CallType")
        return getattr(self, classname).StringDump(self)

    def PrintDump(self):
        classname = calltype_switcher.get(self.call_type, lambda: "Invalid CallType")
        getattr(self, classname).PrintDump(self)

    def GetBytes(self):
        classname = calltype_switcher.get(self.call_type, lambda: "Invalid CallType")
        return getattr(self, classname).GetBytes(self)

    def GetSize(self):
        classname = calltype_switcher.get(self.call_type, lambda: "Invalid CallType")
        return getattr(self, classname).GetSize(self)

    class _CT_COMMON(ISerializable):
        """
        This is inner class of _CALL_SETUP_RES class for message structure
        """
        def init(self, buf=None):
            self.struct_fmt = '!BBHIIIH'
            self.struct_len = struct.calcsize(self.struct_fmt)
            if buf is None:
                self.datas = [0] * 7
            else:
                self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))

        def set_msg(self, datas):
            # self.call_type = datas[0]
            self.result = datas[1]
            self.reserve2 = datas[2]
            self.s_call_id = datas[3]
            self.r_call_id = datas[4]
            self.media_ip = datas[5]
            self.media_port = datas[6]
            self.message_names = [
                'call_type',
                'result',
                's_call_id',
                'r_call_id',
                'media_ip',
                'media_port',
            ]

        def StringDump(self):
            dump = ''
            dump += '[{0}] '.format(self.__class__.__name__)
            dump += 'call_type : [{0}] '.format(self.call_type)
            dump += 'result : [{0}] '.format(self.result)
            dump += 'reserve2 : [{0}] '.format(self.reserve2)
            dump += 's_call_id : [{0}] '.format(self.s_call_id)
            dump += 'r_call_id : [{0}] '.format(self.r_call_id)
            dump += 'media_ip : [{0}] '.format(socket.inet_ntoa(struct.pack('I', self.media_ip)))
            dump += 'media_port : [{0}] '.format(self.media_port)
            return dump

        def PrintDump(self):
            print(self.StringDump())

        def GetBytes(self):
            return struct.pack(
                self.struct_fmt,
                *(
                    self.call_type,
                    self.result,
                    self.reserve2,
                    self.s_call_id,
                    self.r_call_id,
                    self.media_ip,
                    self.media_port,
                ))

        def GetSize(self):
            return self.struct_len

    class _CT_PRIVATE(_CT_COMMON):
        def set_msg(self, datas):
            self.call_type = _CALL_TYPE._CT_PRIVATE.value
            self._CT_COMMON.set_msg(self, datas)

    class _CT_GROUP(_CT_COMMON):
        def set_msg(self, datas):
            self.call_type = _CALL_TYPE._CT_GROUP.value
            self._CT_COMMON.set_msg(self, datas)

    class _CT_EMER(_CT_COMMON):
        def set_msg(self, datas):
            self.call_type = _CALL_TYPE._CT_EMER.value
            self._CT_COMMON.set_msg(self, datas)

    class _CT_UDG(_CT_COMMON):
        def set_msg(self, datas):
            self.call_type = _CALL_TYPE._CT_UDG.value
            self._CT_COMMON.set_msg(self, datas)

    class _CT_ALERT(_CT_COMMON):
        def set_msg(self, datas):
            self.call_type = _CALL_TYPE._CT_ALERT.value
            self._CT_COMMON.set_msg(self, datas)

    class _CT_RPC(ISerializable):
        """
        This is inner class of _CALL_SETUP_RES class for message structure
        """
        def init(self, buf=None):
            self.struct_fmt = '!BBHIIIHI'
            self.struct_len = struct.calcsize(self.struct_fmt)
            if buf is None:
                self.datas = [0] * 8
            else:
                self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))

        def set_msg(self, datas):
            self.call_type = _CALL_TYPE._CT_RPC.value
            self.result = datas[1]
            self.reserve2 = datas[2]
            self.s_call_id = datas[3]
            self.r_call_id = datas[4]
            self.media_ip = datas[5]
            self.media_port = datas[6]
            self.v_rate = datas[7]
            self.message_names = [
                'call_type',
                'result',
                's_call_id',
                'r_call_id',
                'media_ip',
                'media_port',
                'v_rate',
            ]

        def StringDump(self):
            dump = ''
            dump += '[{0}] '.format(self.__class__.__name__)
            dump += 'call_type : [{0}] '.format(self.call_type)
            dump += 'result : [{0}] '.format(self.result)
            dump += 'reserve2 : [{0}] '.format(self.reserve2)
            dump += 's_call_id : [{0}] '.format(self.s_call_id)
            dump += 'r_call_id : [{0}] '.format(self.r_call_id)
            dump += 'media_ip : [{0}] '.format(socket.inet_ntoa(struct.pack('I', self.media_ip)))
            dump += 'media_port : [{0}] '.format(self.media_port)
            dump += 'v_rate : [{0}] '.format(self.v_rate)
            return dump

        def PrintDump(self):
            print(self.StringDump())

        def GetBytes(self):
            return struct.pack(
                self.struct_fmt,
                *(
                    self.call_type,
                    self.result,
                    self.reserve2,
                    self.s_call_id,
                    self.r_call_id,
                    self.media_ip,
                    self.media_port,
                    self.v_rate,
                ))

        def GetSize(self):
            return self.struct_len


class _MEDIA_ON_REQ(ISerializable):
    """
    This is request message for media on
    """
    def __init__(self, buf=None):
        if buf is None:
            return
        self.struct_fmt = '!BBHII'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))
        self.set_msg(self.datas)

    def Init(self, calltype=None):
        if calltype is None:
            calltype = _CALL_TYPE._CT_PRIVATE.value
        if type(calltype) is _CALL_TYPE:
            calltype = calltype.value
        self.struct_fmt = '!BBHII'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = [0] * 5
        self.set_msg([calltype] + self.datas)
        return self

    def set_msg(self, datas):
        self.call_type = datas[0]
        self.o_priority = datas[1]
        self.reserve2 = datas[2]
        self.r_call_id = datas[3]
        self.o_ssid = datas[4]
        self.message_names = [
            'call_type',
            'o_priority',
            'r_call_id',
            'o_ssid',
        ]

    def StringDump(self):
        dump = ''
        dump += '[{0}] '.format(self.__class__.__name__)
        dump += 'call_type : [{0}] '.format(self.call_type)
        dump += 'o_priority : [{0}] '.format(self.o_priority)
        dump += 'reserve2 : [{0}] '.format(self.reserve2)
        dump += 'r_call_id : [{0}] '.format(self.r_call_id)
        dump += 'o_ssid : [{0}] '.format(self.o_ssid)
        return dump

    def PrintDump(self):
        print(self.StringDump())

    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.call_type,
                self.o_priority,
                self.reserve2,
                self.r_call_id,
                self.o_ssid,
            ))

    def GetSize(self):
        return self.struct_len


class _MEDIA_ON_RES(ISerializable):
    """
    This is response message for media on
    """
    def __init__(self, buf=None):
        if buf is None:
            return
        self.struct_fmt = '!BBHII'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))
        self.set_msg(self.datas)

    def Init(self, calltype=None):
        if calltype is None:
            calltype = _CALL_TYPE._CT_PRIVATE.value
        if type(calltype) is _CALL_TYPE:
            calltype = calltype.value
        self.struct_fmt = '!BBHII'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = [0] * 5
        self.set_msg([calltype] + self.datas)
        return self

    def set_msg(self, datas):
        self.call_type = datas[0]
        self.result = datas[1]
        self.reserve2 = datas[2]
        self.r_call_id = datas[3]
        self.o_ssid = datas[4]
        self.message_names = [
            'call_type',
            'result',
            'r_call_id',
            'o_ssid',
        ]

    def StringDump(self):
        dump = ''
        dump += '[{0}] '.format(self.__class__.__name__)
        dump += 'call_type : [{0}] '.format(self.call_type)
        dump += 'result : [{0}] '.format(self.result)
        dump += 'reserve2 : [{0}] '.format(self.reserve2)
        dump += 'r_call_id : [{0}] '.format(self.r_call_id)
        dump += 'o_ssid : [{0}] '.format(self.o_ssid)
        return dump

    def PrintDump(self):
        print(self.StringDump())

    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.call_type,
                self.result,
                self.reserve2,
                self.r_call_id,
                self.o_ssid,
            ))

    def GetSize(self):
        return self.struct_len


class _MEDIA_OFF_REQ(ISerializable):
    """
    This is request message for media off
    """
    def __init__(self, buf=None):
        if buf is None:
            return
        self.struct_fmt = '!BBHI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))
        self.set_msg(self.datas)

    def Init(self, calltype=None):
        if calltype is None:
            calltype = _CALL_TYPE._CT_PRIVATE.value
        if type(calltype) is _CALL_TYPE:
            calltype = calltype.value
        self.struct_fmt = '!BBHI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = [0] * 4
        self.set_msg([calltype] + self.datas)
        return self

    def set_msg(self, datas):
        self.call_type = datas[0]
        self.reserve1 = datas[1]
        self.reserve2 = datas[2]
        self.r_call_id = datas[3]
        self.message_names = [
            'call_type',
            'r_call_id',
        ]

    def StringDump(self):
        dump = ''
        dump += '[{0}] '.format(self.__class__.__name__)
        dump += 'call_type : [{0}] '.format(self.call_type)
        dump += 'reserve1 : [{0}] '.format(self.reserve1)
        dump += 'reserve2 : [{0}] '.format(self.reserve2)
        dump += 'r_call_id : [{0}] '.format(self.r_call_id)
        return dump
        
    def PrintDump(self):
        print(self.StringDump())

    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.call_type,
                self.reserve1,
                self.reserve2,
                self.r_call_id,
            ))

    def GetSize(self):
        return self.struct_len


class _MEDIA_OFF_RES(ISerializable):
    """
    This is response message for media off
    """
    def __init__(self, buf=None):
        if buf is None:
            return
        self.struct_fmt = '!BBHI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))
        self.set_msg(self.datas)

    def Init(self, calltype=None):
        if calltype is None:
            calltype = _CALL_TYPE._CT_PRIVATE.value
        if type(calltype) is _CALL_TYPE:
            calltype = calltype.value
        self.struct_fmt = '!BBHI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = [0] * 4
        self.set_msg([calltype] + self.datas)
        return self

    def set_msg(self, datas):
        self.call_type = datas[0]
        self.result = datas[1]
        self.reserve2 = datas[2]
        self.r_call_id = datas[3]
        self.message_names = [
            'call_type',
            'reseult',
            'r_call_id',
        ]

    def StringDump(self):
        dump = ''
        dump += '[{0}] '.format(self.__class__.__name__)
        dump += 'call_type : [{0}] '.format(self.call_type)
        dump += 'result : [{0}] '.format(self.result)
        dump += 'reserve2 : [{0}] '.format(self.reserve2)
        dump += 'r_call_id : [{0}] '.format(self.r_call_id)
        return dump

    def PrintDump(self):
        print(self.StringDump())

    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.call_type,
                self.result,
                self.reserve2,
                self.r_call_id,
            ))

    def GetSize(self):
        return self.struct_len


class _MEDIA_ON_NOTI(ISerializable):
    """
    This is report message for media on
    """
    def __init__(self, buf=None):
        if buf is None:
            return
        self.struct_fmt = '!BBHII'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))
        self.set_msg(self.datas)

    def Init(self, calltype=None):
        if calltype is None:
            calltype = _CALL_TYPE._CT_PRIVATE.value
        if type(calltype) is _CALL_TYPE:
            calltype = calltype.value
        self.struct_fmt = '!BBHII'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = [0] * 5
        self.set_msg([calltype] + self.datas)
        return self

    def set_msg(self, datas):
        self.call_type = datas[0]
        self.reserve1 = datas[1]
        self.reserve2 = datas[2]
        self.r_call_id = datas[3]
        self.o_ssid = datas[4]
        self.message_names = [
            'call_type',
            'reseult',
            'r_call_id',
            'o_ssid',
        ]

    def StringDump(self):
        dump = ''
        dump += '[{0}] '.format(self.__class__.__name__)
        dump += 'call_type : [{0}] '.format(self.call_type)
        dump += 'reserve1 : [{0}] '.format(self.reserve1)
        dump += 'reserve2 : [{0}] '.format(self.reserve2)
        dump += 'r_call_id : [{0}] '.format(self.r_call_id)
        dump += 'o_ssid : [{0}] '.format(self.o_ssid)
        return dump

    def PrintDump(self):
        print(self.StringDump())

    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.call_type,
                self.reserve1,
                self.reserve2,
                self.r_call_id,
                self.o_ssid,
            ))

    def GetSize(self):
        return self.struct_len


class _MEDIA_OFF_NOTI(ISerializable):
    """
    This is report message for media off
    """
    def __init__(self, buf=None):
        if buf is None:
            return
        self.struct_fmt = '!BBHI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))
        self.set_msg(self.datas)

    def Init(self, calltype=None):
        if calltype is None:
            calltype = _CALL_TYPE._CT_PRIVATE.value
        if type(calltype) is _CALL_TYPE:
            calltype = calltype.value
        self.struct_fmt = '!BBHI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = [0] * 4
        self.set_msg([calltype] + self.datas)
        return self

    def set_msg(self, datas):
        self.call_type = datas[0]
        self.reason = datas[1]
        self.reserve2 = datas[2]
        self.r_call_id = datas[3]
        self.message_names = [
            'call_type',
            'reason',
            'r_call_id',
        ]

    def StringDump(self):
        dump = ''
        dump += '[{0}] '.format(self.__class__.__name__)
        dump += 'call_type : [{0}] '.format(self.call_type)
        dump += 'reason : [{0}] '.format(self.reason)
        dump += 'reserve2 : [{0}] '.format(self.reserve2)
        dump += 'r_call_id : [{0}] '.format(self.r_call_id)
        return dump

    def PrintDump(self):
        print(self.StringDump())

    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.call_type,
                self.reason,
                self.reserve2,
                self.r_call_id,
            ))

    def GetSize(self):
        return self.struct_len


class _CALL_LEAVE_REQ(ISerializable):
    """
    This is request message for call reave
    """
    def __init__(self, buf=None):
        if buf is None:
            return
        self.struct_fmt = '!BBHI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))
        self.set_msg(self.datas)

    def Init(self, calltype=None):
        if calltype is None:
            calltype = _CALL_TYPE._CT_PRIVATE.value
        if type(calltype) is _CALL_TYPE:
            calltype = calltype.value
        self.struct_fmt = '!BBHI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = [0] * 4
        self.set_msg([calltype] + self.datas)
        return self

    def set_msg(self, datas):
        self.call_type = datas[0]
        self.reserve1 = datas[1]
        self.reserve2 = datas[2]
        self.r_call_id = datas[3]
        self.message_names = [
            'call_type',
            'r_call_id',
        ]

    def StringDump(self):
        dump = ''
        dump += '[{0}] '.format(self.__class__.__name__)
        dump += 'call_type : [{0}] '.format(self.call_type)
        dump += 'reserve1 : [{0}] '.format(self.reserve1)
        dump += 'reserve2 : [{0}] '.format(self.reserve2)
        dump += 'r_call_id : [{0}] '.format(self.r_call_id)
        return dump

    def PrintDump(self):
        print(self.StringDump())

    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.call_type,
                self.reserve1,
                self.reserve2,
                self.r_call_id,
            ))

    def GetSize(self):
        return self.struct_len


class _CALL_LEAVE_RES(ISerializable):
    """
    This is response message for call reave
    """
    def __init__(self, buf=None):
        if buf is None:
            return
        self.struct_fmt = '!BBHI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))
        self.set_msg(self.datas)

    def Init(self, calltype=None):
        if calltype is None:
            calltype = _CALL_TYPE._CT_PRIVATE.value
        if type(calltype) is _CALL_TYPE:
            calltype = calltype.value
        self.struct_fmt = '!BBHI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = [0] * 4
        self.set_msg([calltype] + self.datas)
        return self

    def set_msg(self, datas):
        self.call_type = datas[0]
        self.result = datas[1]
        self.reserve2 = datas[2]
        self.r_call_id = datas[3]
        self.message_names = [
            'call_type',
            'reseult',
            'r_call_id',
        ]

    def StringDump(self):
        dump = ''
        dump += '[{0}] '.format(self.__class__.__name__)
        dump += 'call_type : [{0}] '.format(self.call_type)
        dump += 'result : [{0}] '.format(self.result)
        dump += 'reserve2 : [{0}] '.format(self.reserve2)
        dump += 'r_call_id : [{0}] '.format(self.r_call_id)
        return dump

    def PrintDump(self):
        print(self.StringDump())

    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.call_type,
                self.result,
                self.reserve2,
                self.r_call_id,
            ))

    def GetSize(self):
        return self.struct_len


class _CALL_END_NOTI(ISerializable):
    """
    This is request message for call reave
    """
    def __init__(self, buf=None):
        if buf is None:
            return
        self.struct_fmt = '!BBHI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))
        self.set_msg(self.datas)

    def Init(self, calltype=None):
        if calltype is None:
            calltype = _CALL_TYPE._CT_PRIVATE.value
        if type(calltype) is _CALL_TYPE:
            calltype = calltype.value
        self.struct_fmt = '!BBHI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = [0] * 4
        self.set_msg([calltype] + self.datas)
        return self

    def set_msg(self, datas):
        self.call_type = datas[0]
        self.reason = datas[1]
        self.reserve2 = datas[2]
        self.r_call_id = datas[3]
        self.message_names = [
            'call_type',
            'reason',
            'r_call_id',
        ]

    def StringDump(self):
        dump = ''
        dump += '[{0}] '.format(self.__class__.__name__)
        dump += 'call_type : [{0}] '.format(self.call_type)
        dump += 'reason : [{0}] '.format(self.reason)
        dump += 'reserve2 : [{0}] '.format(self.reserve2)
        dump += 'r_call_id : [{0}] '.format(self.r_call_id)
        return dump

    def PrintDump(self):
        print(self.StringDump())

    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.call_type,
                self.reason,
                self.reserve2,
                self.r_call_id,
            ))

    def GetSize(self):
        return self.struct_len


class _BUNCH_INFO(ISerializable):
    """
    This is Bunch Info message
    """
    def __init__(self, buf=None):
        if buf is None:
            return
        self.struct_fmt = '!BBH'
        self.struct_len = struct.calcsize(self.struct_fmt)
        if buf is None:
            self.datas = [0] * 3
            self.datas.append([])
            self.set_msg(self.datas)
        else:
            self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))
            bunch_cnt = self.datas[2]
            if bunch_cnt > 0:
                fmt = str.format('{0}I', bunch_cnt)
                fmt_size = struct.calcsize(fmt)
                bunch_list = list(struct.unpack('!' + fmt, buf[self.struct_len: self.struct_len + fmt_size]))
                self.datas.append(bunch_list)
                self.struct_fmt += fmt
                self.struct_len = struct.calcsize(self.struct_fmt)
            else:
                self.datas.append([])
            self.set_msg(self.datas)

    def Init(self):
        self.struct_fmt = '!BBH'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = [0] * 4
        self.set_msg(self.datas)
        return self

    def set_msg(self, datas):
        self.cmd = datas[0]
        self.reserve1 = datas[1]
        self.counter = datas[2]
        self.bunch = datas[3]
        self.message_names = [
            'cmd'
            'counter',
            'bunch',
        ]

    def StringDump(self):
        dump = ''
        dump += '[{0}] '.format(self.__class__.__name__)
        dump += 'cmd : [{0}] '.format(self.cmd)
        dump += 'reserve1 : [{0}] '.format(self.reserve1)
        dump += 'counter : [{0}] '.format(self.counter)
        dump += 'bunch : [{0}] '.format(self.bunch)
        return dump

    def PrintDump(self):
        print(self.StringDump())

    def GetBytes(self):
        if self.counter > 0:
            self.struct_fmt = str.format('!BBH{0}I', self.counter)
        return struct.pack(
            self.struct_fmt,
            *(
                self.cmd,
                self.reserve1,
                self.counter,
                *(self.bunch),
            ))

    def GetSize(self):
        if self.counter > 0:
            self.struct_fmt = str.format('!BBH{0}I', self.counter)
        self.struct_len = struct.calcsize(self.struct_fmt)
        return self.struct_len


class _CALL_AUDIT_REQ(ISerializable):
    """
    This is request message for call reave
    """
    def __init__(self, buf=None):
        if buf is None:
            return
        self.struct_fmt = '!BI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))
        self.set_msg(self.datas)

    def Init(self, calltype=None):
        if calltype is None:
            calltype = _CALL_TYPE._CT_PRIVATE.value
        if type(calltype) is _CALL_TYPE:
            calltype = calltype.value
        self.struct_fmt = '!BI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = [0] * 2
        self.set_msg([calltype] + self.datas)
        return self

    def set_msg(self, datas):
        self.call_type = datas[0]
        self.r_call_id = datas[1]
        self.message_names = [
            'call_type',
            'r_call_id',
        ]

    def StringDump(self):
        dump = ''
        dump += '[{0}] '.format(self.__class__.__name__)
        dump += 'call_type : [{0}] '.format(self.call_type)
        dump += 'r_call_id : [{0}] '.format(self.r_call_id)
        return dump

    def PrintDump(self):
        print(self.StringDump())

    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.call_type,
                self.r_call_id,
            ))

    def GetSize(self):
        return self.struct_len


class _CALL_AUDIT_RES(ISerializable):
    """
    This is request message for call reave
    """
    def __init__(self, buf=None):
        if buf is None:
            return
        self.struct_fmt = '!BIBI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = list(struct.unpack(self.struct_fmt, buf[0:self.struct_len]))
        self.set_msg(self.datas)

    def Init(self, calltype=None):
        if calltype is None:
            calltype = _CALL_TYPE._CT_PRIVATE.value
        if type(calltype) is _CALL_TYPE:
            calltype = calltype.value
        self.struct_fmt = '!BIBI'
        self.struct_len = struct.calcsize(self.struct_fmt)
        self.datas = [0] * 4
        self.set_msg([calltype] + self.datas)
        return self

    def set_msg(self, datas):
        self.call_type = datas[0]
        self.r_call_id = datas[1]
        self.result = datas[2]
        self.expire_time = datas[3]
        self.message_names = [
            'call_type',
            'r_call_id',
            'result',
            'expire_time',
        ]

    def StringDump(self):
        dump = ''
        dump += '[{0}] '.format(self.__class__.__name__)
        dump += 'call_type : [{0}] '.format(self.call_type)
        dump += 'r_call_id : [{0}] '.format(self.r_call_id)
        dump += 'result : [{0}] '.format(self.result)
        dump += 'expire_time : [{0}] '.format(self.expire_time)
        return dump

    def PrintDump(self):
        print(self.StringDump())

    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.call_type,
                self.r_call_id,
                self.result,
                self.expire_time,
            ))

    def GetSize(self):
        return self.struct_len


def test_call_setup_res_1():
    call_type = _CALL_TYPE._CT_PRIVATE.value
    result = 2
    reserve2 = 3
    s_call_id = 4
    r_call_id = 5
    media_ip = 6
    media_port = 7
    buf = struct.pack("!BBHIIIH", *(
        call_type,
        result,
        reserve2,
        s_call_id,
        r_call_id,
        media_ip,
        media_port
    ))
    call_setup_res = _CALL_SETUP_RES(buf)
    print(call_setup_res.GetSize())
    print(call_setup_res.GetBytes())


def test_call_setup_res_2():
    call_type = _CALL_TYPE._CT_RPC.value
    result = 2
    reserve2 = 3
    s_call_id = 4
    r_call_id = 5
    media_ip = 6
    media_port = 7
    v_rate = 8
    buf = struct.pack("!BBHIIIHI", *(
        call_type,
        result,
        reserve2,
        s_call_id,
        r_call_id,
        media_ip,
        media_port,
        v_rate,
    ))
    call_setup_res = _CALL_SETUP_RES(buf)
    print(call_setup_res.GetSize())
    print(call_setup_res.GetBytes())


def test_media_on_noti():
    call_type = _CALL_TYPE._CT_PRIVATE.value
    reserve1 = 2
    reserve2 = 3
    r_call_id = 4
    o_ssid = 5
    buf = struct.pack("!BBHII", *(
        call_type,
        reserve1,
        reserve2,
        r_call_id,
        o_ssid,
    ))
    media_on_noti = _MEDIA_ON_NOTI(buf)
    print(media_on_noti.GetSize())
    print(media_on_noti.GetBytes())


def test_media_on_noti_make():
    media_on_noti = _MEDIA_ON_NOTI(None)
    print(media_on_noti.GetSize())
    print(media_on_noti.GetBytes())


def test_call_setup_res_make():
    for calltype in _CALL_TYPE:
        res = _CALL_SETUP_RES(None, calltype)
        print(res.GetSize())
        print(res.GetBytes())


def make_call_setup_req():
    # None 으로 생성
    print("####### START _CALL_SETUP_REQ_TEST [ None 으로 생성 시작]#######")

    for calltype in _CALL_TYPE:
        req = _CALL_SETUP_REQ()
        req.Init(calltype)
        req.PrintDump()
        print(req.GetSize())
        print(req.GetBytes())

    print("####### END _CALL_SETUP_REQ_TEST [ None 으로 생성 종료 ]#######")

    # buf 로 생성
    print("####### START _CALL_SETUP_REQ_TEST [ Buf 로 생성 시작]#######")

    for calltype in _CALL_TYPE:
        if calltype is _CALL_TYPE._CT_PRIVATE:
            buf = get_buffer_call_setup_req_private()
        if calltype is _CALL_TYPE._CT_GROUP:
            buf = get_buffer_call_setup_req_group()
        if calltype is _CALL_TYPE._CT_EMER:
            buf = get_buffer_call_setup_req_emer()
        if calltype is _CALL_TYPE._CT_UDG:
            buf = get_buffer_call_setup_req_udg()
        if calltype is _CALL_TYPE._CT_ALERT:
            buf = get_buffer_call_setup_req_alert()
        if calltype is _CALL_TYPE._CT_RPC:
            buf = get_buffer_call_setup_req_rpc()

        req = _CALL_SETUP_REQ(buf)
        req.PrintDump()
        print(req.GetSize())
        print(req.GetBytes())

    print("####### END _CALL_SETUP_REQ_TEST [ Buf 생성 종료 ]#######")


def make_call_setup_res():
    print("####### START _CALL_SETUP_RES_TEST [ None 으로 생성 시작]#######")
    for calltype in _CALL_TYPE:
        res = _CALL_SETUP_RES()     # None 으로 생성
        res.Init(calltype)
        res.PrintDump()
        print(res.GetSize())
        print(res.GetBytes())
    print("####### END _CALL_SETUP_RES_TEST [ None 으로 생성 종료 ]#######")

    print("####### START _CALL_SETUP_RES_TEST [ None 으로 생성 시작]#######")
    for calltype in _CALL_TYPE:
        if calltype is _CALL_TYPE._CT_RPC:
            buf = get_buffer_call_setup_res_rpc(calltype)
        else:
            buf = get_buffer_call_setup_res_common(calltype)
        res = _CALL_SETUP_RES(buf)     # buffer로 생성
        res.Init(calltype)
        res.PrintDump()
        print(res.GetSize())
        print(res.GetBytes())

    print("####### END _CALL_SETUP_RES_TEST [ None 으로 생성 종료 ]#######")


def make_media_on_off_noti():
    print("####### START _MEDIA_ON_NOTI [ None 으로 생성 시작]#######")
    for calltype in _CALL_TYPE:
        noti = _MEDIA_ON_NOTI()     # None 으로 생성
        noti.Init(calltype)
        noti.PrintDump()
        print(noti.GetSize())
        print(noti.GetBytes())
    print("####### START _MEDIA_ON_NOTI [ None 으로 생성 종료]#######")

    print("####### START _MEDIA_ON_NOTI [ Buf 으로 생성 시작]#######")

    for calltype in _CALL_TYPE:
        call_type = calltype.value
        reserve1 = 1
        reserve2 = 2
        r_call_id = 3
        o_ssid = 4

        buf = struct.pack("!BBHII", call_type, reserve1, reserve2, r_call_id, o_ssid)

        noti = _MEDIA_ON_NOTI(buf)     # buf 으로 생성
        noti.PrintDump()
        print(noti.GetSize())
        print(noti.GetBytes())
    print("####### START _MEDIA_ON_NOTI [ Buf 으로 생성 종료]#######")

    print("####### START _MEDIA_OFF_NOTI [ None 으로 생성 시작]#######")
    for calltype in _CALL_TYPE:
        noti = _MEDIA_OFF_NOTI()     # None 으로 생성
        noti.Init(calltype)
        noti.PrintDump()
        print(noti.GetSize())
        print(noti.GetBytes())
    print("####### START _MEDIA_OFF_NOTI [ None 으로 생성 종료]#######")

    print("####### START _MEDIA_OFF_NOTI [ Buf 으로 생성 시작]#######")
    for calltype in _CALL_TYPE:
        call_type = calltype.value
        reason = 1
        reserve2 = 2
        r_call_id = 3

        buf = struct.pack("!BBHI", call_type, reason, reserve2, r_call_id)

        noti = _MEDIA_OFF_NOTI(buf)     # Buf 으로 생성
        noti.PrintDump()
        print(noti.GetSize())
        print(noti.GetBytes())
    print("####### START _MEDIA_OFF_NOTI [ Buf 으로 생성 종료]#######")


def get_buffer_call_setup_res_common(calltype):
    call_type = calltype.value
    result = 2
    reserve2 = 3
    s_call_id = 4
    r_call_id = 5
    media_ip = 7
    media_port = 8
    buf = struct.pack("!BBHIIIH", *(
        call_type,
        result,
        reserve2,
        s_call_id,
        r_call_id,
        media_ip,
        media_port
    ))
    return buf


def get_buffer_call_setup_res_rpc(calltype):
    call_type = calltype.value
    result = 2
    reserve2 = 3
    s_call_id = 4
    r_call_id = 5
    media_ip = 7
    media_port = 8
    v_rate = 9
    buf = struct.pack("!BBHIIIHI", *(
        call_type,
        result,
        reserve2,
        s_call_id,
        r_call_id,
        media_ip,
        media_port,
        v_rate
    ))
    return buf


def get_buffer_call_setup_req_private():
    call_type = _CALL_TYPE._CT_PRIVATE.value
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
    return buf


def get_buffer_call_setup_req_group():
    call_type = _CALL_TYPE._CT_GROUP.value
    priority = 2
    reserve2 = 3
    s_call_id = 4
    bunch_group = 5
    t_ssid = 6
    media_ip = 7
    media_port = 8
    buf = struct.pack("!BBHIIIIH", *(
        call_type,
        priority,
        reserve2,
        s_call_id,
        bunch_group,
        t_ssid,
        media_ip,
        media_port
    ))
    return buf


def get_buffer_call_setup_req_emer():
    call_type = _CALL_TYPE._CT_EMER.value
    priority = 2
    reserve2 = 3
    s_call_id = 4
    bunch_group = 5
    t_ssid = 6
    media_ip = 7
    media_port = 8
    buf = struct.pack("!BBHIIIIH", *(
        call_type,
        priority,
        reserve2,
        s_call_id,
        bunch_group,
        t_ssid,
        media_ip,
        media_port
    ))
    return buf


def get_buffer_call_setup_req_udg():
    call_type = _CALL_TYPE._CT_UDG.value
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
        member_4,
    ))
    return buf


def get_buffer_call_setup_req_alert():
    call_type = _CALL_TYPE._CT_ALERT.value
    priority = 2
    reserve2 = 3
    s_call_id = 4
    o_ssid = 5
    t_ssid = 6
    buf = struct.pack("!BBHIII", *(
        call_type, priority, reserve2, s_call_id, o_ssid, t_ssid
    ))
    return buf


def get_buffer_call_setup_req_rpc():
    call_type = _CALL_TYPE._CT_RPC.value
    reserve1 = 2
    reserve2 = 3
    s_call_id = 4
    o_ssid = 5
    t_ssid = 6
    media_ip = 7
    media_port = 8
    rpc_para = 9
    buf = struct.pack("!BBHIIIIHH", *(
        call_type, reserve1, reserve2, s_call_id, o_ssid, t_ssid, media_ip, media_port, rpc_para
    ))
    return buf


def main():
    make_media_on_off_noti()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
