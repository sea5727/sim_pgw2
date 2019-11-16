from twisted.internet import reactor, protocol
from pgw_protocol import Pgw2Protocol, sessions


class Pgw2ClientFactory(protocol.ReconnectingClientFactory):

    reconnect_count = 0

    def buildProtocol(self, addr):
        self.resetDelay()
        self.protocol = Pgw2Protocol(sessions)
        sessions['client'] = self.protocol
        return self.protocol

    def clientConnectionFailed(self, connector, reason):
        # reactor.callLater(0.5, self.TryReconnect, connector)
        self.maxDelay = 0.5
        print("Connection failed {0}:{1}, state:{2} tryCount:{3} delay:{4}".format(
            connector.host,
            connector.port,
            connector.state,
            self.retries,
            self.delay))
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
