"""
Example code of how to read and write vehicle parameters using pymavlink
"""

import time
# Import mavutil
from pymavlink import mavutil

TIMEOUT_SECOND=3

master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
# Wait a heartbeat before sending commands
master.wait_heartbeat()
print("here")
# Request parameter
master.mav.param_request_read_send(
    master.target_system, master.target_component,
    b'GPS_AUTO_SWITCH',
    -1
)

print("here2")
# Print old parameter value
message = master.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
print(message)
print('name: %s\tvalue: %d' %
      (message['param_id'], message['param_value']))

print("here1")
time.sleep(1)

# Set parameter value
# Set a parameter value TEMPORARILY to RAM. It will be reset to default on system reboot.
# Send the ACTION MAV_ACTION_STORAGE_WRITE to PERMANENTLY write the RAM contents to EEPROM.
# The parameter variable type is described by MAV_PARAM_TYPE in http://mavlink.org/messages/common.
master.mav.param_set_send(
    master.target_system, master.target_component,
    b'GPS_AUTO_SWITCH',
    3,
    mavutil.mavlink.MAV_PARAM_TYPE_REAL32
)

# Read ACK
# IMPORTANT: The receiving component should acknowledge the new parameter value by sending a
# param_value message to all communication partners.
# This will also ensure that multiple GCS all have an up-to-date list of all parameters.
# If the sending GCS did not receive a PARAM_VALUE message within its timeout time,
# it should re-send the PARAM_SET message.
message = master.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
print('name: %s\tvalue: %d' %
      (message['param_id'], message['param_value']))

time.sleep(1)

# Request parameter value to confirm
master.mav.param_request_read_send(
    master.target_system, master.target_component,
    b'GPS_AUTO_SWITCH',
    -1
)

# Print new value in RAM
message = master.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
print('name: %s\tvalue: %d' %
      (message['param_id'], message['param_value']))
