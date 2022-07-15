"""Module docstring."""
import os
import shutil

from pathlib import Path
from typing import List

import math

import speech_recognition as sr
from pydub import AudioSegment

from audio_models import create, read, connect_to_db
from translate_text import translate

from utilities.utils import my_str

os.environ["PATH"] += os.pathsep + R"E:\games\ffmpeg-2022-06-30-git-03b2ed9a50-full_build\bin"

def convert_audio_to_wav(audio_file: Path, out_dir: Path) -> Path:
    """Comvert audio to wav."""
    wav_file = out_dir / audio_file.with_suffix('.wav').name

    file_format = audio_file.suffix[1:].lower()
    if file_format == 'wav':        # just copying
        shutil.copy(audio_file, wav_file)
    else:
        if file_format == 'mp3':
            print('*.mp3 ! ' + 20*'._.')
            audio = AudioSegment.from_mp3(audio_file)
        else:
            audio = AudioSegment.from_file(audio_file, format=file_format)
        audio.export(wav_file, format="wav")

    print(F"{wav_file=}, \n {str(wav_file.resolve())=}")
    return wav_file

class SplitWavTimed():
    """Split wav-file into timed chunks.

        Inspired by:
        https://stackoverflow.com/questions/37999150/how-to-split-a-wav-file-into-multiple-wav-files
    """
    def __init__(self, audio_file_path: Path, folder_to: Path, chunk_duration_in_mins=4):
        self.audio_file_path = audio_file_path
        self.folder_to = folder_to
        self.chunk_duration_in_mins = chunk_duration_in_mins
        self.audio = AudioSegment.from_wav(self.audio_file_path)

    def get_duration(self):
        """Get duration."""
        return self.audio.duration_seconds

    def single_split(self, from_min: int, to_min: int) -> Path:
        """Do split from 'from_min' minute to 'to_min' minute.

        Args:
            from_min (int): Start chunk minute
            to_min (int): End chunk minute

        Returns:
            Path: Chunk splited file.
        """
        from_ms = from_min * 60 * 1000
        to_ms = to_min * 60 * 1000
        split_audio = self.audio[from_ms : to_ms]
        out_file = self.folder_to / "".join(
            [self.audio_file_path.stem, str(from_min).zfill(2), str(to_min).zfill(2), '.wav']
            )
        split_audio.export(out_file, format="wav")
        return out_file

    def multiple_split(self) -> List[Path]:
        """Split audio file into chunks.

        Returns:
            List[Path]: List of chunks files.
        """
        total_mins = math.ceil(self.get_duration() / 60)
        mins_per_split = self.chunk_duration_in_mins

        chunks = []
        for i in range(0, total_mins, mins_per_split):
            chunk_file = self.single_split(i, i+mins_per_split)
            chunks.append(chunk_file)
            print(F"{str(chunk_file)} done. Total duration is {total_mins} minutes.")

        print(40*'--')
        return chunks


def recognize_any_audio_file(audio_file: Path, out_dir: Path):
    """Recognize one audiofile of 'file_format' format."""
    # convert audiofile  to wav  [mov,mp4,m4a,3gp,3g2,mj2]
    wav_file = convert_audio_to_wav(audio_file, out_dir)

    # split *.wav  into timed chunks
    spliter = SplitWavTimed(wav_file, out_dir, chunk_duration_in_mins=4)
    all_waw_parts = spliter.multiple_split()

    # recognise chunks and concatenate text parts
    text_parts = []
    for wav_file in all_waw_parts:
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

        text_parts.append(text_ru)

    all_text_ru = ''.join(text_parts)

    return all_text_ru


def recognize_audio_in_folder(state_pars: dict):
    """Recognize mp3 & m4a   audio in folder."""
    df_cursor = connect_to_db().cursor()

    mp3_folder = Path(state_pars['dirs']['dir_audiofiles']['dir_path'])
    # folder for workout files
    wavs_dir = mp3_folder / 'wavs'
    wavs_dir.mkdir(exist_ok=True)
    print(F"{wavs_dir=}")

    audio_types = ('.m4a', '.mp3')
    mp3_m4a = {key: [] for key in audio_types}    # {'.mp3':[], '.m4a':[]}
    for file in mp3_folder.iterdir():
        if file.suffix in audio_types:
            mp3_m4a[file.suffix].append(file)

    for key_type, files_list in mp3_m4a.items():
        print(F'{key_type=} and {files_list=}')
        if not files_list:
            continue
        for audio_file in files_list:
            # skip the fike if file with this name has been recognized previously
            if read(
                'audiofiles',  'audiofile_name',
                conditions=F' audiofile_name == "{my_str(audio_file.name)}" ',
                cursor=df_cursor
            ):
                continue

            rus_text_rcognized = recognize_any_audio_file(audio_file, wavs_dir)
            rus_text_translated_to_ukr = translate(rus_text_rcognized)
            # store recognized text to DB
            create(
                'audiofiles',
                ['audiofile_name', 'recognized_rus_text', 'rus_text_translated_to_ukr', ],
                (my_str(audio_file.name), rus_text_rcognized, rus_text_translated_to_ukr)
            )


if __name__ == '__main__':
    mp3folder = Path(R"E:\games\audio")
    recognize_audio_in_folder({'dir_audiofiles': mp3folder})
