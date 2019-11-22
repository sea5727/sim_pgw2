from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Protocol
from body import *
from header import _PGW_MSG_HEAD
from message import _MESSAGE
from pgw_define import _MESSAGE_ID, _CALL_TYPE
from proc import *
from util import Util
sessions = {
    'server': None,
    'client': None,
}


class Pgw2Protocol(Protocol):
    count = 0

    def __init__(self, s, name):
        self.sessions = s
        self.name = name

    def connectionMade(self):
        self.count += 1
        print(self.transport.socket)
        print('{0} connectionMade{1}'.format(self.name, self.count))
        # LoopingCall(lambda : )

    def connectionLost(self, reason):
        print('{0} connectionLost reason:{1}'.format(self.name, reason))

    def dataReceived(self, data):
        print('{0} Total Recv (len:{1})'.format(self.name, len(data)))
        while len(data) > 4:
            h = _PGW_MSG_HEAD(data[0:4])
            h.PrintDump()
            msgid = _MESSAGE_ID(h.gw_msgid)
            if msgid is _MESSAGE_ID._CALL_SETUP_REQ:
                print('recv : call setup req')
                calltype = _CALL_TYPE(data[h.GetSize():h.GetSize() + 1][0])
                req_pri = _CALL_SETUP_REQ(data[h.GetSize():h.GetSize() + h.length])
                req_pri.PrintDump()
                
                call_id = Util.makeCallId()
                send_call_setup_res(self, req_pri.call_type, 0, 0, req_pri.s_call_id, call_id, '192.168.0.166', call_id)
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
