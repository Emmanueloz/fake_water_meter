from enum import Enum


class Events(str, Enum):
    CONNECTION_SUCCESS = "connection_success"
    CONNECTION_ERROR = "connection_error"
    CONNECTION_CLOSED = "connection_closed"
    SEND_SUCCESS = "send_success"
    SEND_ERROR = "send_error"
    SET_LOOP_STARTED = "set_loop_started"
    CLEAR_LIST = "clear_list"
    SET_RECORD_SELECTED = "set_record_selected"
