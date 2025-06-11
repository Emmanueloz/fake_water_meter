from flet import Page

from enums.events import Events
from service.database import RecordModel
from service.send_socketio import SocketClient


class AppContext:

    _page: Page | None = None
    _listeners: dict[Events, list[callable]] = {}  # type: ignore
    _socket: SocketClient | None = None
    _loop_started: bool = False
    _record_selected: str | None = None

    @classmethod
    def set_record_selected(cls, value: str):
        cls._record_selected = value
        cls._notify_listeners(Events.SET_RECORD_SELECTED, value)

    @classmethod
    def get_record_selected(cls):
        return cls._record_selected

    @classmethod
    def set_loop_started(cls, value: bool):
        cls._loop_started = value
        cls._notify_listeners(Events.SET_LOOP_STARTED, value)

    @classmethod
    def get_loop_started(cls) -> bool:
        return cls._loop_started

    @classmethod
    def set_page(cls, page: Page):
        cls._page = page

    @classmethod
    def get_page(cls) -> Page | None:
        return cls._page

    @classmethod
    def set_socket(cls, host: str, token: str):
        cls._socket = SocketClient(host, token)
        cls._socket.connect()

        print(f"Socket result: {cls._socket.is_connected()}")

        if cls._socket.is_connected():
            cls._notify_listeners(Events.CONNECTION_SUCCESS, "Connected")
        else:
            cls._notify_listeners(Events.CONNECTION_ERROR, "Error")

        if cls._page is not None:
            cls._page.update()

    @classmethod
    def get_socket(cls) -> SocketClient | None:
        return cls._socket

    @classmethod
    def close_socket(cls):
        if cls._socket:
            cls._socket.disconnect()
            cls._socket = None
            cls._notify_listeners(Events.CONNECTION_CLOSED, "Disconnected")

    @classmethod
    def send_data(cls, data: dict):
        if cls._socket:
            ok = cls._socket.send_message(data)
            if ok:
                cls._notify_listeners(Events.SEND_SUCCESS, data)
            else:
                cls._notify_listeners(Events.SEND_ERROR, "Error")

    @classmethod
    def clear_list(cls):
        cls._notify_listeners(Events.CLEAR_LIST)

    @classmethod
    def add_listener(cls, event: Events, callback: callable):  # type: ignore
        if event not in cls._listeners:
            cls._listeners[event] = []
        cls._listeners[event].append(callback)

    @classmethod
    def remove_listener(cls, event: Events, callback: callable):  # type: ignore
        if event in cls._listeners and callback in cls._listeners[event]:
            cls._listeners[event].remove(callback)

    @classmethod
    def _notify_listeners(cls, event: Events, value=None):
        print(cls._listeners)
        print(f"Notifying listeners for event: {event}, value: {value}")

        if event in cls._listeners:
            for callback in cls._listeners[event]:
                callback(value)
            if cls._page is not None:
                cls._page.update()
