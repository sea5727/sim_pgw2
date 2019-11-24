import enum


class _MESSAGE_ID(enum.Enum):
    _GW_STATUS = 0
    _CALL_SETUP_REQ = 1
    _CALL_SETUP_RES = 2
    _MEDIA_ON_REQ = 3
    _MEDIA_ON_RES = 4
    _MEDIA_OFF_REQ = 5
    _MEDIA_OFF_RES = 6
    _MEDIA_ON_NOTI = 7
    _MEDIA_OFF_NOTI = 8
    _CALL_LEAVE_REQ = 9
    _CALL_LEAVE_RES = 10
    _CALL_END_NOTI = 11
    _BUNCH_INFO = 12
    _CALL_AUDIT_REQ = 13
    _CALL_AUDIT_RES = 14


class _CALL_TYPE(enum.Enum):
    _CT_PRIVATE = 1
    _CT_GROUP = 2
    _CT_EMER = 3
    _CT_UDG = 4
    _CT_ALERT = 5
    _CT_RPC = 6


# def main():
#     from .messages import _CALL_SETUP_REQ
#     p = _CALL_SETUP_REQ(b'abcdefasdasdfasdf12345')
#     p.testprint()
#     # p = pgw_define._PGW_MSG_HEAD(b'aaaabcddeeeeffffgggghhhhii')
#     p.testprint()
#     buf = p.Pack()
#     print(buf)


# # this only runs if the module was *not* imported
# if __name__ == '__main__':
#     main()
