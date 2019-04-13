#azure speech recognition sdk
import azure.cognitiveservices.speech as speechsdk

#<azure text-to-speech service>
import os, requests, time
from xml.etree import ElementTree

try: input = raw_input
except NameError: pass
#</azure text-to-speech service>

#<azure computer vision service>
# import requests
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
#</azure computer vision service>

#sound-length calculator
import wave
import contextlib

#pyglet for playing sound
import pyglet

#list to contain detected objects
objects_detected = []

def AzureVision():
    # Replace <Subscription Key> with your valid subscription key.
    subscription_key = "f21b4f194bb1480c8dde294d9baf18e7"
    assert subscription_key

    # You must use the same region in your REST call as you used to get your
    # subscription keys. For example, if you got your subscription keys from
    # westus, replace "westcentralus" in the URI below with "westus".
    #
    # Free trial subscription keys are generated in the "westus" region.
    # If you use a free trial subscription key, you shouldn't need to change
    # this region.
    vision_base_url = "https://southeastasia.api.cognitive.microsoft.com/vision/v2.0/"

    analyze_url = vision_base_url + "detect"

    # Set image_path to the local path of an image that you want to analyze.
    image_path = "image.jpg"

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
                  'Content-Type': 'application/octet-stream'}
    params     = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    #print(analysis)

    #print('TEST : ', analysis['objects']['object'])

    for dicks in analysis['objects']:
        print(dicks['object'])
        objects_detected.append(dicks['object'])


def Vision():
    execution_path = os.getcwd()

    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "image.jpg"), output_image_path=os.path.join(execution_path , "imagenew.jpg"))

    for eachObject in detections:
        # print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
        objects_detected.append(eachObject["name"])

class TextToSpeech(object):
    def __init__(self, subscription_key):
        self.subscription_key = subscription_key

        # self.tts = "In front of you, there are: A spoon, A fork, A knife, A vegetable dish, A beef steak, and A glass of water."

        ###
        text_candidate = "In front of you, there are: "

        for each_object in objects_detected:
            text_candidate = text_candidate + each_object + ', '

        self.tts = text_candidate

        print('Speech output: ' + text_candidate)
        ###

        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

    def get_token(self):
        fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self):
        base_url = 'https://westus.tts.speech.microsoft.com/'
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
        voice.set('name', 'Microsoft Server Speech Text to Speech Voice (en-US, Guy24KRUS)')
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            with open('resultspeech.wav', 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")

        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = "c7468215707f4a53a65709ca3491553b", "westus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

exit_status = 0

while exit_status == 0:
    print("Say something...")

    # Performs recognition. recognize_once() returns when the first utterance has been recognized,
    # so it is suitable only for single shot recognition like command or query. For long-running
    # recognition, use start_continuous_recognition() instead, or if you want to run recognition in a
    # non-blocking manner, use recognize_once_async().
    result = speech_recognizer.recognize_once()

    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        if result.text == "Turn off.":
            exit_status = 1
            sound = pyglet.resource.media('goodbye.wav', streaming=False)
            sound.play()
            time.sleep(3)
        elif result.text == "What's in front of me.":
            AzureVision()
            subscription_key = "c7468215707f4a53a65709ca3491553b"
            app = TextToSpeech(subscription_key)
            app.get_token()
            app.save_audio()
            # time.sleep(5)

            objects_detected = []

            sleep_time = 0
            fname = 'resultspeech.wav'
            with contextlib.closing(wave.open(fname,'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                sleep_time = frames / float(rate)

            sound = pyglet.resource.media('resultspeech.wav', streaming=False)
            sound.play()

            time.sleep(sleep_time)

        elif result.text == "Help.":
            sound = pyglet.resource.media('helpMessage.wav', streaming=False)
            sound.play()
            time.sleep(12)
        else:
            sound = pyglet.resource.media('invalidCommand.wav', streaming=False)
            sound.play()
            time.sleep(7)
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
