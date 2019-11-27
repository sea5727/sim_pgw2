from twisted.internet import reactor, protocol
from pgw_protocol import Pgw2Protocol
from memory import sessions


class Pgw2ServerFactory(protocol.ServerFactory):

    protocol = Pgw2Protocol(sessions, 'SERVER')
    def buildProtocol(self, addr):
        sessions['server'] = Pgw2ServerFactory.protocol
        return Pgw2ServerFactory.protocol

    def ConnectionFailed(self, connect, reason):
        print('ConnectionFailed')

    def ConnectionLost(self, connect, reason):
        print('ConnectionFailed')


def main():
    import sys
    port = 12345
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    print('port : ', port)
    reactor.listenTCP(port, Pgw2ServerFactory())
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
