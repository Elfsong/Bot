# coding: utf-8

import os
import re
import sys
from tqdm import tqdm
from playsound import playsound
from google.cloud import texttospeech

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    path = os.path.join(base_path, relative_path)
    print(path)

    return path

# Set up GOOGLE_APPLICATION_CREDENTIALS
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = resource_path('./data/lucky-re-4babc7875c8c.json')

class TTS():
    def __init__(self):
        # Instantiates a client
        self.client = texttospeech.TextToSpeechClient()

    def tts(self, text, output):
        # Set the text input to be synthesized
        # synthesis_input = texttospeech.SynthesisInput(text=text)

        # # Build the voice request, select the language code ("en-US") and the ssml voice gender ("neutral")
        # voice = texttospeech.VoiceSelectionParams(
        #     language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        # )

        # # Select the type of audio file you want returned
        # audio_config = texttospeech.AudioConfig(
        #     audio_encoding=texttospeech.AudioEncoding.MP3
        # )

        # # Perform the text-to-speech request on the text input with the selected
        # # voice parameters and audio file type
        # response = self.client.synthesize_speech(
        #     input=synthesis_input, voice=voice, audio_config=audio_config
        # )

        # with open(output, "wb") as out:
        #     # Write the response to the output file.
        #     out.write(response.audio_content)
        #     # print("Audio content written to file", output)
        
        return output

class ScriptLine(object):
    def __init__(self, content, actor=None, audio=None, movement=None):
        self.content = content
        self.actor = actor
        self.audio = audio
        self.movement = movement

    def play_audio(self):
        playsound(self.audio)
    
    def need_play_audio(self):
        return True if self.audio else False

class ScriptReader(object):
    def __init__(self):
        self.tts_worker = TTS()
        self.script_lines = list()
        self.need_vioce = ["Pam-Medic"]
        self.sound_storge_path = "/Users/elfsong/Projects/Bot/data/sounds/"
        self.script_storge_path = "/Users/elfsong/Projects/Bot/data/scripts/"

    def get_sound_storge_path(self, line_id):
        return self.sound_storge_path + line_id + ".mp3"

    def process_script(self, script_name):
        with open(self.script_storge_path + script_name, "r") as raw_script:
            for index, line in tqdm(enumerate(raw_script.readlines())):
                # Regular Expression
                try:
                    actor_re = re.compile('\[(.*?)\]').findall(line)
                    movement_re = re.compile('[(](.*?)[)]').findall(line)
                    content_re = re.compile('(?<=:).*').findall(line)
                    actor = actor_re[0] if actor_re else None
                    movement = movement_re[0] if movement_re else None
                    content = content_re[0] if content_re else None
                except:
                    print("Script is in wrong format!")
                
                # Generate line_id
                line_id = script_name + "_" + str(index)

                # Generate audio file if needed
                audio = None
                if actor in self.need_vioce:
                    audio = self.tts_worker.tts(content, self.get_sound_storge_path(line_id))
                
                # Construct script line instance
                line = ScriptLine(content, actor, audio, movement)

                self.script_lines.append(line)
    
    def get_script_lines(self):
        return self.script_lines

class BOT(object):
    def __init__(self, bot_name):
        self.name = bot_name
        self.script_reader = ScriptReader()
        self.memory = dict()

    def set_current_line_index(self, line_index):
        self.memory["current_line_index"] = line_index

    def get_current_line_index(self):
        return self.memory["current_line_index"]

    def has_next_line(self):
        return True if self.memory["script_line_len"] > self.memory["current_line_index"] else False

    def load_lines_to_memory(self, script_line):
        self.memory["script_line"] = script_line
        self.memory["script_line_len"] = len(script_line)
        self.set_current_line_index(0)

    def load_script(self, script_name):
        # Process script
        print("Processing script %s ..." % (script_name))
        self.script_reader.process_script(script_name)

        # Load script to memory
        print("Loading script %s to memory..." % (script_name))
        self.load_lines_to_memory(self.script_reader.get_script_lines())


if __name__ == "__main__":
    bot = BOT("NAO")
    bot.reharse("script_1")