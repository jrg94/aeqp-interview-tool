from audio_manager import AudioManager
import time

audio = AudioManager()
audio.start_recording()
time.sleep(5)
audio.stop_recording()
audio.close_manager()
audio.dump_recording()
