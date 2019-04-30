import requests
def bye(city):
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={}&apikey=3e267a09-6928-465d-a36c-86fa3bd4c0d8&format=json".format(city)
    response = requests.get(geocoder_request)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    coord = ','.join(toponym["Point"]["pos"].split())
    url = "https://search-maps.yandex.ru/v1/?apikey=9ec008c8-1b5b-4ca5-897a-0f18ecb866d0&text=салон красоты&type=biz&ll="+coord+"&spn=0.08,0.08&lang=ru_RU&results=3"
    response = requests.request("GET", url)
    res = []
    for i in response.json()['features']:
        word = '"'+i['properties']['CompanyMetaData']['name']+'" '+i['properties']['CompanyMetaData']['address']
        res.append(word)
    return(res)
