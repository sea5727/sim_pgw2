
from body import _CALL_SETUP_REQ, _MEDIA_ON_NOTI
from message import _MESSAGE
from pgw_define import _CALL_TYPE


def send_call_setup_req(session):
    req = _CALL_SETUP_REQ()
    req.Init(_CALL_TYPE._CT_PRIVATE)
    req.priority = 1
    req.reserve2 = 2
    req.s_call_id = 3
    req.o_ssid = 4
    req.t_ssid = 5
    req.media_ip = 6
    req.media_port = 7

    msg = _MESSAGE(req)
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_media_on_noti(session):
    noti = _MEDIA_ON_NOTI()
    noti.Init(_CALL_TYPE._CT_PRIVATE)
    noti.reserve1 = 1
    noti.reserve2 = 2
    noti.r_call_id = 3
    noti.o_ssid = 4

    msg = _MESSAGE(noti)
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())
