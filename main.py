from twisted.internet import reactor, stdio
from client import Pgw2ClientFactory
from server import Pgw2ServerFactory
from cmdline import CommandProtocol


# this connects the protocol to a server running on port 8000
def main():
    stdio.StandardIO(CommandProtocol())
    reactor.listenTCP(54321, Pgw2ServerFactory())
    reactor.connectTCP("localhost", 12345, Pgw2ClientFactory())
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
