import enum

class __MESSAGE_ID(enum.Enum):
    PGW_MSG_HEAD = -1
    GW_STATUS = 0
    CALL_SETUP_REQ = 1
    CALL_SETUP_RES = 2
    MEDIA_ON_REQ = 3
    MEDIA_ON_RES = 4
    MEDIA_OFF_REQ = 5
    MEDIA_OFF_RES = 6
    MEDIA_ON_NOTI = 7
    MEDIA_OFF_NOTI = 8
    CALL_LEAVE_REQ = 9
    CALL_LEAVE_RES = 10
    CALL_END_NOTI = 11
    BUNCH_INFO = 12
    CALL_AUDIT_REQ = 12
    CALL_AUDIT_RES = 13


class _CALL_TYPE(enum.Enum):
    CT_PRIVATE = 1
    CT_GROUP = 2
    CT_EMER = 3
    CT_UDG = 4
    CT_ALERT = 5
    CT_RPC = 6


def main():
    from messages import _CALL_SETUP_REQ
    p = _CALL_SETUP_REQ(b'abcdefasdasdfasdf12345')
    p.testprint()
    # p = pgw_define._PGW_MSG_HEAD(b'aaaabcddeeeeffffgggghhhhii')
    p.testprint()
    buf = p.Pack()
    print(buf)


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
