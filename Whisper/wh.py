import whisper
from datetime import timedelta
import os
from whisper.utils import get_writer
model = whisper.load_model('medium')

def get_transcribe(audio: str, language: str = 'chinese'):
    return model.transcribe(audio=audio, language=language, verbose=True)

def save_file(results, format='srt'):
    writer = get_writer(format, './output/')
    writer(results, f'transcribe.{format}')

def get_std_srt(segments):
    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"

        srtFilename = os.path.join("SrtFiles", f"VIDEO_FILENAME.srt")
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

if __name__ == "__main__":
    result = get_transcribe(audio='20250217091914.wav')
    print('-'*50)
    print(result.get('text', ''))

    save_file(result, 'srt')
    get_std_srt(result['segments'])
    