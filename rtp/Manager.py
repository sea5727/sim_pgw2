class Manager:
    Rtps = {}
    init_port = 10000
    def __init__(self, init_recv_port=init_port):
        self.recv_port = init_recv_port
    def makeRecvPort(self):
        recv_port = self.recv_port
        self.recv_port += 1
        if self.recv_port > 65000:
            self.recv_port = Manager.init_port
        return recv_port

    def getRtp(self, key):
        if key in self.Rtp:
            return self.Rtp[key]
        return None

    def setRtp(self, key, rtpSender, rtpReceiver):
        rtp = {
            "RtpSender" : rtpSender,
            "RtpReceiver" : rtpReceiver,
        }
        self.Rtps[key] = rtp
