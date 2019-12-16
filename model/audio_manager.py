import pyaudio
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5


class AudioManager:
    """
    An audio manager class which allows us to record from a PC mic.
    """

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.data = list()

    def stream_chunk(self, in_data, frame_count, time_info, status) -> tuple:
        """
        Reads in the latest information from the audio stream, stores the results,
        and keeps the stream alive.

        :param in_data: latest data in the buffer
        :param frame_count: the number of frames included in data
        :param time_info: time data
        :param status: streaming status
        :return: the input data and the continue signal as a tuple
        """
        self.data.append(in_data)
        return in_data, pyaudio.paContinue

    def start_recording(self) -> None:
        """
        Begins recording from the mic.

        :return: nothing
        """
        self.stream = self.audio.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK,
                                      stream_callback=self.stream_chunk)

    def stop_recording(self) -> None:
        """
        Stops recording from the mic.

        :return: nothing
        """
        self.stream.stop_stream()
        self.stream.close()

    def close_manager(self) -> None:
        """
        Closes out mic connection.

        :return: nothing
        """
        self.audio.terminate()

    def dump_recording(self) -> None:
        """
        Dumps a recording to the root of the project.
        """
        wave_file = wave.open("../test.wav", 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(self.audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(self.data))
        wave_file.close()
        self.data.clear()
