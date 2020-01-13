import socket


class EDAManager:

    LIST_DEVICES_COMMAND = "device_list"
    CONNECT_DEVICE_COMMAND = "device_connect"

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @staticmethod
    def _construct_command(command, *args) -> bytes:
        return bytes(f'{command}{" ".join(args)}"\r\n"')

    def _list_devices(self):
        self.socket.sendall(EDAManager._construct_command(EDAManager.LIST_DEVICES_COMMAND))
