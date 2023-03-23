import pyaudio
import wave
from recorder import Recorder
class Audio:
    @staticmethod

    def play_voice(path):
        # threading.Thread(target=Recorder.play, args=(path,))
        Recorder.play(path)

    @staticmethod
    def record_voice(time, record_path):
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 512
        RECORD_SECONDS = time
        device_index = 1
        audio = pyaudio.PyAudio()

        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True, input_device_index=device_index,
                            frames_per_buffer=CHUNK)
        Recordframes = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            Recordframes.append(data)
        stream.stop_stream()
        stream.close()
        audio.terminate()
        WAVE_OUTPUT_FILENAME = record_path
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(Recordframes))
        waveFile.close()