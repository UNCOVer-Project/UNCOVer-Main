# Libs for text-to-speech
# import os
import requests
from xml.etree import ElementTree

# Libs for sound-length calculator
import wave
import contextlib

# Libs to play sound
import pyglet


def Pyglet_playSound(file_path):
    '''
    Play sound file using pyglet module
    dependency: pyglet

    @param file_path: path to the audio file
    '''
    print('LOG: Playing audio file: ' + file_path + '...')

    sound = pyglet.resource.media(file_path, streaming=False)
    sound.play()

    print('LOG: Done playing!')


def Calculate_soundFile_duration(file_path):
    '''
    Algorithm to calculate duration of a sound file
    dependency: wave, contextlib

    @param file_path: Path to the sound file
    @return: time in seconds (integer)
    '''
    print('LOG: Calculating duration of ' + file_path + '...')
    with contextlib.closing(wave.open(file_path, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        time_ = frames / float(rate)

    print('LOG: Done calculating!')

    return time_


class ObjectDetection(object):
    def __init__(self, subscription_key, image_path):
        self.subscription_key = subscription_key
        self.image_path = image_path

    def DetectObject(self):
        '''
        Azure Computer Vision API

        @param image_path: Set image_path to the local path
            of an image that you want
        to analyze.
        '''
        print(
            'LOG: Commencing image recognition of '
            + self.image_path + '\nusing Azure Computer Vision API...'
        )

        subscription_key = self.subscription_key

        print('LOG: Using vision subscription_key ' + subscription_key)

        assert subscription_key

        vision_base_url = ("https://southeastasia.api.cognitive.microsoft.com/"
                           + "vision/v2.0/")

        print('LOG: Using vision base url ' + vision_base_url)

        analyze_url = vision_base_url + "detect"

        print('LOG: Reading the image into a byte array...')

        # Read the image into a byte array
        image_data = open(self.image_path, "rb").read()

        headers = {'Ocp-Apim-Subscription-Key': subscription_key,
                   'Content-Type': 'application/octet-stream'}
        params = {'visualFeatures': 'Categories,Description,Color'}
        response = requests.post(
            analyze_url, headers=headers, params=params, data=image_data)
        response.raise_for_status()

        print('LOG: Receiving JSON response...')

        self.result = response.json()

        print('LOG: JSON response received...')

    def getDetectedObject(self):
        result = self.result

        objects_detected = []
        # # parse object names from JSON response
        print('LOG: Parsing object names from JSON...')
        for dicts in result['objects']:
            object_name = dicts['object']
            object_pos = []
            for i in dicts['rectangle']:
                object_pos.append(dicts['rectangle'][i])

            objects_detected.append((object_name, object_pos))

        return objects_detected


# Azure text-to-speech service
class TextToSpeech(object):
    '''
    constructor for TextToSpeech object

    @param subscription_key: change to tts subscription_key
    @param text_candidate: text/string to be converted to speech audio file
    '''
    def __init__(self, subscription_key, text_candidate):
        print('LOG: Initializing TextToSpeech object...')
        print('LOG: Using speech subscription_key ' + subscription_key)

        self.subscription_key = subscription_key

        self.tts = text_candidate

        print('LOG: Speech output: ' + text_candidate)

        self.access_token = None

    def get_token(self):
        print('LOG: Getting token...')

        fetch_token_url = ("https://southeastasia.api.cognitive.microsoft.com"
                           + "/sts/v1.0/issueToken")

        print('LOG: Fetching token at ' + fetch_token_url)

        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self, filename):
        '''
        function to save the generated speech as .wav audio file

        @param filename: path and filename to save the audio file
        '''

        print('LOG: Processing audio...')

        base_url = 'https://southeastasia.tts.speech.microsoft.com/'

        print('LOG: Using speech base url ' + base_url)

        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set(
            'name',
            'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)'
        )
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            print('LOG: Saving audio as ' + filename + '...')

            with open(filename + '.wav', 'wb') as audio:
                audio.write(response.content)
                print(
                    "\nStatus code: "
                    + str(response.status_code)
                    + "\nYour TTS is ready for playback.\n"
                )

        else:
            print(
                "\nStatus code: "
                + str(response.status_code)
                + "\nSomething went wrong. "
                + "Check your subscription key and headers.\n"
            )


soundDir = 'sounds/'

# perform object recognition
subKey = 'f21b4f194bb1480c8dde294d9baf18e7'
objectDetect = ObjectDetection(subKey, 'image.jpg')
objectDetect.DetectObject()
objects = objectDetect.getDetectedObject()
print(objects)
object_names = [i[0] for i in objects]
print(object_names)

# tts_subscription_key = "d7f48f6fc6d34d6bae9b72814bbd0519"
# tts_text_candidate = "In front of you, there are: "
#
# # append each detected objects into the text candidate
# for each_object in object_names:
#     tts_text_candidate = tts_text_candidate + each_object + ', '
#
# # begin text-to-speech process using Azure tts service
# app = TextToSpeech(tts_subscription_key, tts_text_candidate)
# app.get_token()
# app.save_audio(soundDir + 'resultspeech')
#
# # calculate speech audio file duration
# audio_path = soundDir + 'resultspeech.wav'
# sleep_time = Calculate_soundFile_duration(audio_path)
#
# # play the speech audio file
# Pyglet_playSound(audio_path)
#
# # pause the program while playing the audio file
# time.sleep(sleep_time)
