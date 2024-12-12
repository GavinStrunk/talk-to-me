import whisper

class Whisper:
    """
    Requires ffmpeg to be installed. sudo apt install ffmpeg

    References:
        [1] https://github.com/openai/whisper
    """
    def __init__(self,
                 model_size: str = 'base'
                 ):
        self.model_size = model_size
        self.model = whisper.load_model(model_size)

    def convert_audio(self, audio_path):
        text = self.model.transcribe(audio_path)
        print(text)
        return text["text"]



if __name__ == "__main__":
    stt = Whisper()
    audio_file = 'test.mp3'
    print(stt.convert_audio(audio_file))

