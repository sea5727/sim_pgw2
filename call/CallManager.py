from rtp.Rtp import RTP

DEFAUT_CALLID = 5000
class CallManager:
    CallId = DEFAUT_CALLID
    Manager = {}

    @staticmethod
    def makeCallId():
        if CallManager.CallId is None:
            print('callid is None')
            CallManager.CallId = DEFAUT_CALLID
            return CallManager.CallId
        ret = CallManager.CallId
        CallManager.CallId += 1
        return ret

    @staticmethod
    def printCallStatus():
        print('####### CALL STATUS ##########')

    @staticmethod
    def GenerateCall(to_ip, to_port, callid):
        rtp = RTP()
        rtp.InitRtp(to_ip, to_port)
        CallManager.Manager[callid] = rtp

    @staticmethod
    def StartCall(callid):
        rtp = CallManager.Manager[callid]
        rtp.SendRtp()
        # recieve?

    @staticmethod
    def PauseCall(callid):
        rtp = CallManager.Manager[callid]
        rtp.PauseRtp()

    def StopCall(self, callid):
        rtp = CallManager.Manager[callid]
        rtp.PauseRtp()
