# Azure custom vision prediction service
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

# Change endpoint location according to Azure account
ENDPOINT = "https://southeastasia.api.cognitive.microsoft.com"

projectID = '47917e0f-ee76-4fc3-afe4-1eb02b94d6b0'

# Replace with a valid key
training_key = "6ad939516c234dfc8e7de03935037264"
prediction_key = "4b0ab4fa945a41b187c5fcb6c4ea5cdb"

# Now there is a trained endpoint that can be used to make a prediction
predictor = CustomVisionPredictionClient(prediction_key, endpoint=ENDPOINT)

img_path = input('Image path: ')

# Open the sample image and get back the prediction results.
with open(img_path, mode="rb") as test_data:
    results = predictor.predict_image(projectID, test_data)

# Display the results.
for prediction in results.predictions:
    print ("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100), prediction.bounding_box.left, prediction.bounding_box.top, prediction.bounding_box.width, prediction.bounding_box.height)
