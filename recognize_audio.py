import os

from pathlib import Path

import speech_recognition as sr
from pydub import AudioSegment

from audio_models import create, read, connect_to_db
from translate_text import translate

from utilities.utils import my_str

os.environ["PATH"] += os.pathsep + R"E:\games\ffmpeg-2022-06-30-git-03b2ed9a50-full_build\bin"


def recognize_audio_file(mp3_file: Path, out_dir: Path):
    """Recognize one mp3 audiofile."""
    print(F"{out_dir=}")
    # convert mp3  to wav
    audio = AudioSegment.from_mp3(mp3_file)
    wav_file = out_dir / mp3_file.with_suffix('.wav').name
    print(F"{wav_file=}, \n {str(wav_file.resolve())=}")
    audio.export(wav_file, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(str(wav_file.resolve())) as source:
        audio = recognizer.record(source)  # read the entire audio file

    text_ru = F'Файл {mp3_file} не вдалося розпізнати.'
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use
        # `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text_ru = recognizer.recognize_google(audio, language='ru-RU')
        print(F"Google Speech Recognition thinks you said:  {text_ru}")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as ex:
        print(F"Could not request results from Google Speech Recognition service; {ex}")

    return text_ru


def recognize_any_audio_file(audio_file: Path, file_format: str, out_dir: Path):
    """Recognize one audiofile of 'file_format' format."""
    # convert audiofile  to wav  [mov,mp4,m4a,3gp,3g2,mj2]
    
    if file_format == 'mp3':
        print(20*'*.mp3')
        audio = AudioSegment.from_mp3(audio_file)
    else:
        audio = AudioSegment.from_file(audio_file, format=file_format)

    wav_file = out_dir / audio_file.with_suffix('.wav').name
    print(F"{wav_file=}, \n {str(wav_file.resolve())=}")

    audio.export(wav_file, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(str(wav_file.resolve())) as source:
        audio = recognizer.record(source)  # read the entire audio file

    text_ru = F'Файл {audio_file} не вдалося розпізнати.'
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use
        # `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text_ru = recognizer.recognize_google(audio, language='ru-RU')
        print(F"Google Speech Recognition thinks you said:  {text_ru}")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as ex:
        print(F"Could not request results from Google Speech Recognition service; {ex}")

    return text_ru


def recognize_audio_in_folder(state_pars: dict):
    """Recognize mp3 & m4a   audio in folder."""
    mp3_folder = Path(state_pars['dirs']['dir_audiofiles']['dir_path'])
    # folder for workout files
    wavs_dir = mp3_folder / 'wavs'
    wavs_dir.mkdir(exist_ok=True)
    print(F"{wavs_dir=}")

    df_cursor = connect_to_db().cursor()

    audio_types = ('.m4a', '.mp3')
    #   NOT !!! fromdict(audio_types, [])  --->   the same list for all keys.
    mp3_m4a = {key: [] for key in audio_types}    # {'.mp3':[], '.m4a':[]} 
    
    for f in mp3_folder.iterdir():
        if f.suffix in audio_types:
            mp3_m4a[f.suffix].append(f) 

    for key_type, files_list in mp3_m4a.items():
        print(F'{key_type=} and {files_list=}')
        if not files_list:
            continue
        for audio_file in files_list:
            if read(
                'audiofiles',  'audiofile_name',
                conditions=F'audiofile_name == "{my_str(audio_file.name)}" ',
                cursor=df_cursor
            ):
                continue

            rus_text_rcognized = recognize_any_audio_file(audio_file, key_type[1:], wavs_dir)
            rus_text_translated_to_ukr = translate(rus_text_rcognized)
            create(
                'audiofiles',
                ['audiofile_name', 'recognized_rus_text', 'rus_text_translated_to_ukr', ],
                (my_str(audio_file.name), rus_text_rcognized, rus_text_translated_to_ukr)
            )


if __name__ == '__main__':
    mp3folder = Path(R"E:\games\audio")
    recognize_audio_in_folder({'dir_audiofiles': mp3folder})
