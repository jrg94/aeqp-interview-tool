import socket


class EDAManager:

    LOCALHOST = "127.0.0.1"
    PORT = 28000

    # Empatica E4 Commands
    LIST_DEVICES_COMMAND = "device_list"
    CONNECT_DEVICE_COMMAND = "device_connect"
    DISCONNECT_DEVICE_COMMAND = "device_disconnect"
    STREAM_SUBSCRIBE_COMMAND = "device_subscribe"

    # Empatica E4 Streams
    THREE_AXIS_ACCELERATION = "acc"
    BLOOD_VOLUME_PULSE = "bvp"
    GALVANIC_SKIN_RESPONSE = "gsr"
    INTERBEAT_INTERVAL_AND_HEARTRATE = "ibi"
    SKIN_TEMPERATURE = "tmp"
    DEVICE_BATTERY = "bat"
    DEVICE_TAG = "tag"

    # Empatica E4 Status Codes
    STATUS_CODE_ERR = "ERR"
    STATUS_CODE_OK = "OK"

    COMMAND_SEPARATOR = "|"

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_recording(self):
        self.socket.connect((EDAManager.LOCALHOST, EDAManager.PORT))

    def stop_recording(self):
        self.socket.close()

    @staticmethod
    def _construct_command(command, *args) -> bytes:
        return bytes(f'{command}{" ".join(args)}\r\n', 'utf-8')

    def _get_devices(self) -> list:
        """
        A helper method which returns a list of devices connected to the EDA server.

        :return: a list of devices (e.g. ['6D4ACD Empatica_E4'])
        """
        device_list_command = EDAManager._construct_command(EDAManager.LIST_DEVICES_COMMAND)
        self.socket.sendall(device_list_command)
        response = self.socket.recv(1024).decode("utf-8")
        devices = list(map(str.strip, response.split(EDAManager.COMMAND_SEPARATOR)[1:]))
        return devices

    def _connect_device(self, device_id) -> bool:
        device_connect_command = EDAManager._construct_command(EDAManager.CONNECT_DEVICE_COMMAND, device_id)
        self.socket.sendall(device_connect_command)
        response = self.socket.recv(1024).decode("utf-8")
        status_code = response.split(" ")[2]
        return True if status_code == EDAManager.STATUS_CODE_OK else False

manager = EDAManager()
manager.start_recording()
print(manager._get_devices())
manager.stop_recording()
