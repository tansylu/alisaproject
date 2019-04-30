import requests
import google_images_download   #importing the library
def im_id(s):
    response = google_images_download.googleimagesdownload()   #class instantiation
    arguments = {"keywords":s,"limit":1}
    paths = response.download(arguments)[s][0]
    url = "https://dialogs.yandex.net/api/v1/skills/42bf7345-43a8-4ea7-8a6a-8f73f885fc13/images"
    headers = {
            'Authorization': "OAuth AQAAAAAc4bhNAAT7o9I-T9hCMkPXoL0nwVPPuDc"}
    response = requests.request("POST", url, files={'file': open(paths, 'rb')}, headers=headers)
    return(response.json()['image']['id'])
