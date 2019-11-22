from body import *
from message import _MESSAGE
from pgw_define import _CALL_TYPE
import socket
import struct
import sys


__all__ = [
    'send_call_setup_req', 
    'send_call_setup_res', 
    'send_media_on_noti', 
    'send_media_off_noti', 
    'send_media_on_req', 
    'send_media_on_res', 
    'send_media_off_req', 
    'send_media_off_res', 
    'send_call_leave_req', 
    'send_call_leave_res',
    'send_call_end_noti',
    'send_bunch_info',
    ]

test_ip = '192.168.0.166'

def send_gw_status(session, cmd=1, state=1):
    gs = _GW_STAUS()
    gs.cmd = cmd
    gs.state = state
    msg = _MESSAGE(gs)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())
    

def send_call_setup_req(session, calltype=_CALL_TYPE._CT_PRIVATE, priority=1, reserve2=2, s_call_id=3, o_ssid=4, t_ssid=5, media_ip='127.0.0.1', media_port=7):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    req = _CALL_SETUP_REQ()
    req.Init(calltype)
    req.priority = priority
    req.reserve2 = reserve2
    req.s_call_id = s_call_id
    req.o_ssid = o_ssid
    req.t_ssid = t_ssid
    req.media_ip = struct.unpack('=I', socket.inet_aton(media_ip))[0]
    req.media_port = media_port

    msg = _MESSAGE(req)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_call_setup_res(session, calltype=_CALL_TYPE._CT_PRIVATE, result=0, reserve2=1, s_call_id=2, r_call_id=3, media_ip='127.0.0.1', media_port=5):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    res = _CALL_SETUP_RES()
    res.Init(calltype)
    res.result = result
    res.reserve2 = reserve2
    res.s_call_id = s_call_id
    res.r_call_id = r_call_id
    res.media_ip = struct.unpack('=I', socket.inet_aton(media_ip))[0]
    res.media_port = media_port

    msg = _MESSAGE(res)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_media_on_noti(session):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    noti = _MEDIA_ON_NOTI()
    noti.Init(_CALL_TYPE._CT_PRIVATE)
    noti.reserve1 = 1
    noti.reserve2 = 2
    noti.r_call_id = 3
    noti.o_ssid = 4

    msg = _MESSAGE(noti)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_media_off_noti(session):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    noti = _MEDIA_OFF_NOTI()
    noti.Init(_CALL_TYPE._CT_PRIVATE)
    noti.reason = 1
    noti.reserve2 = 2
    noti.r_call_id = 3

    msg = _MESSAGE(noti)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_media_on_req(session):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    req = _MEDIA_ON_REQ()
    req.Init(_CALL_TYPE._CT_PRIVATE)
    req.o_priority = 1
    req.reserve2 = 2
    req.r_call_id = 3
    req.o_ssid = 4

    msg = _MESSAGE(req)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_media_on_res(session):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    res = _MEDIA_ON_RES()
    res.Init(_CALL_TYPE._CT_PRIVATE)
    res.result = 1
    res.reserve2 = 2
    res.r_call_id = 3
    res.o_ssid = 4

    msg = _MESSAGE(res)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_media_off_req(session):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    req = _MEDIA_OFF_REQ()
    req.Init(_CALL_TYPE._CT_PRIVATE)
    req.reserve1 = 1
    req.reserve2 = 2
    req.r_call_id = 3

    msg = _MESSAGE(req)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_media_off_res(session):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    res = _MEDIA_OFF_RES()
    res.Init(_CALL_TYPE._CT_PRIVATE)
    res.result = 1
    res.reserve2 = 2
    res.r_call_id = 3

    msg = _MESSAGE(res)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_call_leave_req(session):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    req = _CALL_LEAVE_REQ()
    req.Init(_CALL_TYPE._CT_PRIVATE)
    req.reserve1 = 1
    req.reserve2 = 2
    req.r_call_id = 3

    msg = _MESSAGE(req)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_call_leave_res(session):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    res = _CALL_LEAVE_RES()
    res.Init(_CALL_TYPE._CT_PRIVATE)
    res.result = 1
    res.reserve2 = 2
    res.r_call_id = 3

    msg = _MESSAGE(res)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_call_end_noti(session):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    noti = _CALL_END_NOTI()
    noti.Init(_CALL_TYPE._CT_PRIVATE)
    noti.reason = 1
    noti.reserve2 = 2
    noti.r_call_id = 3

    msg = _MESSAGE(noti)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_bunch_info(session):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    noti = _BUNCH_INFO()
    noti.Init()
    noti.cmd = 1
    noti.reserve1 = 2
    noti.counter = 3
    noti.bunch = [4, 5, 6]

    msg = _MESSAGE(noti)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_call_audit_req(session):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    req = _CALL_AUDIT_REQ()
    req.Init(_CALL_TYPE._CT_PRIVATE)
    req.r_call_id = 2

    msg = _MESSAGE(req)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_call_audit_res(session):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    res = _CALL_AUDIT_RES()
    res.Init(_CALL_TYPE._CT_PRIVATE)
    res.r_call_id = 1
    res.result = 2
    res.expire_time = 3

    msg = _MESSAGE(res)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())

def proc_test(session):
    send_call_setup_req(session)
    send_call_setup_res(session)
    send_media_on_noti(session)
    send_media_off_noti(session)
    send_media_on_req(session)
    send_media_on_res(session)
    send_media_off_req(session)
    send_media_off_res(session)
    send_call_leave_req(session)
    send_call_leave_res(session)
    send_call_end_noti(session)
    send_bunch_info(session)
    send_call_audit_req(session)
    send_call_audit_res(session)
