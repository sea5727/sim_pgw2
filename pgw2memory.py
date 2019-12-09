from define.pgw_define import _MESSAGE_ID, _CALL_TYPE
from config.configure import Config
from call.Manager import Manager
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

pgw2CallManager = Manager(1000)
