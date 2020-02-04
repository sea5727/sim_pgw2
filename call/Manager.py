class Call:
    # MESSAGES 도 필요?? ( 호셋업 메시지를 가지고 있을 필요가 있을까)
    call_type = -1
    priority = -1
    s_call_id = -1
    r_call_id = -1   # 상대의 Call Id
    o_ssid = -1      # 발신자 번호
    t_ssid = -1      # 수신자 번호
    bunch_group = -1
    media_ip = ''
    media_port = -1
    mem_cnt = -1
    mem_list = []
    rpc_param = -1


class Manager:
    Calls = {}

    def __init__(self, init_call_id=0):
        self.CallId = init_call_id

    def makeCallId(self):
        callid = self.CallId
        self.CallId += 1
        return callid

    def getCallId(self, keyCallId):
        if keyCallId in self.Calls:
            return self.Calls[keyCallId]
        return None

    def setCallId(self, myCallId, partnerCallId):
        self.Calls[myCallId] = partnerCallId
