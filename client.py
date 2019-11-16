from __future__ import print_function
from twisted.internet import reactor, protocol
from body import _CALL_SETUP_REQ, _CALL_SETUP_RES, _MEDIA_ON_NOTI
from message import _MESSAGE
from pgw_define import _CALL_TYPE, _MESSAGE_ID
from header import _PGW_MSG_HEAD


class MyProtocol(protocol.Protocol):
    def connectionMade(self):
        req = _CALL_SETUP_REQ()
        req.Init(_CALL_TYPE._CT_PRIVATE)
        req.priority = 1
        req.reserve2 = 2
        req.s_call_id = 3
        req.o_ssid = 4
        req.t_ssid = 5
        req.media_ip = 6
        req.media_port = 7

        msg = _MESSAGE(req)

        self.transport.write(msg.GetBytes())
        print('connectionMade')

    def dataReceived(self, data):
        print('Total Recv (len:{0})'.format(len(data)))
        while len(data) > 4:
            h = _PGW_MSG_HEAD(data[0:4])
            h.PrintDump()
            msgid = _MESSAGE_ID(h.gw_msgid)
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
        # self.transport.loseConnection()

    def connectionLost(self, reason):
        print("connection lost")


class MyFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return MyProtocol()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed - goodbye!")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost - goodbye!")
        reactor.stop()


# this connects the protocol to a server running on port 8000
def main():
    reactor.connectTCP("localhost", 12345, MyFactory())
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
