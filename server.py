'sim_pgw2 server module'

from twisted.internet import reactor, protocol
from header import _PGW_MSG_HEAD
from body import _CALL_SETUP_REQ, _CALL_SETUP_RES, _MEDIA_ON_NOTI
from message import _MESSAGE
from pgw_define import _MESSAGE_ID, _CALL_TYPE


class MyProtocol(protocol.Protocol):
    def dataReceived(self, data):
        print("dataRecieved : ", data)
        h = _PGW_MSG_HEAD(data[0:4])
        h.PrintDump()

        msgid = _MESSAGE_ID(h.gw_msgid)
        if msgid is _MESSAGE_ID._CALL_SETUP_REQ:
            print('recv : call setup req')
            calltype = _CALL_TYPE(data[h.GetSize():h.GetSize() + 1][0])
            if calltype is _CALL_TYPE._CT_PRIVATE:
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
            elif calltype is _CALL_TYPE.CT_GROUP:
                print('')
            elif calltype is _CALL_TYPE.CT_EMER:
                print('')
            elif calltype is _CALL_TYPE.CT_UDG:
                print('')
            elif calltype is _CALL_TYPE.CT_ALERT:
                print('')
            elif calltype is _CALL_TYPE.CT_RPC:
                print('')
            print('calltype :', calltype)
            req = _CALL_SETUP_REQ(data[h.GetSize():h.GetSize() + h.length])
            req.PrintDump()
            res = _CALL_SETUP_RES(None, _CALL_TYPE(req.msg.call_type))
            res.msg.result = 0
            res.msg.reserve2 = 1
            res.msg.s_call_id = 2
            res.msg.r_call_id = 3
            res.msg.media_ip = 4
            res.msg.media_port = 5
            res.PrintDump()

            msg = _MESSAGE(res)

            self.transport.write(msg.GetBytes())

            noti = _MEDIA_ON_NOTI(None, _CALL_TYPE(req.msg.call_type))
            noti.reserve1 = 1
            noti.reserve2 = 2
            noti.r_call_id = 3
            noti.o_ssid = 4

            # rpt = _MESSAGE_ID(noti)
            # self.transport.write(rpt.GetBytes())


class MyFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return MyProtocol()


def main():
    reactor.listenTCP(12345, MyFactory())
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
