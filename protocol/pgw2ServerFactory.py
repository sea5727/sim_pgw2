from twisted.internet import reactor, protocol
from pgw_protocol import Pgw2Protocol
from pgw2memory import sessions
<<<<<<< HEAD
from logger.pyLogger import pgw2logger as logger
=======
>>>>>>> ee35aef1f7ce100641f18c8f4cc72c928439bed1


class Pgw2ServerFactory(protocol.ServerFactory):

    protocol = Pgw2Protocol(sessions, 'SERVER')

    def buildProtocol(self, addr):
<<<<<<< HEAD
        logger.debug('Pgw2ServerFactory : buildProtocol... addr: host({0}), port({1}), type({2})'.format( addr.host, addr.port, addr.type))
=======
>>>>>>> ee35aef1f7ce100641f18c8f4cc72c928439bed1
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
