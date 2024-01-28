from pymavlink import mavutil
from pymavlink.mavutil import mavfile

TIMEOUT_SECOND=3
PARAMETER_NAME="GPS_AUTO_SWITCH"

connection:mavfile = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
connection.wait_heartbeat(timeout=TIMEOUT_SECOND)

def set_a_parameter_at_on_board_computer(parameter_name:str,sock:mavfile,timeout:int=TIMEOUT_SECOND):
    sock.mav.param_set_send(
        sock.target_system, sock.target_component,
        bytes(PARAMETER_NAME,'utf-8'),
        2,
        mavutil.mavlink.MAV_PARAM_TYPE_REAL32
    )
    message = sock.recv_match(type='PARAM_VALUE', blocking=True,timeout=3).to_dict()
    print('name: %s\tvalue: %d' %
          (message['param_id'], message['param_value']))


