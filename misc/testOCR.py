import requests


def AzureOcr(image_path):
    subscription_key = "f21b4f194bb1480c8dde294d9baf18e7"

    assert subscription_key

    vision_base_url = ("https://southeastasia.api.cognitive.microsoft.com/"
                       + "vision/v2.0/")

    ocr_url = vision_base_url + "ocr"

    # Read the image into a byte array
    image_data = open(image_path, "rb").read()

    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'language': 'unk', 'detectOrientation': 'true'}
    response = requests.post(
        ocr_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    analysis = response.json()

    return analysis


if __name__ == '__main__':
    json_response = AzureOcr('test.jpg')

    for i in json_response['regions']:
        for j in i['lines']:
            for k in j['words']:
                print(k['text'], end=' ')
            print('')
    # print(json.dumps(json_response, indent=4, sort_keys=True))
