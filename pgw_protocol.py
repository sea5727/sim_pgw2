from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Protocol
from messages.header import _PGW_MSG_HEAD
from define.pgw_define import _MESSAGE_ID
import messages.body
from protocol import proc
from pgw2memory import pgw2Config as config
from logger.pyLogger import pgw2logger as logger
from pgw2memory import messageid_switcher
from pgw2memory import pgw2CallManager
from pgw2memory import pgw2RtpManager
from rtp.Pgw2Rtp import RtpReceiver, RtpSender, RtpProxy
from pgw2memory import pgw2RtpInterceptManager as InterceptManager
import struct
import socket
from define.pgw_define import _CALL_TYPE

class Pgw2Protocol(Protocol):
    count = 0

    def __init__(self, s, name):
        self.sessions = s
        self.name = name

    def connectionMade(self):
        self.count += 1
        logger.debug(self.transport.socket)
        logger.debug('{0} connectionMade{1}'.format(self.name, self.count))
        if self.name == 'CLIENT' and config.flag_hb == 'on':
            self.hb = LoopingCall(proc.send_gw_status, self, cmd=1, state=1)
            self.hb.start(10, now=True)

    def connectionLost(self, reason):
        logger.debug('{0} connectionLost reason:{1}'.format(self.name, reason))
        if self.name != 'CLIENT':
            return
        if hasattr(self, 'hb') and self.hb is not None:
            self.hb.stop()

    def dataReceived(self, data):
        logger.debug('RECV < [len:{0}] ({1}) : '.format(len(data), self.name))

        while len(data) > 4:
            h = _PGW_MSG_HEAD(data[0:4])
            logger.debug('RECV < Header : [len:{0}, {1}] ({2}) : '.format(h.GetSize(), h.GetBytes(), self.name))
            logger.debug('RECV < ' + h.StringDump())
            msgid = _MESSAGE_ID(h.gw_msgid)
            message_name = messageid_switcher.get(msgid.value, None)
            callid = -1
            msg = getattr(messages.body, message_name)(data[h.GetSize():h.GetSize() + h.length])
            logger.debug('RECV < msg : [len:{0}, {1}] ({2}) : '.format(msg.GetSize(), msg.GetBytes(), self.name))
            logger.info('RECV < ' + msg.StringDump())

            if type(msg) is messages.body._CALL_SETUP_RES:
                callid = pgw2CallManager.getCallId(msg.r_call_id)
                if callid is not None:
                    pgw2CallManager.setCallId(callid, msg.s_call_id)
                    

            if config.flag_hb == 'on':
                if type(msg) is messages.body._GW_STATUS and msg.cmd == messages.body._GW_STATUS.KeepAliveRequest:
                    proc.send_gw_status(self, cmd=messages.body._GW_STATUS.KeepAliveResponse,
                                        state=messages.body._GW_STATUS.ConnectedWithPTALKServer)

            if config.flag_automode == 'on':
                if type(msg) is messages.body._CALL_SETUP_RES:
                    pgw2CallManager.setCallId(msg.r_call_id, msg.s_call_id)
                    
                elif type(msg) is messages.body._CALL_SETUP_REQ:
                    callid = pgw2CallManager.makeCallId()
                    pgw2CallManager.setCallId(callid, msg.s_call_id)

                    if msg.call_type != _CALL_TYPE._CT_ALERT.value:
                        remoteIp = socket.inet_ntoa(struct.pack('I', msg.media_ip))
                        remotePort = msg.media_port
                        recv_ip = '0.0.0.0'
                        recv_port = pgw2RtpManager.makeRecvPort()
                            

                    res = messages.body._CALL_SETUP_RES()
                    res.Init(msg.call_type)
                    res.result = 0
                    res.r_call_id = msg.s_call_id
                    res.s_call_id = callid
                    res.media_ip = 0
                    res.media_port = 0
                    if msg.call_type != _CALL_TYPE._CT_ALERT.value:
                        res.media_ip = struct.unpack('I', socket.inet_aton(config.my_ip))[0]
                        res.media_port = recv_port

                        client = InterceptManager.matchClient(res)
                        # if client is not None:
                        #     print('client ip:', client.ip)
                        #     print('client port:', client.port)
                        #     print('client filter_type:', client.filter_type)
                        #     print('client filter_value:', client.filter_value)

                        if config.flag_rtp == 'on':
                            rtpSender = RtpSender()
                            rtpSender.SetLocalPort(recv_port)
                            rtpSender.InitGObjectRtp(remoteIp, remotePort)
                            if client is not None:
                                rtpReceiver = RtpProxy()    
                                rtpReceiver.InitGObjectRtp(recv_ip, recv_port, client.ip, client.port)
                            else:
                                rtpReceiver = RtpReceiver()
                            # rtpReceiver.InitGObjectRtp(recv_ip, recv_port)

                            pgw2RtpManager.setRtp(callid, rtpSender, rtpReceiver)
                            logger.info('RtpReceiver Ip:{0} Port:{1}, RtpSender Ip:{2}, Port:{3}'.format(recv_ip, recv_port, remoteIp, remotePort))
                            rtpSender.StartRtp()
                            rtpReceiver.StartRtp()
                        
                        
                        
                    proc.send_call_setup_res(self, res)

                elif type(msg) is messages.body._MEDIA_ON_REQ:
                    callid = pgw2CallManager.getCallId(msg.r_call_id)
                    if callid is None:
                        callid = 12345
                    proc.send_media_on_res(self,
                                           calltype=msg.call_type,
                                           result=0,
                                           reserve2=0,
                                           r_call_id=callid)
                elif type(msg) is messages.body._MEDIA_OFF_REQ:
                    callid = pgw2CallManager.getCallId(msg.r_call_id)
                    if callid is None:
                        callid = 12345
                    proc.send_media_off_res(self,
                                            calltype=msg.call_type,
                                            result=0,
                                            reserve2=0,
                                            r_call_id=callid)
                elif type(msg) is messages.body._CALL_LEAVE_REQ:
                    callid = pgw2CallManager.getCallId(msg.r_call_id)
                    if callid is None:
                        callid = 12345
                    proc.send_call_leave_res(self,
                                            calltype=msg.call_type,
                                            result=0,
                                            reserve2=0,
                                            r_call_id=callid)
                elif type(msg) is messages.body._CALL_END_NOTI:
                    callid = pgw2CallManager.getCallId(msg.r_call_id)
                    objRtp = pgw2RtpManager.getRtp(callid)
                    if objRtp is not None:
                        objRtp['RtpSender'].StopRtp()
                        objRtp['RtpReceiver'].StopRtp()
                        
                    

            data = data[h.GetSize() + h.length:]
