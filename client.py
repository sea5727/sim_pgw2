from __future__ import print_function
from twisted.internet import reactor, protocol
from messages import _CALL_SETUP_REQ, _PGW_MSG_HEAD


class MyProtocol(protocol.Protocol):
    def connectionMade(self):
        h = _PGW_MSG_HEAD(b'\x47\x01\x00\x10')
        p = _CALL_SETUP_REQ(b'bcddeeeeffffgggghhhhii')
        self.transport.write(h.Pack() + p.Pack())

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
