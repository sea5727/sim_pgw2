
from twisted.internet import reactor, stdio
from client import Pgw2ClientFactory
from server import Pgw2ServerFactory
from cmdline import CommandProtocol
from config.configure import Config
from util import Util
import sys
from logger import LogManager


def main():
    # main.py open_port connect_ip connect_port automode(on/off) hb(on/off) rtp(on/off)
    # args > config.ini 순으로 적용
    config = Config()
    config.Init('./config.ini')
    
    logger = LogManager.getInstance()
    logger.info('######## START ##########')

    Util.automode = config.automode
    Util.hb = config.hb
    Util.rtp = config.rtp
    Util.std = config.std
    Util.log = config.log

    for args in sys.argv:
        logger.info('system args : {0}'.format(args))
    open_port = config.open_port
    connect_port = config.connect_port

    if len(sys.argv) > 1 and sys.argv[1]:
        open_port = int(sys.argv[1])
    if len(sys.argv) > 2 and sys.argv[2]:
        connect_port = int(sys.argv[2])

    logger.info('open port : {0}, connect port : {1}'.format(open_port, connect_port))
    stdio.StandardIO(CommandProtocol())
    reactor.listenTCP(open_port, Pgw2ServerFactory())
    reactor.connectTCP(config.connect_ip, connect_port, Pgw2ClientFactory())
    reactor.run()


if __name__ == '__main__':
    main()
