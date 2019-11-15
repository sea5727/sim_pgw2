from __future__ import print_function
from twisted.internet import reactor, protocol
from body import _CALL_SETUP_REQ
from header import _PGW_MSG_HEAD
from define import _CALL_TYPE, __MESSAGE_ID

class MyProtocol(protocol.Protocol):
    def connectionMade(self):
        req = _CALL_SETUP_REQ(None, _CALL_TYPE.CT_PRIVATE)
        req.priority = 1
        req.reserve2 = 2
        req.s_call_id = 3
        req.o_ssid = 4
        req.t_ssid = 5
        req.media_ip = 6
        req.media_port = 7

        header = _PGW_MSG_HEAD(None)
        header.gw_magic = b'\x47'[0]
        header.gw_msgid = __MESSAGE_ID.CALL_AUDIT_REQ.value
        header.length = req.GetSize()

        self.transport.write(header.GetBytes() + req.GetBytes())
        print('connectionMade')


    def dataReceived(self, data):
        print("Server said:", data)
        self.transport.loseConnection()

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
