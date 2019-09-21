import os
import time
import subprocess
from abc import ABC, abstractmethod

import ffmpeg
from pydub import AudioSegment
import tempfile
from gtts import gTTS
import speech_recognition as sr


class AbstaractMethod(ABC):
    def __init__(self, bot):
        self.bot = bot

    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def send(self):
        pass


class T2S(AbstaractMethod):
    def __init__(self, bot):
        super().__init__(bot)
        self.file = tempfile.NamedTemporaryFile(suffix='.ogg', delete=False)

    @staticmethod
    def _transform(text='hello', lang='ru', filename='tmp'): #, frmt='mp3'
        gTTS(text=text, lang=lang).save(filename) # .{frmt}'

    def transform(self, text):
        self._transform(text=text, filename=self.file.name)
        self.file.close()
        return self

    def send(self, chat_id):
        try:
            with open(self.file.name, 'rb') as audio:
                self.bot.send_audio(chat_id, audio)
            os.remove(self.file.name)
            return 'File'
        except Exception as error:
            self.bot.send_message(chat_id, str(error))
            return str(error)


class S2T(AbstaractMethod):
    def __init__(self, bot):
        super().__init__(bot)
        self.infile = tempfile.NamedTemporaryFile(suffix='.ogg', delete=False)
        self.outfile = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        self.outfile.close()

    def _download(self, file_id):
        file = self.bot.get_file(file_id)
        data = self.bot.download_file(file.file_path)
        self.infile.write(data)
        self.infile.close()

    @staticmethod
    def _convert(infile, outfile):
        AudioSegment.from_file(infile).export(outfile, format='wav')
        #ffmpeg.input(infile).output(outfile).run()        

    @staticmethod
    def _transform(filename, language='ru-RU'):
        recognizer = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
            return recognizer.recognize_google(audio, language=language)

    def transform(self, file_id):
        try:
            self._download(file_id)
            self._convert(self.infile.name, self.outfile.name)
            self.text = self._transform(self.outfile.name)
        except Exception as error:
            self.text = str(error)
        return self

    def send(self, chat_id):
        self.bot.send_message(chat_id, self.text)
        os.remove(self.infile.name)
        os.remove(self.outfile.name)
        return self.text