from define.pgw_define import _MESSAGE_ID, _CALL_TYPE
from config.configure import Config
from call.Manager import Manager as CallManager
from rtp.Manager import Manager as RtpManager
from rtp.pgw2RtpIntercept import InterceptManager


sessions = {
    'server': None,
    'client': None,
    'command': None
}

calltype_switcher = {calltype.value: calltype.name for calltype in _CALL_TYPE}
messageid_switcher = {msg.value: msg.name for msg in _MESSAGE_ID}

calltype_dict = {calltype.name: calltype.value for calltype in _CALL_TYPE}
messageid_dict = {msg.name: msg.value for msg in _MESSAGE_ID}

pgw2Config = Config()

pgw2CallManager = CallManager(1000)
pgw2RtpManager = RtpManager(10000)

pgw2RtpInterceptManager = InterceptManager()