import socket


class EDAManager:

    LOCALHOST = "127.0.0.1"
    PORT = 28000
    LIST_DEVICES_COMMAND = "device_list"
    CONNECT_DEVICE_COMMAND = "device_connect"
    COMMAND_SEPARATOR = "|"

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_recording(self):
        self.socket.connect((EDAManager.LOCALHOST, EDAManager.PORT))

    @staticmethod
    def _construct_command(command, *args) -> bytes:
        return bytes(f'{command}{" ".join(args)}"\r\n"')

    def _get_devices(self) -> list:
        """
        A helper method which returns a list of devices connected to the EDA server.

        :return: a list of devices
        """
        self.socket.sendall(EDAManager._construct_command(EDAManager.LIST_DEVICES_COMMAND))
        command = str(self.socket.recv(1024))
        devices = command.split(EDAManager.COMMAND_SEPARATOR)[1:]
        return devices

