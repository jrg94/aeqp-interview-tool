import pyaudio  # Needed Visual C++ 14.0 for this
import wave

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5


class AudioManager:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def start(self):
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                      rate=RATE, input=True,
                                      frames_per_buffer=CHUNK)

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
