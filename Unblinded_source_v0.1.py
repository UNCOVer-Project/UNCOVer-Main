# / / / / / / / / / / / / / / / / / / / / /
#
# UNBLINDED PROTOTYPE SOFTWARE
# v0.1
# Made by Agi, Adhito, Muhammad Teguh, Joshua Evans
#
# / / / / / / / / / / / / / / / / / / / / /


# azure speech recognition sdk
import azure.cognitiveservices.speech as speechsdk

# <azure text-to-speech service>
import os
import requests
import time
from xml.etree import ElementTree

try:
    input = raw_input
except NameError:
    pass
# </azure text-to-speech service>

# <azure computer vision service>
# import requests
# import matplotlib.pyplot as plt
# from PIL import Image
# from io import BytesIO
# </azure computer vision service>

# sound-length calculator
import wave
import contextlib

# pyglet for playing sound
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


def AzureVision(image_path):
    '''
    Azure Computer Vision API

    @param image_path: Set image_path to the local path
        of an image that you want
    to analyze.
    @return: A JSON response in dictionary format
    '''
    print(
        'LOG: Commencing image recognition of '
        + image_path + '\nusing Azure Computer Vision API...'
    )

    # Replace <Subscription Key> with your valid subscription key.
    subscription_key = "f21b4f194bb1480c8dde294d9baf18e7"

    print('LOG: Using vision subscription_key ' + subscription_key)

    assert subscription_key

    # You must use the same region in your REST call as you used to get your
    # subscription keys. For example, if you got your subscription keys from
    # westus, replace "westcentralus" in the URI below with "westus".
    #
    # Free trial subscription keys are generated in the "westus" region.
    # If you use a free trial subscription key, you shouldn't need to change
    # this region.
    vision_base_url = ("https://southeastasia.api.cognitive.microsoft.com/"
                       + "vision/v2.0/")

    print('LOG: Using vision base url ' + vision_base_url)

    # use /detect for object detections
    #
    # other uses can be read at
    # https://westcentralus.dev.cognitive.microsoft.com/docs/services
    # /5adf991815e1060e6355ad44/operations/5e0cdeda77a84fcd9a6d3d0a
    analyze_url = vision_base_url + "detect"

    print('LOG: Reading the image into a byte array...')
    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    print('LOG: Receiving JSON response...')
    # The 'analysis' object (a dictionary) contains various fields that
    # describe the image. The most relevant caption for the image
    # is obtained from the 'description' property.
    analysis = response.json()

    print('LOG: JSON response received...')

    # print the JSON response
    # print(analysis)

    return analysis


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

        self.timestr = time.strftime("%Y%m%d-%H%M")
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

    # function to save the generated speech as .wav audio file
    #
    # @param filename: path and filename to save the audio file
    def save_audio(self, filename):
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


# / / / / / / / / / / / / / / / / / / / / / / /
#
# Main program and speech recognition portion
#
# / / / / / / / / / / / / / / / / / / / / / / /

soundDir = 'sounds/'

# Creates an instance of a speech config with specified subscription key
# and service region.

# Replace with your own subscription key and service region (e.g., "westus").
speech_key, speech_service_region = ("d7f48f6fc6d34d6bae9b72814bbd0519",
                                     "southeastasia")

print('LOG: Using speech subscription key ' + speech_key)
print('LOG: Speech service region at ' + speech_service_region)

speech_config = speechsdk.SpeechConfig(
    subscription=speech_key,
    region=speech_service_region
)

print('LOG: Creating speech recognizer...')

# Creates a speech recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

# boolean for exit status
exit_status = 0

while exit_status == 0:
    print("MIC RECORDING, Say something...")

    # Performs speech recognition.
    # recognize_once() returns when the first utterance has been recognized,
    # so it is suitable only for single shot recognition like command or query.
    # For long-running recognition, use start_continuous_recognition() instead,
    # or if you want to run recognition in a non-blocking manner,
    # use recognize_once_async().
    result = speech_recognizer.recognize_once()

    # Checks speech recognition result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))

        # if the recognized speech is "Turn off.", the program will append
        # after playing goodbye.wav
        if result.text == "Turn off.":
            exit_status = 1

            Pyglet_playSound(soundDir + 'goodbye.wav')

            time.sleep(3)

        # if the recognized speech is "What's in front of me.",
        # start the main recognition sequence and speech output
        elif result.text == "What's in front of me.":
            # perform object recognition
            json_response = AzureVision("image.jpg")

            # list to contain detected objects
            objects_detected = []

            # parse object names from JSON response
            # and append to objects_detected list
            print('LOG: Parsing object names from JSON...')
            for dicts in json_response['objects']:
                print(dicts['object'])
                objects_detected.append(dicts['object'])

            # prepare the text candidate to be converted into speech
            tts_text_candidate = "In front of you, there are: "

            # append each detected objects into the text candidate
            for each_object in objects_detected:
                tts_text_candidate = tts_text_candidate + each_object + ', '

            # subscription key for Azure tts service
            tts_subscription_key = "d7f48f6fc6d34d6bae9b72814bbd0519"

            # begin text-to-speech process using Azure tts service
            app = TextToSpeech(tts_subscription_key, tts_text_candidate)
            app.get_token()
            app.save_audio(soundDir + 'resultspeech')

            # calculate speech audio file duration
            audio_path = soundDir + 'resultspeech.wav'
            sleep_time = Calculate_soundFile_duration(audio_path)

            # play the speech audio file
            # sound = pyglet.resource.media(
            #   'resultspeech.wav', streaming=False
            # )
            # sound.play()
            Pyglet_playSound(audio_path)

            # pause the program while playing the audio file
            time.sleep(sleep_time)

        # if the recognized speech is "Help.", play the 'helpMessage.wav' audio
        elif result.text == "Help.":
            Pyglet_playSound(soundDir + 'helpMessage.wav')

            time.sleep(12)

        # if the recognized speech is other than above strings,
        # play the 'invalidCommand.wav' audio
        else:
            Pyglet_playSound(soundDir + 'invalidCommand.wav')

            time.sleep(7)

    # if no speech is detected/recognized, print the reason
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print(
            "No speech could be recognized: {}"
            .format(result.no_match_details)
        )

    # if speech recognition is canceled or error, print the reason
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(
            "Speech Recognition canceled:"
            + " {}".format(cancellation_details.reason)
        )

        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(
                "Error details: {}"
                .format(cancellation_details.error_details)
            )
