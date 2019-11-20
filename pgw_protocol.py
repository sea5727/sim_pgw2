from twisted.internet.protocol import Protocol
from body import *
from header import _PGW_MSG_HEAD
from message import _MESSAGE
from pgw_define import _MESSAGE_ID, _CALL_TYPE


sessions = {
    'server': None,
    'client': None,
}


class Pgw2Protocol(Protocol):
    count = 0

    def __init__(self, s):
        self.sessions = s

    def connectionMade(self):
        self.count += 1
        print(self.transport.socket)
        print('connectionMade{0}'.format(self.count))

    def connectionLost(self, reason):
        print('connectionLost reason:{0}'.format(reason))

    def dataReceived(self, data):
        print('Total Recv (len:{0})'.format(len(data)))
        while len(data) > 4:
            h = _PGW_MSG_HEAD(data[0:4])
            h.PrintDump()
            msgid = _MESSAGE_ID(h.gw_msgid)
            if msgid is _MESSAGE_ID._CALL_SETUP_REQ:
                print('recv : call setup req')
                calltype = _CALL_TYPE(data[h.GetSize():h.GetSize() + 1][0])
                req_pri = _CALL_SETUP_REQ(data[h.GetSize():h.GetSize() + h.length])
                req_pri.PrintDump()

                res = _CALL_SETUP_RES()
                res.Init(calltype)
                res.result = 0
                res.reserve2 = 1
                res.s_call_id = 2
                res.r_call_id = 3
                res.media_ip = 4
                res.media_port = 5
                res.PrintDump()

                msg = _MESSAGE(res)
                print('send(len:{0}) : {1}'.format(msg.GetSize(), msg.GetBytes()))
                self.transport.write(msg.GetBytes())

                noti = _MEDIA_ON_NOTI()
                noti.Init(calltype)
                noti.reserve1 = 1
                noti.reserve2 = 2
                noti.r_call_id = 3
                noti.o_ssid = 4
                rpt = _MESSAGE(noti)
                print('send(len:{0}) : {1}'.format(rpt.GetSize(), rpt.GetBytes()))
                self.transport.write(rpt.GetBytes())
                return
            if msgid is _MESSAGE_ID._CALL_SETUP_RES:
                print('recv : call setup res')
                calltype = _CALL_TYPE(data[h.GetSize():h.GetSize() + 1][0])
                if calltype is _CALL_TYPE._CT_PRIVATE:
                    res_pri = _CALL_SETUP_RES(data[h.GetSize():h.GetSize() + h.length])
                    res_pri.PrintDump()
            elif msgid is _MESSAGE_ID._MEDIA_ON_NOTI:
                print('recv : media on not')
                calltype = _CALL_TYPE(data[h.GetSize():h.GetSize() + 1][0])
                noti = _MEDIA_ON_NOTI(data[h.GetSize():h.GetSize() + h.length])
                noti.PrintDump()
            data = data[h.GetSize() + h.length:]
