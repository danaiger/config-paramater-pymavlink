from enum import Enum


class GPS_Auto_Switch(Enum):
    USE_PRIMARY = 0
    USE_BEST = 1
    BLEND = 2
    USE_PRIMARY_IF_3D_FIX_OR_BETTER = 4
