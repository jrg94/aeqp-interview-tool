import socket
import threading


class EDAManager:

    # Connection details
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

    # Empatica E4 On/Off
    STREAM_ON = "ON"
    STREAM_OFF = "OFF"

    COMMAND_SEPARATOR = "|"

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data = list()
        self.stream_thread = threading.Thread(target=self._stream_data)

    def start_recording(self):
        self.socket.connect((EDAManager.LOCALHOST, EDAManager.PORT))
        devices = self._get_devices()
        device_id = devices[0].split(" ")[0]
        is_connected = self._connect_device(device_id)
        if is_connected:
            self._subscribe_stream(EDAManager.BLOOD_VOLUME_PULSE)
            self.stream_thread.start()

    def stop_recording(self):
        self.stream_thread.join()
        self.socket.close()

    def _stream_data(self):
        raw_data = self.socket.recv(1024)
        while raw_data != "":
            raw_data = self.socket.recv(1024)
            raw_data_list = raw_data.decode("utf-8").splitlines()
            for sample in raw_data_list:
                items = sample.split(" ")
                self.data.append({
                    "type": items[0],
                    "time": items[1],
                    "value": items[2:]
                })
                print(self.data[-1])

    @staticmethod
    def _construct_command(command, *args) -> bytes:
        """
        Constructs an E4 command given the command and a set of arguments.

        :param command: the action to be performed (e.g. LIST_DEVICES_COMMAND, CONNECT_DEVICE_COMMAND, etc.)
        :param args: a list of potential arguments to pass to alongside the command
        :return: the resulting command as a set of bytes
        """
        return bytes(f'{command} {" ".join(args)}\r\n', 'utf-8')

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

    def _connect_device(self, device_id: str) -> bool:
        """
        A helper method which connects to a specific device by ID

        :param device_id: the ID of the device we want to connect to
        :return: a boolean indicating whether or not the connection was successful
        """
        device_connect_command = EDAManager._construct_command(EDAManager.CONNECT_DEVICE_COMMAND, device_id)
        self.socket.sendall(device_connect_command)
        response = self.socket.recv(1024).decode("utf-8")
        status_code = response.strip().split(" ")[2]
        return True if status_code == EDAManager.STATUS_CODE_OK else False

    def _subscribe_stream(self, stream: str) -> bool:
        """
        Subscribes to a stream of data from a device.

        :param stream: a data stream abbreviation according to documentation (e.g. BLOOD_VOLUME_PULSE)
        :return: True if the subscription was successful
        """
        stream_subscribe_command = EDAManager._construct_command(
            EDAManager.STREAM_SUBSCRIBE_COMMAND,
            stream,
            EDAManager.STREAM_ON
        )
        self.socket.sendall(stream_subscribe_command)
        response = self.socket.recv(1024).decode("utf-8")
        status_code = response.strip().split(" ")[3]
        return True if status_code == EDAManager.STATUS_CODE_OK else False


manager = EDAManager()
manager.start_recording()
manager.stop_recording()
