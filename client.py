from twisted.internet import reactor, protocol
from pgw_protocol import Pgw2Protocol
from memory import sessions
from config.configure import pgw2Config as config
from logger import pgw2logger as logger

class Pgw2ClientFactory(protocol.ReconnectingClientFactory):

    protocol = Pgw2Protocol(sessions, 'CLIENT')
    
    def buildProtocol(self, addr):
        self.resetDelay()
        sessions['client'] = Pgw2ClientFactory.protocol
        return Pgw2ClientFactory.protocol

    def clientConnectionFailed(self, connector, reason):
        # reactor.callLater(0.5, self.TryReconnect, connector)
        self.maxDelay = config.reconnect_interval
        logger.debug('connection failed {0}:{1}, state:{2}, tryCount:{3}, delay:{4}'.format(
            connector.host,
            connector.port,
            connector.state,
            self.retries,
            self.delay            
        ))

        super().clientConnectionFailed(connector, reason)


# this connects the protocol to a server running on port 8000
def main():
    import sys
    port = 12345
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    print(port)
    reactor.connectTCP("localhost", port, Pgw2ClientFactory())
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
