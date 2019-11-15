'sim_pgw2 server module'

from twisted.internet import reactor, protocol
from header import _PGW_MSG_HEAD
from define import __MESSAGE_ID


class MyProtocol(protocol.Protocol):
    def dataReceived(self, data):
        print("dataRecieved : ", data)
        header = _PGW_MSG_HEAD(data[0:1])
        msgid = __MESSAGE_ID(header.gw_msgid)
        
        self.transport.write(data)


class MyFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return MyProtocol()


def main():
    reactor.listenTCP(12345, MyFactory())
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
