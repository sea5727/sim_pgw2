
from twisted.internet import reactor, stdio
from client import Pgw2ClientFactory
from server import Pgw2ServerFactory
from cmdline import CommandProtocol
from config.configure import pgwConfig
import sys


def main():
    for args in sys.argv:
        print(args)
    open_port = pgwConfig.open_port
    connect_port = pgwConfig.connect_port

    if len(sys.argv) > 1 and sys.argv[1]:
        open_port = int(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2]:
        connect_port = int(sys.argv[2])

    print('open port : {0}, connect port : {1}'.format(open_port, connect_port))
    stdio.StandardIO(CommandProtocol())
    reactor.listenTCP(open_port, Pgw2ServerFactory())
    reactor.connectTCP(pgwConfig.connect_ip, connect_port, Pgw2ClientFactory())
    reactor.run()


if __name__ == '__main__':
    main()
