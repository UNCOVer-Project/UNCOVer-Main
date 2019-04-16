from uncoverLib import ObjectDetection

subKey = 'f21b4f194bb1480c8dde294d9baf18e7'
objectDetect = ObjectDetection(subKey, 'image.jpg')
objectDetect.DetectObject()
objects = objectDetect.getDetectedObject()

print(objects)
