from twisted.internet import protocol


class ClientProtocol(protocol.Protocol):

    def connectionMade(self):
        print('CmdClientProtocol connectionMade')
        # self.transport.write(b"help")

    def dataReceived(self, data):
        print('CmdClientProtocol recv : ' + data.decode())
        # if data.decode() == 'Goodbye.':
        #     CmdManager.FLAG_EXIT = 'on'


class ReconnectClientFactory(protocol.ReconnectingClientFactory):
    protocol = ClientProtocol()

    def buildProtocol(self, addr):
        print('buildProtocol..')
        return self.protocol

    def clientConnectionFailed(self, connector, reason):
        print('clientConnectionFailed..')
        self.maxDelay = 0.5
        super().clientConnectionFailed(connector, reason)

    def clientConnectionLost(self, connector, unused_reason):
        print('clientConnectionLost..')
        self.maxDelay = 0.5
        super().clientConnectionLost(connector, unused_reason)
