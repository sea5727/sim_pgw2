from body import *
from message import _MESSAGE
from pgw_define import _CALL_TYPE
import socket
import struct
import sys


test_ip = '192.168.0.166'


def send_call_setup_req(session):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    req = _CALL_SETUP_REQ()
    req.Init(_CALL_TYPE._CT_PRIVATE)
    req.priority = 1
    req.reserve2 = 2
    req.s_call_id = 3
    req.o_ssid = 4
    req.t_ssid = 5
    req.media_ip = struct.unpack('=I', socket.inet_aton(test_ip))[0]
    req.media_port = 7

    msg = _MESSAGE(req)
    msg.body.PrintDump()
    print('send(len:{0}) msg : {1}'.format(
        msg.GetSize(),
        msg.GetBytes()))
    session.transport.write(msg.GetBytes())


def send_call_setup_res(session):
    print('### START ### ' + sys._getframe(0).f_code.co_name + '()')
    res = _CALL_SETUP_RES()
    res.Init(_CALL_TYPE._CT_PRIVATE)
    res.result = 0
    res.reserve2 = 1
    res.s_call_id = 2
    res.r_call_id = 3
    res.media_ip = struct.unpack('=I', socket.inet_aton(test_ip))[0]
    res.media_port = 5

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
