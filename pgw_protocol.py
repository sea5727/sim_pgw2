from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Protocol
from messages.header import _PGW_MSG_HEAD
from define.pgw_define import _MESSAGE_ID, _CALL_TYPE
import messages.body
import proc
import socket
import struct
from util import Util
from call.CallManager import CallManager


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
            self.hb = LoopingCall(proc.send_gw_status, self, cmd=1, state=1)
            self.hb.start(10, now=True)

    def connectionLost(self, reason):
        print('{0} connectionLost reason:{1}'.format(self.name, reason))
        if self.name == 'CLIENT' and self.hb is not None:
            self.hb.stop()

    def dataReceived(self, data):
        if Util.printf == 'on':
            print('{0} Total Recv (len:{1})'.format(self.name, len(data)))
        while len(data) > 4:
            h = _PGW_MSG_HEAD(data[0:4])
            if Util.printf == 'on':
                h.PrintDump()
            msgid = _MESSAGE_ID(h.gw_msgid)
            message_name = switcher.get(msgid.value, None)
            callid = -1
            msg = getattr(messages.body, message_name)(data[h.GetSize():h.GetSize() + h.length])
            
            if Util.printf == 'on':
                msg.PrintDump()

            if Util.hb == 'on':
                if type(msg) is messages.body._GW_STATUS and msg.cmd == messages.body._GW_STATUS.KeepAliveRequest:
                    proc.send_gw_status(self, cmd=messages.body._GW_STATUS.KeepAliveResponse, state=messages.body._GW_STATUS.ConnectedWithPTALKServer)

            if Util.rtp == 'on':
                if type(msg) in (messages.body._CALL_SETUP_REQ, messages.body._CALL_SETUP_RES):
                    callid = CallManager.makeCallId()
                    to_ip = socket.inet_ntoa(struct.pack("=I", msg.media_ip))
                    to_port = msg.media_port
                    CallManager.GenerateCall(to_ip, to_port, callid)

            if Util.automode == 'on':
                if type(msg) is messages.body._CALL_SETUP_REQ:
                    if Util.rtp == 'off':
                        callid = CallManager.makeCallId()
                    proc.send_call_setup_res(self, calltype=msg.call_type, result=0, reserve2=0, s_call_id=callid, r_call_id=msg.s_call_id, media_ip='127.0.0.1', media_port=5)
                elif type(msg) is messages.body._MEDIA_ON_REQ:
                    proc.send_media_on_res(self, calltype=msg.call_type, result=0, reserve2=0, r_call_id=msg.r_call_id)
                elif type(msg) is messages.body._MEDIA_OFF_REQ:
                    proc.send_media_off_res(self, calltype=msg.call_type, result=0, reserve2=0, r_call_id=msg.r_call_id)



                
            data = data[h.GetSize() + h.length:]
