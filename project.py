# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals
import grabnails
import json
import logging
import random
import geo
from flask import Flask, request

app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

arr = {}

@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)
    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }
    handle_dialog(request.json, response)
    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )
def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Привет! Введи своё имя и город.'
        arr[user_id] = {}
        arr[user_id] = {
            'city': '', 'ggl':[]
        }
        return
    if req['session']['message_id']==1:
        global city, first_name
        city  = get_city(req)
        first_name = get_first_name(req)
        arr[user_id]['city'] = city
        arr[user_id]['ggl'] = ['nails']
        res['response']['text'] = 'Приятно познакомиться, ' +first_name.title() + '. Я - Алиса. Какой маникюр хочешь сделать?'
        res['response']['buttons'] = get_suggests()
        return
    if req['request']['original_utterance'].lower() == 'хочу маникюр!':
        word = arr[user_id]['ggl']
        res['response']['card'] = {}
        res['response']['card']['type'] = 'BigImage'
        res['response']['card']['title'] = 'Лови!'
        res['response']['card']['image_id'] = grabnails.im_id(' '.join(word))
        res['response']['text'] = 'Что-то пошло не так('
        res['response']['buttons'] = get_suggests()
        arr[user_id]['ggl'] = ['manicure pinterest']
        return
    if req['request']['original_utterance'].lower() == 'стоп' :
        res['response']['text'] = 'Вот, где можно сделать маникюр в твоем городе:'+'\n'+'\n'+('\n'.join(geo.bye(arr[user_id]['city']))) +'\n' +'\n'+'пока♡'
        arr[user_id]['city'] = city
        arr[user_id]['ggl'] = ['nails']
        res['end_session'] = True
        return
    arr[user_id]['ggl'].insert(0, req['request']['original_utterance'].lower())
    res['response']['text'] = '«' + ' '.join(arr[user_id]['ggl'][:-1]) + '» ' + 'уже в списке параметров.' + '\n' + 'Если это всё, то напиши «хочу маникюр!»'
    res['response']['buttons'] = get_suggests()

def get_suggests():
    session ={'suggests':["nature","classic", "romantic",
                "nude",
                "geometry","modern",
                "matt",
                "long",
                "rhinestones",
                "letters",
                "short",
                "pink",
                "date"]}
    random.shuffle(session['suggests'])
    arr = ['хочу маникюр!','стоп'] + session['suggests']
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in arr[:6]
    ]

    return suggests
def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            return entity['value'].get('first_name', None).title()
def get_city(req):
    # перебираем именованные сущности
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            # возвращаем None, если не нашли сущности с типом YANDEX.GEO
            return entity['value'].get('city', None)
