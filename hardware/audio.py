# import sounddevice as sd
#
# class Microphone:
#     """
#     The microphone class finds the available microphones and records the audio.
#
#     """
#     def __init__(self):
#         pass
#
# if __name__ == "__main__":
#     # Settings
#     duration = 5  # seconds
#     sample_rate = 44100  # Hz
#     channels = 1  # Mono
#
#     # List devices
#     print(sd.query_devices())
#
#     print("Recording...")
#
#     # Record audio
#     audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16')
#     sd.wait()  # Wait for recording to finish
#
#     print("Recording finished!")
#
#     # Play the audio
#     print('Playing audio...')
#     sd.play(audio_data)
#     sd.wait()
import sounddevice as sd
import numpy as np
import webrtcvad
import speech_recognition as sr

def record_until_pause(sample_rate=16000, duration=10, aggressiveness=3):
    """
    Record audio until a pause is detected.

    Args:
        sample_rate (int): The sample rate for recording.
        duration (int): Maximum recording duration in seconds.
        aggressiveness (int): WebRTC VAD aggressiveness level (0-3).

    Returns:
        np.ndarray: Recorded audio data.
    """
    vad = webrtcvad.Vad(aggressiveness)
    audio_data = []
    print("Listening for speech...")

    def callback(indata, frames, time, status):
        nonlocal audio_data
        if status:
            print("Error:", status)
        audio_data.extend(indata[:, 0].tolist())

    with sd.InputStream(samplerate=sample_rate, channels=1, callback=callback):
        for _ in range(int(sample_rate / 100 * duration)):  # Process in 10ms frames
            frame = np.array(audio_data[-int(sample_rate / 100):], dtype=np.int16).tobytes()
            if len(frame) < 320:  # Minimum frame size
                continue
            if not vad.is_speech(frame, sample_rate):
                print("Pause detected, stopping recording.")
                break

    return np.array(audio_data, dtype=np.float32)


def listen_for_keyword(keyword="dummy"):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print(f"Waiting for keyword '{keyword}'...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio).lower()
                if keyword in text:
                    print(f"Keyword '{keyword}' detected!")
                    return True
            except sr.UnknownValueError:
                print("Could not understand audio, retrying...")
            except sr.RequestError as e:
                print(f"Speech Recognition error: {e}")


if __name__ == "__main__":
    """
    Had to install sudo apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev
    poetry add pyaudio

    """
    # Step 1: Wait for the keyword
    if listen_for_keyword():
        # Step 2: Record audio until a pause
        recorded_audio = record_until_pause()
        print(f"Recorded {len(recorded_audio)} samples.")

        print("Playing audio...")
        sd.play(recorded_audio, samplerate=16000)
        sd.wait()