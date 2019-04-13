# UNCOVer : UNsighted COmputer Vision


## BACKGROUND

  

![A blind person](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQehofMIx7HhACfNghBfVM7tU__QfUqTxsR8VzzQWSPFsmwA25m)

  

<sup>*Image: A blind person*</sup>

  

Blind people are people who have complete or nearly complete vision loss and may result in difficulties in daily life routines such as walking, socialising and reading. As of 2015 there were 940 million people with some degree of vision loss (Collaborators 2015)<sup>1</sup>. Blind people do lead a normal life with their own style of doing things. But, they definitely face troubles due to inaccessible infrastructure and social challenges.

  

According to Erin Brady et al., the most common accessibility issues encountered in everyday life is Identification, making up 41% of the total sample. More than half of Identification questions were simple, “No Context” questions (58%) where the user did not provide any information about the subject of the object (Brady et al. 2013)<sup>2</sup>.

  

Other problems that is faced by blind people are locating an object. Popular culture depicts that if one of the senses of a person stops working, the others become sharper. Blind people may rely more on their other senses and develop a strong memory, but this may not be well enough to identify object and their location. Blind people must memorise the location of every obstacle or item in their home environment. Any changes in location can put burden to the person to search the item again with varying difficulties.

  

Despite the challenges faced by the blind, the most valuable thing for a disabled person is gaining independence. A blind person can lead an independent life with some specifically designed adaptive things for them. There are lots of adaptive equipment that can enable a blind person to live their life independently but they are not easily available in the local shops or markets. They have to put much effort to get each equipment that can take them one step closer towards independence (Kumar 2018)<sup>3</sup>.

  

Computers and the Internet are two of the most significant developments since the invention of braille, as for the first time ever many blinds and partially sighted people have access to the same wealth of information as sighted people and on the same terms. Computing technology is promising greater accessibility to information, services, and society. (Jarry et al. 2017)<sup>4</sup>.

  

With the premise above, we came up with a powerful and easy-to-use solution for the blind to identify and discover the location of objects that we called **"UNCOVer: UNsighted COmputer Vision"**

  

## What is UNCOVer

  

UNCOVer is an accessibility tool for the sightless person that is worn like sunglasses. UNCOVer will use the technology of Artificial Intelligence to aid the user in identifying and locating objects and texts accurately.

  

![UNCOVer illustration](https://raw.githubusercontent.com/agikarasugi/HackMyLife/master/HackMyLifeGraphic/UNBLINDED%20concept_smaller.png)

  

<sup>*Image: UNCOVer product illustration*</sup>

  

UNCOVer differentiates itself from the currently available products by offering multiple object detection complete with object name and location, powerful and precise object description by detecting the object pointed by the user's finger, and optical character recognition that enables the user to "hear" the characters, all in a single, easy-to-use package, and reasonable price within reach of many people.

  

<img  src="https://raw.githubusercontent.com/UNCOVer-Project/UNCOVer-Main/common/HackMyLifeGraphic/UNCOVer%20-%20Components.jpg"  width="1000">

  

<sup>*Image: UNCOVer prototype working components*</sup>

  

UNCOVer core components consists of a single camera positioned to mimic user's field of view. This camera will be used to capture an image of the objects and texts to be analysed. To facilitate user with easy and simple to use interface, UNCOVer will feature a microphone powered by speech recognition so that the user can give command directly by speaking without pressing any button. All information will be given to the user as speech via the provided earphone.

  

UNCOVer's prototype will use a single Raspberry Pi 3 Model B to handle and process the information. To detect object and recognise characters, UNCOVer will be powered by Azure Cognitive Service for reliable object & character recognition and speech services to deliver the best possible experience.

  

To make sure blind people are within reach of the device, UNCOVer will be priced in a relatively low cost between 100 to 150 USD. The UNCOVer will be distributed to local medical vendors to reach the users.

  

With all of those feaures, it is hoped that UNCOVer will give blind people independence in identifying and locating object, and reading text so they can enjoy life as much as normal people, making them <strong>*uncover*</strong> the countless information of the world.

  

## HOW TO USE UNCOVer

  

Operating UNCOVer is very straightforward. To start using the device, the user must wear UNCOVer like a sunglasses. After the device has been firmly worn, he/she must turn on the device by pressing a button. After the device has been turned on, the user can now speak predetermined commands to UNCOVer.

  

There are several commands that the user can speak of such as "What's in front of me" to identify objects in front of the user or to describe an object pointed by the user, "Read text in front of me" to recognise text in front of the user, and "Show me available commands" to show all available commands.

  

Lastly, if the user wishes to stop using the device, he/she have to turn off the device by pressing the same button used to turn on the device.

  

<img  src="https://raw.githubusercontent.com/UNCOVer-Project/UNCOVer-Main/common/HackMyLifeGraphic/UNCOVer%20-%20HowItWorks-0001.jpg"  width="1000">

  

<sup>*Steps to use UNCOVer on object recognition*</sup>

  

<img  src="https://raw.githubusercontent.com/UNCOVer-Project/UNCOVer-Main/common/HackMyLifeGraphic/UNCOVer%20-%20HowItWorks-0002A.jpg"  width="1000">

  

<sup>*Steps to use UNCOVer on text recognition*</sup>

  

## HOW UNCOVer WORKS

  

When the device is turned on, the device will enter an initial state where the microphone will continuously record sound. The software in the raspberry pi that communicates with Azure Speech SDK will constantly perform speech recognition on the recorded stream of sound. If a sentence is completed, the software will then match the sentence in the recognised speech with the sentence of the available commands.

If the sentence "What's in front of me" is found within the recognised speech, the camera on the device will capture an image in the direction where the user is facing. The software will then send the image to Azure's Computer Vision API. The API will perform finger detection which searches the user's finger on the image, and then return the information of the finger's location and orientation in the image if a finger is detected, otherwise the API will return without the information.

UNCOVer will perform the task of detailed object recognition of the pointed object if a finger is detected. First, the software will crop the image based on the finger orientation to discard unwanted areas and minimise the search area. The finger location will be saved as a reference point for the later process. The cropped image will be sent to the Computer Vision API that will perform object recognition. The API will return complete information of the object(s) detected. If there is no object detected, then UNCOVer will say a message "No object is detected" and return to initial state. Else, the program will start calculating the distance from each detected object to the reference point. UNCOVer will pick the nearest object from the reference point and say the complete description of the chosen object, which is the pointed object.

The other task that UNCOVer will perform is general object recognition where a finger is not detected. The software will directly send the image to the Computer Vision API to recognise object(s) and will return information of object(s)'s name and position. If no objects are detected, UNCOVer will say "No object is detected". Otherwise, the device will say each object(s)'s name and relative position.

Back to the recognised speech, if the sentence "Read Text in front of me" is found, the camera will capture an image in the direction where the user is facing. The software will send the image to the Computer Vision API to perform character recognition in the image. The API will then return the information containing the text. If there are no text or any characters in the image, the returned text information will be blank and the device will say "No text or character is detected". Otherwise, the device will say all detected text in the image.

UNCOVer will use Azure Speech Service for text-to-speech conversion to give the best output speech for the user. When the object or text is detected and contained in the information returned by the API as described previously, the string in the information that will be spoken to the user will be parsed first, and then sent to the Speech Service for TTS request. The Speech Service will return the speech as a .wav audio file. UNCOVer will then say the information by playing the audio file on the earphone. For instances where no object or text is found, the pre-recorded audio file will be played instead.

  

<img src="https://raw.githubusercontent.com/UNCOVer-Project/UNCOVer-Main/common/HackMyLifeGraphic/UNCOVer%20flowchart.jpg" width=700>

<sup>*Image: General flowchart of how UNCOVer works*</sup>

  

## TOOLS THAT EMPOWER UNCOVer PROTOTYPE

  

<img  src="https://github.com/UNCOVer-Project/UNCOVer-Main/blob/common/HackMyLifeGraphic/HackmyLief-0002.jpg?raw=true"  width="1000">

  

### Azure Vision Cognitive Services

  

Extract rich information from images to categorize and process visual data—and perform machine-assisted moderation of images.

  

### Azure Speech Services

  

Swiftly convert audio to text for natural responsiveness. The Speech to Text and Text to Speech API is part of the Speech services.

  

### Python

  

Python is used for simplicity, versatility, and cross-platform compatibility. Azure Cognitive Services supports Python.

  

### Raspbian OS

  

Raspbian OS is the default OS of Raspberry Pi. Raspbian is based on linux. The OS will offer flexibility in developing the software.

  

***

  

Sources:

  

<sup>1</sup>GBD 2015 Disease and Injury Incidence and Prevalence Collaborators (2016). Global, regional, and national incidence, prevalence, and years lived with disability for 310 diseases and injuries, 1990-2015: a systematic analysis for the Global Burden of Disease Study 2015. Lancet (London, England), 388(10053), 1545-1602.

  

<sup>2</sup>Brady, E., Morris, M. R., Zhong, Y., White, S., & Bigham, J. P. (2013, April). Visual challenges in the everyday lives of blind people. In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (pp. 2117-2126). ACM.



<sup>3</sup>Kumar, L 2018, Daily Life Problems Faced by Blind People, viewed 24 January 2019, https://wecapable.com/problems-faced-by-blind-people/.

<sup>4</sup>Jarry, A., Chapdelaine, C., Kurniawan, S., & Wittich, W. (2017). Blind Adults’ Perspectives on Technical Problems and Solutions When Using Technology. Journal of Blindness Innovation & Research, 7(1).

***

For additional information about our team, please visit our project landing site: https://uncover-project.github.io/