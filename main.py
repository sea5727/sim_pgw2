from twisted.internet import reactor, stdio
from client import Pgw2ClientFactory
from server import Pgw2ServerFactory
from cmdline import CommandProtocol
from config import pgwConfig



def main():
    stdio.StandardIO(CommandProtocol())
    reactor.listenTCP(pgwConfig.open_port, Pgw2ServerFactory())
    reactor.connectTCP(pgwConfig.connect_ip, pgwConfig.connect_port, Pgw2ClientFactory())
    reactor.run()


if __name__ == '__main__':
    main()
