import enum


CALL_SETUP_REQ_CT_PRIVATE = [
    ('call_type', 'B'),     # unsigned char
    ('priority', 'B'),      # unsgiend char
    ('reserve2', 'H'),      # unsgiend short
    ('s_call_id', 'I'),     # unsigend int
    ('o_ssid', 'I'),        # unsigned int
    ('t_ssid', 'I'),        # unsigned int
    ('media_ip', 'I'),      # unsigned int
    ('media_port', 'H'),    # unsigned short
    ]
CALL_SETUP_REQ_CT_GROUP = [
    ('call_type', 'B'),     # unsigned char
    ('priority', 'B'),      # unsgiend char
    ('reserve2', 'H'),      # unsgiend short
    ('s_call_id', 'I'),     # unsigend int
    ('o_ssid', 'I'),        # unsigned int
    ('bunch_group', 'I'),        # unsigned int
    ('media_ip', 'I'),      # unsigned int
    ('media_port', 'H'),    # unsigned short
]
CALL_SETUP_REQ_CT_EMER = [
    ('call_type', 'B'),     # unsigned char
    ('priority', 'B'),      # unsgiend char
    ('reserve2', 'H'),      # unsgiend short
    ('s_call_id', 'I'),     # unsigend int
    ('o_ssid', 'I'),        # unsigned int
    ('bunch_group', 'I'),        # unsigned int
    ('media_ip', 'I'),      # unsigned int
    ('media_port', 'H'),    # unsigned short
]
CALL_SETUP_REQ_CT_UDG = [
    ('call_type', 'B'),     # unsigned char
    ('priority', 'B'),      # unsgiend char
    ('reserve2', 'H'),      # unsgiend short
    ('s_call_id', 'I'),     # unsigend int
    ('o_ssid', 'I'),        # unsigned int
    ('media_ip', 'I'),      # unsigned int
    ('media_port', 'H'),    # unsigned short
    ('mem_cnt', 'H'),       # unsigned short
    ('media_port', '10s'),  # 가변
]
CALL_SETUP_REQ_CT_ALERT = [
    ('call_type', 'B'),     # unsigned char
    ('reserve1', 'B'),      # unsgiend char
    ('reserve2', 'H'),      # unsgiend short
    ('s_call_id', 'I'),     # unsigend int
    ('o_ssid', 'I'),        # unsigned int
    ('t_ssid', 'I'),      # unsigned int
]
CALL_SETUP_REQ_CT_RPC = [
    ('call_type', 'B'),     # unsigned char
    ('reserve1', 'B'),      # unsgiend char
    ('reserve2', 'H'),      # unsgiend short
    ('s_call_id', 'I'),     # unsigend int
    ('o_ssid', 'I'),        # unsigned int
    ('t_ssid', 'I'),      # unsigned int
    ('media_ip', 'I'),      # unsigned int
    ('media_port', 'H'),    # unsigned short
    ('rpc_para', 'H'),       # unsigned short
]
CALL_SETUP_RES_COMMON = [
    ('call_type', 'B'),     # unsigned char
    ('result', 'B'),      # unsgiend char
    ('reserve2', 'H'),      # unsgiend short
    ('s_call_id', 'I'),     # unsigend int
    ('r_call_id', 'I'),        # unsigned int
    ('media_ip', 'I'),        # unsigned int
    ('media_port', 'H'),    # unsigned short
]
CALL_SETUP_RES_CT_RPC = [
    ('call_type', 'B'),     # unsigned char
    ('result', 'B'),        # unsgiend char
    ('reserve2', 'H'),      # unsgiend short
    ('s_call_id', 'I'),     # unsigend int
    ('r_call_id', 'I'),     # unsigned int
    ('media_ip', 'I'),      # unsigned int
    ('media_ip', 'I'),      # unsigned int
    ('media_port', 'H'),    # unsigned short
    ('v_rate',  'I'),       # unsigned int
]


class _MESSAGE_ID(enum.Enum):
    PGW_MSG_HEAD = -1
    GW_STATUS = 0
    CALL_SETUP_REQ = 1
    CALL_SETUP_RES = 2
    CALL_LEAVE_REQ = 3
    CALL_LEAVE_RES = 4
    CALL_END_NOTI = 5
    MEDIA_ON_REQ = 6
    MEDIA_ON_RES = 7
    MEDIA_OFF_REQ = 8
    MEDIA_OFF_RES = 9
    MEDIA_ON_NOTI = 10
    MEDIA_OFF_NOTI = 11
    BUNCH_INFO = 11
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
