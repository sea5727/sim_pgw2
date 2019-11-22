from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Protocol
from header import _PGW_MSG_HEAD
from pgw_define import _MESSAGE_ID, _CALL_TYPE
import body
import proc
from util import Util


sessions = {
    'server': None,
    'client': None,
}

switcher = {msgid.value: msgid.name for msgid in _MESSAGE_ID}


class Pgw2Protocol(Protocol):
    count = 0

    def __init__(self, s, name):
        self.sessions = s
        self.name = name

    def connectionMade(self):
        self.count += 1
        print(self.transport.socket)
        print('{0} connectionMade{1}'.format(self.name, self.count))
        if self.name == 'CLIENT':
            self.hb = LoopingCall(proc.send_gw_status, self, 1, 1)
            self.hb.start(10, Now=True)

    def connectionLost(self, reason):
        print('{0} connectionLost reason:{1}'.format(self.name, reason))
        if self.hb:
            self.hb.stop()

    def dataReceived(self, data):
        print('{0} Total Recv (len:{1})'.format(self.name, len(data)))
        while len(data) > 4:
            h = _PGW_MSG_HEAD(data[0:4])
            h.PrintDump()
            msgid = _MESSAGE_ID(h.gw_msgid)

            message_name = switcher.get(msgid.value, None)
            req = getattr(body, message_name)(data[h.GetSize():h.GetSize() + h.length])
            req.PrintDump()

            if Util.hb == 'on':
                if type(req) is body._GW_STATUS and req.cmd == body._GW_STATUS.KeepAliveRequest:
                    proc.send_gw_status(self, body._GW_STATUS.KeepAliveResponse, body._GW_STATUS.ConnectedWithPTALKServer)

            if Util.automode == 'on':
                if type(req) is body._CALL_SETUP_REQ:
                    call_id = Util.makeCallId()
                    proc.send_call_setup_res(self, calltype=req.call_type, result=0, reserve2=0, s_call_id=call_id, r_call_id=req.s_call_id, media_ip='127.0.0.1', media_port=5)
                elif type(req) is body._MEDIA_ON_REQ:
                    proc.send_media_on_res(self, calltype=req.call_type, result=0, reserve2=0, r_call_id=req.r_call_id)
                elif type(req) is body._MEDIA_OFF_REQ:
                    proc.send_media_off_res(self, calltype=req.call_type, result=0, reserve2=0, r_call_id=req.r_call_id)

            data = data[h.GetSize() + h.length:]
