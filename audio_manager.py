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
        self.data = list()

    def stream_chunk(self, in_data, frame_count, time_info, status):
        self.data.append(in_data)
        return in_data, pyaudio.paContinue

    def start_recording(self):
        self.stream = self.audio.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK,
                                      stream_callback=self.stream_chunk)

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()

    def close_manager(self):
        self.audio.terminate()

    def dump_recording(self):
        wave_file = wave.open("test.wav", 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(self.audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(self.data))
        wave_file.close()
        self.data.clear()
