
class Util:
    callid = 1000
    automode = 'on'
    hb = 'on'
    @staticmethod
    def makeCallId():
        if Util.callid is None:
            print('callid is None')
            Util.callid = 1000
            return Util.callid
        ret = Util.callid
        Util.callid += 1
        return ret
