# Azure custom vision prediction service
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

# Change endpoint location according to Azure account
ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com"

projectID = '2eea0487-ca2f-46e4-ab69-773f7c8b91f2'

# Replace with a valid key
training_key = "cd2b555f55f245399b4012a9aa657f90"
prediction_key = "69b8a6b4dd6a47ed8f7ca4be7d2265f2"

# Now there is a trained endpoint that can be used to make a prediction
predictor = CustomVisionPredictionClient(prediction_key, endpoint=ENDPOINT)

# Open the sample image and get back the prediction results.
with open("images/Test/test_img0.jpg", mode="rb") as test_data:
    results = predictor.predict_image(projectID, test_data)

# Display the results.
for prediction in results.predictions:
    print ("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100), prediction.bounding_box.left, prediction.bounding_box.top, prediction.bounding_box.width, prediction.bounding_box.height)
