from uncoverLib import ObjectDetection
from uncoverLib import getImageSize
from uncoverLib import FingerDetection
import cv2
from matplotlib import pyplot as plt
import math


def getFingersMiddlePos(fingerResult):
    if len(fingerResult) < 1:
        return []

    positions = []

    # get fingers position
    for _, fingerPos in fingerResult:
        left, top, width, height = fingerPos

        shapesize = getImageSize(image_path)
        left = int(left * float(shapesize[0]))
        top = int(top * float(shapesize[1]))
        width = left + int(width * float(shapesize[0]))
        height = top + int(height * float(shapesize[1]))
        # print('l: {}, t: {}, w: {}, h: {}'.format(left, top, width, height))

        # middle point of finger
        xF = int((left + width) / 2.0)
        yF = int((top + height) / 2.0)
        # print('FINGER - xF: {}, yF: {}'.format(xF, yF))

        positions.append((xF, yF))

    return positions


def findObjectLocation(listOfObj, img_size):
    # returned value listOfTuple
    validObjs = []

    # get img dimension
    widthImg, heightImg = img_size

    for names, pos in listOfObj:
        x, _, w, _ = pos

        # middle point each obj
        xt = (w)/2.0 + x

        # divide img scene into 3 partition
        if xt <= widthImg/3.0:
            orientation = "left"
        elif xt <= 2.0 * widthImg/3.0:
            orientation = "center"
        else:
            orientation = "right"

        validObjs.append((names, orientation))

    return validObjs


def findClosestObjectFromFinger(objectResults, fingerMidPos,
                                withCoord=False):

    xF, yF = fingerMidPos
    print('FINGER - xF: {}, yF: {}'.format(xF, yF))

    distances = []
    names = []
    coords = []

    # get object mid positions
    for objName, objPos in objectResults:
        x, y, w, h = objPos

        xObj = int(w/2 + x)
        yObj = int(h/2 + y)

        dist = int(math.sqrt(
            ((xF - xObj) ** 2) + ((yF - yObj) ** 2)
        ))

        print('{} - x: {}, y: {}'.format(objName, xObj, yObj))

        distances.append(dist)
        names.append(objName)
        if withCoord is True:
            coords.append((xObj, yObj))

    closest = distances.index(min(distances))

    if withCoord is True:
        return (names[closest], coords[closest])
    else:
        return names[closest]


# set the image path
image_path = 'finger1.jpg'

# perform object detection
subKey = 'f21b4f194bb1480c8dde294d9baf18e7'
objectDetect = ObjectDetection(subKey, image_path)
objectDetect.DetectObject()
objects = objectDetect.getDetectedObject()

# perform finger detection
fingerDetect = FingerDetection(
    '4b0ab4fa945a41b187c5fcb6c4ea5cdb',
    image_path
)
fingerDetect.PredictImage()
fingerDetected = fingerDetect.getPrediction(0.5)

# find object location relative to the image
validObjs = findObjectLocation(
    objects, getImageSize(image_path)
)
print('Object locations:\n', validObjs)

fingersMidPos = getFingersMiddlePos(fingerDetected)

# find the closest object from finger
closestObj = findClosestObjectFromFinger(objects, fingersMidPos[0], True)
print('Closest object: ', closestObj)

# read the image with opencv
img = cv2.imread(image_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# draw rectangles on each object
for names, pos in objects:
    cv2.rectangle(
        img,
        (pos[0], pos[1]),
        (pos[0]+pos[2], pos[1]+pos[3]),
        (0, 255, 0),
        10
    )

# fingerDetectedJson = fingerDetect.getPredictionJson()
# print(json.dumps(fingerDetectedJson, indent=4))

# draw rectangles on finger(s)
for names, pos in fingerDetected:
    left, top, width, height = pos

    shapesize = getImageSize(image_path)
    x = int(left * float(shapesize[0]))
    y = int(top * float(shapesize[1]))
    x2 = x + int(width * float(shapesize[0]))
    y2 = y + int(height * float(shapesize[1]))

    cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 10)

# xFinger, yFinger = fingersMidPos[0]
# xClose, yClose = closestObj[1]
cv2.line(img, fingersMidPos[0], closestObj[1], (255, 255, 0), 10)

plt.imshow(img)
plt.show()
