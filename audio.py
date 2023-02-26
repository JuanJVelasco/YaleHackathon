import pyaudio
import wave

class Audio:
	def __init__():
		self.FORMAT = pyaudio.paInt16
		self.CHANNELS = 1
		self.RATE = 44100
		self.CHUNK = 512
		self.RECORD_SECONDS = 15
		self.WAVE_OUTPUT_FILENAME = "recordedFile.wav"
		self.device_index = 2
		self.audio = pyaudio.PyAudio()

	def get_stream(self):
		pass