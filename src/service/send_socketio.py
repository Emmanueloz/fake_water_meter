import socketio
import logging
from typing import Callable
from enum import Enum, auto


class ConnectionState(Enum):
    DISCONNECTED = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    AUTH_FAILED = auto()  # No se puede conectar al namespace


class SocketClient:
    """
    Cliente Socket.IO simplificado con manejo confiable de conexión/desconexión
    """

    def __init__(self, server_url: str, access_token: str):
        self.server_url = server_url
        self.access_token = access_token
        self.sio = None
        self.state = ConnectionState.DISCONNECTED
        self.logger = self._setup_logger()
        self._connect_timeout = 5

    def _setup_logger(self):
        logger = logging.getLogger("SocketIOReceiveClient")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def connect(self):
        if self.state not in [ConnectionState.DISCONNECTED, ConnectionState.AUTH_FAILED]:
            return

        self.state = ConnectionState.CONNECTING
        self.logger.info("Iniciando conexión...")

        try:
            self.sio = socketio.Client(
                reconnection=False,
                logger=False,
                engineio_logger=False
            )

            # Configurar solo los eventos necesarios
            self.sio.on('connect', self._on_connect, namespace='/receive/')
            self.sio.on('disconnect', self._on_namespace_disconnect,
                        namespace='/receive/')
            self.sio.on('message', self._on_message, namespace='/receive/')

            headers = {'ACCESS_TOKEN': self.access_token}

            self.sio.connect(
                self.server_url,
                namespaces=['/receive/'],
                headers=headers,
                wait_timeout=self._connect_timeout,
                transports=['websocket']
            )

        except Exception as e:
            self.logger.error(f"Error de conexión: {str(e)}")
            self.state = ConnectionState.DISCONNECTED

    def disconnect(self):
        if self.sio:
            try:
                self.sio.disconnect()
            except Exception as e:
                self.logger.error(f"Error al desconectar: {str(e)}")
            finally:
                self.state = ConnectionState.DISCONNECTED

    def send_message(self, data: dict) -> bool:
        if not self.is_connected():
            self.logger.warning(
                "Intento de enviar mensaje sin conexión válida")
            return False

        try:
            self.sio.emit('message', data, namespace='/receive/')
            return True
        except Exception as e:
            self.logger.error(f"Error al enviar mensaje: {str(e)}")
            self.state = ConnectionState.DISCONNECTED
            return False

    def _on_connect(self):
        """Conexión al namespace exitosa"""
        if self.state != ConnectionState.AUTH_FAILED:
            self.state = ConnectionState.CONNECTED
            self.logger.info("Conexión autenticada y establecida en /receive/")

    def _on_namespace_disconnect(self):
        """Desconexión del namespace (siempre actualiza el estado)"""
        self.state = ConnectionState.AUTH_FAILED
        self.logger.info("Desconectado del namespace /receive/")
        self.disconnect()

    def _on_message(self, data):
        """Manejador de mensajes recibidos"""
        self.logger.debug(f"Mensaje recibido: {data}")

    def is_connected(self) -> bool:
        return self.state == ConnectionState.CONNECTED

    def set_message_handler(self, handler: Callable):
        if self.sio:
            self.sio.on('message', handler, namespace='/receive/')
