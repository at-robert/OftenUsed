import whisper
from whisper.utils import get_writer
model = whisper.load_model('medium')

def get_transcribe(audio: str, language: str = 'en'):
    return model.transcribe(audio=audio, language=language, verbose=True)

def save_file(results, format='tsv'):
    writer = get_writer(format, './output/')
    writer(results, f'transcribe.{format}')

if __name__ == "__main__":
    result = get_transcribe(audio='Baby Come Back.mp3')
    print('-'*50)
    print(result.get('text', ''))

    save_file(result, 'srt')