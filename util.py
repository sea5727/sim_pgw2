
class Util:
    callid = 1000

    @staticmethod
    def makeCallId():
        if Util.callid is None:
            print('callid is None')
            Util.callid = 1000
            return Util.callid
        Util.callid += 1
        return Util.callid
