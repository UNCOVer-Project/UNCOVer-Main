import requests
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

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
# print(image_data)
headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
              'Content-Type': 'application/octet-stream'}
params     = {'visualFeatures': 'Categories,Description,Color'}
response = requests.post(
    analyze_url, headers=headers, params=params, data=image_data)
response.raise_for_status()
print(response.request.body)
# The 'analysis' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'description' property.
analysis = response.json()
#print(analysis)

#print('TEST : ', analysis['objects']['object'])

for dicks in analysis['objects']:
    print(dicks['object'])
