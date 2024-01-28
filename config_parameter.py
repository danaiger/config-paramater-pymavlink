from pymavlink import mavutil
from pymavlink.mavutil import mavfile
from enum import Enum

class GPS_AUTO_SWITCH(Enum):
    USE_PRIMARY=0
    USE_BEST=1
    BLEND=2
    USE_PRIMARY_IF_3D_FIX_OR_BETTER=4

TIMEOUT_SECOND=3
PARAMETER_NAME="GPS_AUTO_SWITCH"

connection:mavfile = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
connection.wait_heartbeat(timeout=TIMEOUT_SECOND)

def set_a_parameter_at_on_board_computer(parameter_name:str,sock:mavfile,timeout_seconds:int=TIMEOUT_SECOND):
    sock.mav.param_set_send(
        sock.target_system, sock.target_component,
        bytes(parameter_name,'utf-8'),
        2,
        mavutil.mavlink.MAV_PARAM_TYPE_REAL32
    )
    message = sock.recv_match(type='PARAM_VALUE', blocking=True,timeout=timeout_seconds).to_dict()
    print('name: %s\tvalue: %d' %
          (message['param_id'], message['param_value']))


