#!/usr/bin/python3
from flask import Flask, request, Response,make_response,send_from_directory
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage,ContactMessage,KeyboardMessage,PictureMessage,RichMediaMessage,FileMessage
from viberbot.api.messages.text_message import TextMessage
import logging
import sqlite3
import os
import datetime
import xlsxwriter
import requests
import json
import time

from viberbot.api.messages.data_types.contact import Contact

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest
import logging

app = Flask(__name__,static_folder='/')

bot_configuration = BotConfiguration(
    name='automibi3445',
    avatar='http://viber.com/avatar.jpg',
    auth_token='4c478ae7aec00b46-ae61a8e34721cea2-53f02a0305f91901'
)
viber = Api(bot_configuration)
auth_token = '4c478ae7aec00b46-ae61a8e34721cea2-53f02a0305f91901' # тут ваш токен полученный в начале #п.2
hook = 'https://chatapi.viber.com/pa/send_message'
headers = {'X-Viber-Auth-Token': auth_token}

@app.route("/hello.xlsx",methods=['GET'])
def hello(): 
    return send_from_directory(app.static_folder, 'formula.xlsx')



@app.route("/",methods=['POST','GET'])
def incoming():

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    KEYBOARD_MAIN = {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Менаджер",
    "ReplyType": "message",
    "Text": "Менаджер"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Покупатель",
    "ReplyType": "message",
    "Text": "Покупатель"
    },
    ]
    }

    KEYBOARD_DOWNLOAD = {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "КорзиПВ",
    "ReplyType": "message",
    "Text": "Предложения покупателей"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "КорзиКВ",
    "ReplyType": "message",
    "Text": "Продажи"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "ТоварВ",
    "ReplyType": "message",
    "Text": "Товары"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "МаркВ",
    "ReplyType": "message",
    "Text": "Марки"
    },
        {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "ЧастВ",
    "ReplyType": "message",
    "Text": "Модели"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "ПометкВ",
    "ReplyType": "message",
    "Text": "Расходы"
    },
        {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "КатВ",
    "ReplyType": "message",
    "Text": "Категории"
    },
    {
    "Columns":3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "глаАд",
    "ReplyType": "message",
    "Text": "Назад"
    },
    ]
    }

    KEYBOARD_NOTE = {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "ПосЗ",
    "ReplyType": "message",
    "Text": "Посмотреть все"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "УдалитьЗ",
    "ReplyType": "message",
    "Text": "Удалить"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "ДобавитьЗ",
    "ReplyType": "message",
    "Text": "Добавить"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "глаАд",
    "ReplyType": "message",
    "Text": "Назад"
    },
    ]
    }

    KEYBOARD_ADMIN_MAIN_MANAGER= {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "марки",
    "ReplyType": "message",
    "Text": "Марки"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "автомо. части",
    "ReplyType": "message",
    "Text": "Модели"
    },
        {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Категории",
    "ReplyType": "message",
    "Text": "Категории"
    }, 
        {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "корзина",
    "ReplyType": "message",
    "Text": "Корзина"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "объявления",
    "ReplyType": "message",
    "Text": "Объявления"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Пометки",
    "ReplyType": "message",
    "Text": "Расходы"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Выгрузка",
    "ReplyType": "message",
    "Text": "Выгрузка"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "На главную",
    "ReplyType": "message",
    "Text": "На главную"
    },
    {
    "Columns": 6,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Сменпра",
    "ReplyType": "message",
    "Text": "Сменить пароль"
    },   
    ]
    }

    KEYBOARD_ADMIN_MAIN= {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "марки",
    "ReplyType": "message",
    "Text": "Марки"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "автомо. части",
    "ReplyType": "message",
    "Text": "Модели"
    },
        {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Категории",
    "ReplyType": "message",
    "Text": "Категории"
    },
        {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "корзина",
    "ReplyType": "message",
    "Text": "Корзина"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "объявления",
    "ReplyType": "message",
    "Text": "Объявления"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Пометки",
    "ReplyType": "message",
    "Text": "Расходы"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Выгрузка",
    "ReplyType": "message",
    "Text": "Выгрузка"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "На главную",
    "ReplyType": "message",
    "Text": "На главную"
    },
    ]
    }


    KEYBOARD_ADMIN_MAIN_MARK= {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Добавить марки",
    "ReplyType": "message",
    "Text": "Добавить"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Удалить марки",
    "ReplyType": "message",
    "Text": "Удалить"
    },
        {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Посмотреть все марки",
    "ReplyType": "message",
    "Text": "Посмотреть все"
    },
        {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Добавить фото к объявлениям",
    "ReplyType": "message",
    "Text": "Добавить фото"
    },
            {
    "Columns": 6,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "глаАд",
    "ReplyType": "message",
    "Text": "Назад"
    },
    ]
    }


    KEYBOARD_ADMIN_MAIN_THING= {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Добавить части авто",
    "ReplyType": "message",
    "Text": "Добавить"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Удалить части авто",
    "ReplyType": "message",
    "Text": "Удалить"
    },
        {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Посмотреть все части авто",
    "ReplyType": "message",
    "Text": "Посмотреть все"
    },
        {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Добавить фото к объявлениям",
    "ReplyType": "message",
    "Text": "Добавить фото"
    },
            {
    "Columns": 6,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "глаАд",
    "ReplyType": "message",
    "Text": "Назад"
    },
    ]
    }


    KEYBOARD_ADMIN_MAIN_CAT= {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Добавить категории",
    "ReplyType": "message",
    "Text": "Добавить"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Удалить категории",
    "ReplyType": "message",
    "Text": "Удалить"
    },
        {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Посмотреть все категории",
    "ReplyType": "message",
    "Text": "Посмотреть все"
    },
        {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Добавить фото к объявлениям",
    "ReplyType": "message",
    "Text": "Добавить фото"
    },
            {
    "Columns": 6,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "глаАд",
    "ReplyType": "message",
    "Text": "Назад"
    },
    ]
    }




    KEYBOARD_ADMIN_MAIN_ADS= {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Добавить объявления",
    "ReplyType": "message",
    "Text": "Добавить"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Удалить объявления",
    "ReplyType": "message",
    "Text": "Удалить"
    },
        {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Посмотреть все объявления",
    "ReplyType": "message",
    "Text": "Посмотреть все"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Добавить фото к объявлениям",
    "ReplyType": "message",
    "Text": "Добавить фото"
    },
            {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "глаАд",
    "ReplyType": "message",
    "Text": "Назад"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Редактировать объявления",
    "ReplyType": "message",
    "Text": "Редактировать"
    },
    ]
    }

    KEYBOARD_ADMIN = {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 6,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Назад",
    "ReplyType": "message",
    "Text": "Назад"
    },
    ]
    }

    KEYBOARD_CART = {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Куили",
    "ReplyType": "message",
    "Text": "Продажи"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Свц",
    "ReplyType": "message",
    "Text": "Предложения покупателей"
    },
    {
    "Columns": 6,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "глаАд",
    "ReplyType": "message",
    "Text": "Назад"
    },
    ]
    }

    KEYBOARD_CART_ONE = {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Поскор",
    "ReplyType": "message",
    "Text": "Посмотреть все"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Удкор",
    "ReplyType": "message",
    "Text": "Удалить"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Редкор",
    "ReplyType": "message",
    "Text": "Редактировать"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "глаАд",
    "ReplyType": "message",
    "Text": "Назад"
    },
    ]
    }

    KEYBOARD_CART_TWO = {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Поссв",
    "ReplyType": "message",
    "Text": "Посмотреть все"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Удсв",
    "ReplyType": "message",
    "Text": "Удалить"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Редсв",
    "ReplyType": "message",
    "Text": "Редактировать"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "глаАд",
    "ReplyType": "message",
    "Text": "Назад"
    },
    ]
    }



    KEYBOARD_ADMIN_BACK = {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 6,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "глаАд",
    "ReplyType": "message",
    "Text": "Назад"
    },
    ]
    }

    KEYBOARD_UPDATE = {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "изма",
    "ReplyType": "message",
    "Text": "Пароль админа"
    },
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "измм",
    "ReplyType": "message",
    "Text": "Пароль менд"
    },
        {
    "Columns": 6,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "глаАд",
    "ReplyType": "message",
    "Text": "Назад"
    },
    ]
    }


    KEYBOARD_CLIENT = {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 6,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "На главную",
    "ReplyType": "message",
    "Text": "На главную"
    },
    ]
    }

    KEYBOARD_CLIENT_TWO = {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "На главную",
    "ReplyType": "message",
    "Text": "На главную"
    },
        {
    "Columns": 3,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Контакты",
    "ReplyType": "message",
    "Text": "Контакты"
    },
    ]
    }
    KEYBOARD_START = {
    "Type": "keyboard",
    "Buttons": [
    {
    "Columns": 6,
    "Rows": 1,
    "BgLoop": True,
    "ActionType": "reply",
    "ActionBody": "Начать",
    "ReplyType": "message",
    "Text": "Начать"
    },
    ]
    }

    logging.basicConfig(filename = "sample.log", level = logging.INFO)
    logging.debug("This is debug message")
    if isinstance(viber_request, ViberConversationStartedRequest):
        if request.cookies.get('statusConversationStart') != 'yes':
            mass = TextMessage(text="Вас приветствует авторазборка 🔥Auto Parts USA,🔥\nВы всегда можете подобрать запчасти на Ваш авто.\n👉Выберете модель, затем марку, и нужную Вам категорию и деталь.\n☎️И мы Вам перезвоним, или Вы можете связать с нами:\n МТС 📲0991689891\n Киевстар 📲0976072454\n Мы всегда готовы предложить хорошее решение по Вашему запросу.🙂 \n\n---------------------------\n\n Чтобы начать введите: Начать")
            key = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_START)
            viber.send_messages(viber_request.user.id, [mass])
            res = make_response("Setting a cookie")
            res.set_cookie('statusConversationStart', 'yes', max_age=60*60*24*365*2)
            return res
    elif isinstance(viber_request, ViberUnsubscribedRequest):
        res = make_response("Setting a cookie")
        res.set_cookie('statusConversationStart', 'no', max_age=60*60*24*365*2)
        return res  
    else:
        message = str(viber_request.message.text)
    if isinstance(viber_request, ViberMessageRequest):
#main section
        if message == 'Начать' or message == 'Назад' or message == 'На главную':
            messageKeyMain = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_MAIN)
            mesT = TextMessage(text="Выберите кто вы")
            viber.send_messages(viber_request.sender.id, [
            mesT,
            messageKeyMain
            ])
            res = make_response("Setting a cookie")
            res.set_cookie(str(viber_request.sender.id)[:8]+'pass', '', max_age=60*60*24*365*2)
            return res

        if message == 'Покупатель':
            with sqlite3.connect("db.db") as con:  
                cursor_select_pass = con.cursor()
                cursor_select_pass.execute("SELECT * FROM mark")   
                rows = cursor_select_pass.fetchall()
                arr_f = []
                for row in rows:
                    with sqlite3.connect("db.db") as cons:  
                        cursor_select_passs = cons.cursor()
                        cursor_select_passs.execute("SELECT * FROM models WHERE mark = ?",(str(row[0]),))   
                        rowss = len(cursor_select_passs.fetchall())
                    imger = ''
                    if row[4] != None:
                        imger = row[4].split('devider')[1]
                    else:
                        imger = 'https://avatanplus.com/files/resources/original/5bf90aff5e95b16744d2f59b.jpg' 
                    arr_f.append({
                    "Columns":6,
                    "Rows":4,
                    "ActionType":"reply",
                    "ActionBody":"Чст-"+str(row[0]),
                    "Image": imger,
                    })
                    arr_f.append({
                    "Columns":6,
                    "Rows":3,
                    "Text":"<font color=#323232><b>"+str(row[1])+"</b></font><font color=#6fc133><br>"+'Количество моделей: '+str(rowss)+"</font>",
                    "ActionType": "reply",
                    "ActionBody": "Чст-"+str(row[0]),
                    "TextSize":"large",
                    "TextVAlign":"middle",
                    "TextHAlign":"left"
                    })

            sen = {
            "receiver":viber_request.sender.id,
            "type":"rich_media",
            "min_api_version":7,
            "rich_media":{
            "Type":"rich_media",
            "ButtonsGroupColumns":6,
            "ButtonsGroupRows":7,
            "BgColor":"#FFFFFF",
            "Buttons": arr_f
            }
            }
            
            sec = {
            "receiver": viber_request.sender.id,
            "min_api_version":7,
            "keyboard":{
            "Type":"keyboard",
            "Buttons":[
            {
            "Columns": 3,
            "Rows": 1,
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "На главную",
            "ReplyType": "message",
            "Text": "На главную"
            },
            {
            "Columns": 3,
            "Rows": 1,
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "Контакты",
            "ReplyType": "message",
            "Text": "Контакты"
            },
            ]
            }
            }
            requests.post(hook, json.dumps(sen), headers=headers)
            time.sleep(0.2)
            requests.post(hook, json.dumps(sec), headers=headers)     
            return Response(status=200)


        if 'Чст' in message:
            with sqlite3.connect("db.db") as con:  
                cursor_select_pass = con.cursor()
                cursor_select_pass.execute("SELECT * FROM models WHERE mark = ? ",(message.split('-')[1]))   
                rows = cursor_select_pass.fetchall()
                arr_f = []
                for row in rows:
                    with sqlite3.connect("db.db") as cons:  
                        cursor_select_passs = cons.cursor()
                        cursor_select_passs.execute("SELECT * FROM things WHERE models = ?",(str(row[0]),))   
                        rowss = len(cursor_select_passs.fetchall())
                    imger = ''
                    if row[4] != None:
                        imger = row[4].split('devider')[1]
                    else:
                        imger = 'https://avatanplus.com/files/resources/original/5bf90aff5e95b16744d2f59b.jpg' 
                    arr_f.append({
                    "Columns":6,
                    "Rows":4,
                    "ActionType":"reply",
                    "ActionBody":"Псм-"+str(row[0]),
                    "Image": imger,
                    })
                    arr_f.append({
                    "Columns":6,
                    "Rows":3,
                    "Text":"<font color=#323232><b>"+str(row[1])+"</b></font><font color=#777777><br></font><font color=#6fc133>"+'Количество категорий запчастей: '+str(rowss)+"</font>",
                    "ActionType": "reply",
                    "ActionBody": "Псм-"+str(row[0]),
                    "TextSize":"large",
                    "TextVAlign":"middle",
                    "TextHAlign":"left"
                    })

            sen = {
            "receiver":viber_request.sender.id,
            "type":"rich_media",
            "min_api_version":7,
            "rich_media":{
            "Type":"rich_media",
            "ButtonsGroupColumns":6,
            "ButtonsGroupRows":7,
            "BgColor":"#FFFFFF",
            "Buttons": arr_f
            }
            }
            
            sec = {
            "receiver": viber_request.sender.id,
            "min_api_version":7,
            "keyboard":{
            "Type":"keyboard",
            "Buttons":[
            {
            "Columns": 3,
            "Rows": 1,
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "На главную",
            "ReplyType": "message",
            "Text": "На главную"
            },            {
            "Columns": 3,
            "Rows": 1,
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "Контакты",
            "ReplyType": "message",
            "Text": "Контакты"
            },
            ]
            }
            }
                 
            requests.post(hook, json.dumps(sen), headers=headers)
            time.sleep(0.2)
            requests.post(hook, json.dumps(sec), headers=headers)     
            return Response(status=200)





        if 'Псм' in message:
            with sqlite3.connect("db.db") as con:  
                cursor_select_pass = con.cursor()
                cursor_select_pass.execute("SELECT * FROM things WHERE models = ? ",(message.split('-')[1]))   
                rows = cursor_select_pass.fetchall()
                arr_f = []
                for row in rows:
                    with sqlite3.connect("db.db") as cons:  
                        cursor_select_passs = cons.cursor()
                        cursor_select_passs.execute("SELECT * FROM offer WHERE thing = ?",(str(row[0]),))   
                        rowss = len(cursor_select_passs.fetchall())
                    imger = ''
                    if row[5] != None:
                        imger = row[5].split('devider')[1]
                    else:
                        imger = 'https://avatanplus.com/files/resources/original/5bf90aff5e95b16744d2f59b.jpg' 
                    arr_f.append({
                    "Columns":6,
                    "Rows":4,
                    "ActionType":"reply",
                    "ActionBody":"Сбо-"+str(row[0]),
                    "Image": imger,
                    })
                    arr_f.append({
                    "Columns":6,
                    "Rows":3,
                    "Text":"<font color=#323232><b>"+str(row[1])+"</b></font><font color=#777777><br></font><font color=#6fc133>"+'Количество объявлений: '+str(rowss)+"</font>",
                    "ActionType": "reply",
                    "ActionBody": "Сбо-"+str(row[0]),
                    "TextSize":"large",
                    "TextVAlign":"middle",
                    "TextHAlign":"left"
                    })

            sen = {
            "receiver":viber_request.sender.id,
            "type":"rich_media",
            "min_api_version":7,
            "rich_media":{
            "Type":"rich_media",
            "ButtonsGroupColumns":6,
            "ButtonsGroupRows":7,
            "BgColor":"#FFFFFF",
            "Buttons": arr_f
            }
            }
            
            sec = {
            "receiver": viber_request.sender.id,
            "min_api_version":7,
            "keyboard":{
            "Type":"keyboard",
            "Buttons":[
            {
            "Columns": 3,
            "Rows": 1,
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "На главную",
            "ReplyType": "message",
            "Text": "На главную"
            },
                        {
            "Columns": 3,
            "Rows": 1,
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "Контакты",
            "ReplyType": "message",
            "Text": "Контакты"
            }
            ]
            }
            }
                 
            requests.post(hook, json.dumps(sen), headers=headers)
            time.sleep(0.2)
            requests.post(hook, json.dumps(sec), headers=headers)     
            return Response(status=200)




        if 'Сбо' in message:
            messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_CLIENT_TWO)
            with sqlite3.connect("db.db") as con:  
                cursor_select_pass = con.cursor()
                cursor_select_pass.execute("SELECT * FROM offer WHERE thing = ?",(message.split('-')[1]))   
                rows = cursor_select_pass.fetchall()
                finSel = ''
                for row in rows:
                    if row[7] != 0:
                        finSel = ' № '+str(row[0])+' Название: '+str(row[1])+' Цена: '+str(row[2])+'\n\n Описание: '+str(row[3])+'\n\n Время добавления: '+str(row[5])+'\n\n---------------------------\n\n'+str(finSel)
                finSel = 'Чтобы посмотреть объявление введите номер объявления\n\n---------------------------\n\n'+finSel + 'Чтобы посмотреть объявление введите номер объявления'
            textMarkAdd = TextMessage(text=str(finSel))   
            viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])  
            return Response(status=200)


        if message == 'Менаджер':
            messageKeyMain = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN)
            password = TextMessage(text='Введите пароль')   
            viber.send_messages(viber_request.sender.id, [
            password,
            messageKeyMain
            ])
            return Response(status=200)

        with sqlite3.connect("db.db") as con:  
            cursor_select_pass = con.cursor()
            cursor_select_pass.execute("SELECT * FROM users")   
            rows = cursor_select_pass.fetchall()
            final_pass = str(rows[1][1])
            final_pass_manager = str(rows[0][1])
        if final_pass in message:
            messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_MAIN)
            buy = TextMessage(text='Админ Панель')   
            viber.send_messages(viber_request.sender.id, [
            buy,
            messageKeyClient
            ])
            res = make_response("Setting a cookie")
            res.set_cookie(str(viber_request.sender.id)[:8]+'pass', message, max_age=60*60*24*365*2)
            return res

        if ((request.cookies.get(str(viber_request.sender.id)[:8]+'pass') == final_pass) and (message == 'глаАд') ):
            messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_MAIN)
            buy = TextMessage(text='Админ Панель')   
            viber.send_messages(viber_request.sender.id, [
            buy,
            messageKeyClient
            ])
            return Response(status=200)

        if final_pass_manager in message:
            messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_MAIN_MANAGER)
            buy = TextMessage(text='Админ Панель')   
            viber.send_messages(viber_request.sender.id, [
            buy,
            messageKeyClient
            ])
            res = make_response("Setting a cookie")
            res.set_cookie(str(viber_request.sender.id)[:8]+'pass', message, max_age=60*60*24*365*2)
            return res

        if ((request.cookies.get(str(viber_request.sender.id)[:8]+'pass') == final_pass_manager) and (message == 'глаАд') ):
            messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_MAIN_MANAGER)
            buy = TextMessage(text='Админ Панель')   
            viber.send_messages(viber_request.sender.id, [
            buy,
            messageKeyClient
            ])
            return Response(status=200)

#Admin    

        if len(str(request.cookies.get(str(viber_request.sender.id)[:8]+'pass'))) > 0:
        
            


            if message == 'КорзиКВ':
                workbook = xlsxwriter.Workbook('formula.xlsx')
                worksheet = workbook.add_worksheet()

                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM cart WHERE y_cost = 0")   
                    rows = cursor_select_pass.fetchall()
                bold = workbook.add_format({'bold': True})
                worksheet.set_column(0, 7, 15)
                worksheet.write('A1', 'Имя', bold)
                worksheet.write('B1', 'Город', bold)
                worksheet.write('C1', 'Телфон', bold)
                worksheet.write('D1', 'Статус', bold)
                worksheet.write('E1', 'Дата', bold)
                worksheet.write('F1', 'Номер товара', bold)
                worksheet.write('G1', 'Цена', bold)

                for i, offer in enumerate(rows, start=2):
                    worksheet.write(f'A{i}', offer[2])
                    worksheet.write(f'B{i}', offer[3])
                    worksheet.write(f'C{i}', offer[5])
                    worksheet.write(f'D{i}', offer[7])
                    worksheet.write(f'E{i}', offer[9])
                    worksheet.write(f'F{i}', offer[1])
                    worksheet.write(f'G{i}', offer[4])
                        # колонкой ниже добавить подсчет суммы
                    worksheet.write(f'F{i+1}', 'Итого:',bold)
                    worksheet.write(f'G{i+1}', f'=SUM(G2:G{i})')
                        #   сохраняем и закрываем
                workbook.close()
                filename = 'file'+str(datetime.datetime.today().strftime("%m/%d/%Y"))+'.xlsx'
                textMarkAdd = FileMessage(media='https://celecard.ru/hello.xlsx', size=10000, file_name=filename)
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)


            if message == 'КорзиПВ':
                workbook = xlsxwriter.Workbook('formula.xlsx')
                worksheet = workbook.add_worksheet()

                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM cart WHERE y_cost <> 0")   
                    rows = cursor_select_pass.fetchall()
                bold = workbook.add_format({'bold': True})
                worksheet.set_column(0, 7, 15)
                worksheet.write('A1', 'Имя', bold)
                worksheet.write('B1', 'Город', bold)
                worksheet.write('C1', 'Телфон', bold)
                worksheet.write('D1', 'Статус', bold)
                worksheet.write('E1', 'Предоплата', bold)
                worksheet.write('F1', 'Дата', bold)
                worksheet.write('G1', 'Номер товара', bold)
                worksheet.write('H1', 'Предложенная цена', bold)

                for i, offer in enumerate(rows, start=2):
                    worksheet.write(f'A{i}', offer[2])
                    worksheet.write(f'B{i}', offer[3])
                    worksheet.write(f'C{i}', offer[5])
                    worksheet.write(f'D{i}', offer[7])
                    worksheet.write(f'E{i}', offer[8])
                    worksheet.write(f'F{i}', offer[9])
                    worksheet.write(f'G{i}', offer[1])
                    worksheet.write(f'H{i}', offer[6])
                        # колонкой ниже добавить подсчет суммы
                    worksheet.write(f'G{i+1}', 'Итого:',bold)
                    worksheet.write(f'H{i+1}', f'=SUM(H2:H{i})')
                        #   сохраняем и закрываем
                workbook.close()
                filename = 'file'+str(datetime.datetime.today().strftime("%m/%d/%Y"))+'.xlsx'
                textMarkAdd = FileMessage(media='https://celecard.ru/hello.xlsx', size=10000, file_name=filename)
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)

            if message == 'ТоварВ':
                workbook = xlsxwriter.Workbook('formula.xlsx')
                worksheet = workbook.add_worksheet()

                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM offer")   
                    rows = cursor_select_pass.fetchall()
                bold = workbook.add_format({'bold': True})
                worksheet.set_column(0, 7, 15)
                worksheet.write('A1', 'Имя', bold)
                worksheet.write('B1', 'Описание', bold)
                worksheet.write('C1', 'Дата', bold)
                worksheet.write('D1', 'Статус', bold)
                worksheet.write('E1', 'Картинка', bold)
                worksheet.write('F1', 'Номер части', bold)
                worksheet.write('G1', 'Сумма', bold)

                for i, offer in enumerate(rows, start=2):
                    worksheet.write(f'A{i}', offer[2])
                    worksheet.write(f'B{i}', offer[3])
                    worksheet.write(f'C{i}', offer[5])
                    worksheet.write(f'D{i}', offer[7])
                    worksheet.write(f'E{i}', offer[6])
                    worksheet.write(f'F{i}', offer[4])
                    worksheet.write(f'G{i}', offer[2])

                        # колонкой ниже добавить подсчет суммы
                    worksheet.write(f'F{i+1}', 'Итого:',bold)
                    worksheet.write(f'G{i+1}', f'=SUM(G2:G{i})')
                        #   сохраняем и закрываем
                workbook.close()
                filename = 'file'+str(datetime.datetime.today().strftime("%m/%d/%Y"))+'.xlsx'
                textMarkAdd = FileMessage(media='https://celecard.ru/hello.xlsx', size=10000, file_name=filename)
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)


            if message == 'ПометкВ':
                workbook = xlsxwriter.Workbook('formula.xlsx')
                worksheet = workbook.add_worksheet()

                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM note")   
                    rows = cursor_select_pass.fetchall()
                bold = workbook.add_format({'bold': True})
                worksheet.set_column(0, 7, 15)
                worksheet.write('A1', 'Название', bold)
                worksheet.write('B1', 'Дата', bold)
                worksheet.write('C1', 'Цена', bold)

                for i, offer in enumerate(rows, start=2):
                    worksheet.write(f'A{i}', offer[1])
                    worksheet.write(f'B{i}', offer[3])
                    worksheet.write(f'C{i}', offer[2])


                        # колонкой ниже добавить подсчет суммы
                    worksheet.write(f'B{i+1}', 'Итого:',bold)
                    worksheet.write(f'C{i+1}', f'=SUM(C2:C{i})')
                        #   сохраняем и закрываем
                workbook.close()
                filename = 'file'+str(datetime.datetime.today().strftime("%m/%d/%Y"))+'.xlsx'
                textMarkAdd = FileMessage(media='https://celecard.ru/hello.xlsx', size=10000, file_name=filename)
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)

            if message == 'МаркВ':
                workbook = xlsxwriter.Workbook('formula.xlsx')
                worksheet = workbook.add_worksheet()

                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM mark")   
                    rows = cursor_select_pass.fetchall()
                bold = workbook.add_format({'bold': True})
                worksheet.set_column(0, 7, 15)
                worksheet.write('A1', 'Наименование', bold)
                worksheet.write('B1', 'Дата', bold)
                worksheet.write('C1', 'Картинка', bold)

                for i, offer in enumerate(rows, start=2):
                    worksheet.write(f'A{i}', offer[1])
                    worksheet.write(f'B{i}', offer[2])
                    worksheet.write(f'C{i}', offer[4])

                        # колонкой ниже добавить подсчет суммы
                        #   сохраняем и закрываем
                workbook.close()
                filename = 'file'+str(datetime.datetime.today().strftime("%m/%d/%Y"))+'.xlsx'
                textMarkAdd = FileMessage(media='https://celecard.ru/hello.xlsx', size=10000, file_name=filename)
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)

            if message == 'ЧастВ':
                workbook = xlsxwriter.Workbook('formula.xlsx')
                worksheet = workbook.add_worksheet()

                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM models")   
                    rows = cursor_select_pass.fetchall()
                bold = workbook.add_format({'bold': True})
                worksheet.set_column(0, 7, 15)
                worksheet.write('A1', 'Наименование', bold)
                worksheet.write('B1', 'Дата', bold)
                worksheet.write('C1', 'Номер марки', bold)
                worksheet.write('D1', 'Картинка', bold)

                for i, offer in enumerate(rows, start=2):
                    worksheet.write(f'A{i}', offer[1])
                    worksheet.write(f'B{i}', offer[3])
                    worksheet.write(f'C{i}', offer[2])
                    worksheet.write(f'D{i}', offer[4])
                        # колонкой ниже добавить подсчет суммы
                        #   сохраняем и закрываем
                workbook.close()
                filename = 'file'+str(datetime.datetime.today().strftime("%m/%d/%Y"))+'.xlsx'
                textMarkAdd = FileMessage(media='https://celecard.ru/hello.xlsx', size=10000, file_name=filename)
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)


            if message == 'КатВ':
                workbook = xlsxwriter.Workbook('formula.xlsx')
                worksheet = workbook.add_worksheet()

                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM things")   
                    rows = cursor_select_pass.fetchall()
                bold = workbook.add_format({'bold': True})
                worksheet.set_column(0, 7, 15)
                worksheet.write('A1', 'Наименование', bold)
                worksheet.write('B1', 'Дата', bold)
                worksheet.write('C1', 'Номер модели', bold)
                worksheet.write('D1', 'Картинка', bold)

                for i, offer in enumerate(rows, start=2):
                    worksheet.write(f'A{i}', offer[1])
                    worksheet.write(f'B{i}', offer[3])
                    worksheet.write(f'C{i}', offer[2])
                    worksheet.write(f'D{i}', offer[5])
                        # колонкой ниже добавить подсчет суммы
                        #   сохраняем и закрываем
                workbook.close()
                filename = 'file'+str(datetime.datetime.today().strftime("%m/%d/%Y"))+'.xlsx'
                textMarkAdd = FileMessage(media='https://celecard.ru/hello.xlsx', size=10000, file_name=filename)
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)


            if message == 'марки':
                messageKeyMainMark = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_MAIN_MARK)
                textMarkAdd = TextMessage(text="Выберите что вы хотите сделать с ними")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyMainMark])
                return Response(status=200)
            if message == 'Добавить марки':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: ДобавитьМ-МАРКА АВТО")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if message == 'Удалить марки':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: УдалитьМ-НОМЕР МАРКИ")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)               
            if message == 'Посмотреть все марки':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: Пм")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)


            if 'ДобавитьМ' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("INSERT INTO mark (mark,dateof) VALUES(?,?)",(message.split('-')[1],datetime.datetime.today().strftime("%m/%d/%Y")))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Марка добавлена успешно")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if 'УдалитьМ' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("DELETE FROM mark WHERE  id=?",(message.split('-')[1], ))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Марка успешно удалена")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if 'Пм' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM mark")   
                    rows = cursor_select_pass.fetchall()
                    finSel = ''
                    for row in rows:
                        with sqlite3.connect("db.db") as cons:  
                            cursor_select_passs = cons.cursor()
                            cursor_select_passs.execute("SELECT * FROM models WHERE mark = ?",(str(row[0]),))   
                            rowss = len(cursor_select_passs.fetchall())
                        finSel = ' № '+str(row[0])+' Марка: '+str(row[1])+' Время: '+str(row[2])+'\nКоличество: '+str(rowss)+'\n\n--------------------------\n\n'+str(finSel)
                    finSel = finSel + 'Чтобы перейти от марки к моделе введите: \n Чст-НОМЕР'

                    textMarkAdd = TextMessage(text=str(finSel))   
                    viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                    return Response(status=200)                    

            

            if message == 'Пометки':
                messageKeyMainMark = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_NOTE)
                textMarkAdd = TextMessage(text="Выберите что вы хотите сделать с ними")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyMainMark])
                return Response(status=200)
            if message == 'ДобавитьЗ':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: ДЗ-ПОМЕТКА/ЦЕНА")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if message == 'УдалитьЗ':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: УЗ-НОМЕР")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)               
            if message == 'ПосЗ':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: Пп")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)


            if 'ДЗ' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("INSERT INTO note (name,cost,dateof) VALUES(?,?,?)",(message.split('-')[1].split('/')[0],message.split('-')[1].split('/')[1],datetime.datetime.today().strftime("%m/%d/%Y")))
                    con.commit()        
                textMarkAdd = TextMessage(text="Пометка добавлена успешно")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if 'УЗ' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("DELETE FROM note WHERE id=?",(message.split('-')[1], ))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Пометка успешно удалена")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if 'Пп' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM note")   
                    rows = cursor_select_pass.fetchall()
                    finSel = ''
                    for row in rows:
                        finSel = ' № '+str(row[0])+' Название: '+str(row[1])+' Цена: '+str(row[2])+' Время: '+str(row[3])+'\n\n------------------\n\n'+str(finSel)
                    textMarkAdd = TextMessage(text=str(finSel))   
                    viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                    return Response(status=200)                    

            array_img = request.cookies.get('array_img')
            if 'http' in message:

                array_img = str(array_img) +'devider'+ str(message)
                res = make_response("Фото")
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                res.set_cookie('array_img', array_img, max_age=17)
                mesT = TextMessage(text="Фото добавлено в список на загрузку \n\n Чтобы окончатлеьно загрузить \n\n к объявлениям введите: Загрузить \n\n к маркам введите: Загмарки \n\n к моделям введите: Загмодели \n\n к категориям введите: Загкатегории")
                viber.send_messages(viber_request.sender.id, [
                mesT,messageKeyClient
                ])
                return res 


            if message == 'автомо. части':
                messageKeyMainMark = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_MAIN_THING)
                textMarkAdd = TextMessage(text="Выберите что вы хотите сделать с ними")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyMainMark])
                return Response(status=200)
            if message == 'Добавить части авто':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: ДобавитьВ-МОДЕЛЬ/НОМЕР МАРКИ")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if message == 'Удалить части авто':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: УдалитьВ-НОМЕР МОДЕЛИ")  
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)               
            if message == 'Посмотреть все части авто':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: Пд")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)

            if 'ДобавитьВ' in message:
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("INSERT INTO models (name,mark,dateof) VALUES(?,?,?)",(message.split('-')[1].split('/')[0],message.split('-')[1].split('/')[1],datetime.datetime.today().strftime("%m/%d/%Y")))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Моедль добавлена успешно")  
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK) 
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if 'УдалитьВ' in message:
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("DELETE FROM models WHERE id=?",(message.split('-')[1], ))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Модель успешно удалена")  
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK) 
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if 'Пд' in message:
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM models")   
                    rows = cursor_select_pass.fetchall()
                    finSel = ''
                    for row in rows:
                        with sqlite3.connect("db.db") as cons:  
                            cursor_select_passs = cons.cursor()
                            cursor_select_passs.execute("SELECT * FROM things WHERE models = ?",(str(row[0]),))   
                            rowss = len(cursor_select_passs.fetchall())
                        finSel = ' № '+str(row[0])+' Модели: '+str(row[1])+' Марка: '+str(row[3])+'\nВремя: '+str(row[2])+'\nКоличество: '+str(rowss)+'\n\n---------------------\n\n'+str(finSel)
                    finSel = finSel + 'Чтобы перейти от модели к категории введите: \n Псм-НОМЕР'
                    textMarkAdd = TextMessage(text=str(finSel))  
                    messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK) 
                    viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                    return Response(status=200)    



            if 'ЧсА' in message:
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM models WHERE mark = ? ",(message.split('-')[1]))   
                    rows = cursor_select_pass.fetchall()
                    finSel = ''
                    for row in rows:
                        with sqlite3.connect("db.db") as cons:  
                            cursor_select_passs = cons.cursor()
                            cursor_select_passs.execute("SELECT * FROM offer WHERE thing = ?",(str(row[0]),))   
                            rowss = len(cursor_select_passs.fetchall())
                        finSel = ' № '+str(row[0])+' Часть: '+str(row[1])+' Марка: '+str(row[2])+'\nВремя: '+str(row[3])+'\nКоличество: '+str(rowss)+'\n\n---------------------\n\n'+str(finSel)
                    textMarkAdd = TextMessage(text=str(finSel))   
                    messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK) 
                    viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                    return Response(status=200)
                
 
            

            if message == 'Категории':
                messageKeyMainMark = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_MAIN_CAT)
                textMarkAdd = TextMessage(text="Выберите что вы хотите сделать с ними")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyMainMark])
                return Response(status=200)
            if message == 'Добавить категории':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: ДобавитьК-КАТЕГОРИЯ/НОМЕР МОДЕЛИ")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if message == 'Удалить категории':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: УдалитьК-НОМЕР КАТЕГОРИИ")  
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)               
            if message == 'Посмотреть все категории':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: Пк")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)

            if 'ДобавитьК' in message:
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("INSERT INTO things (name,models,dateof) VALUES(?,?,?)",(message.split('-')[1].split('/')[0],message.split('-')[1].split('/')[1],datetime.datetime.today().strftime("%m/%d/%Y")))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Категория добавлена успешно")  
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK) 
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if 'УдалитьК' in message:
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("DELETE FROM things WHERE id=?",(message.split('-')[1], ))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Категория успешно удалена")  
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if 'Пк' in message:
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM things")   
                    rows = cursor_select_pass.fetchall()
                    finSel = ''
                    for row in rows:
                        with sqlite3.connect("db.db") as cons:  
                            cursor_select_passs = cons.cursor()
                            cursor_select_passs.execute("SELECT * FROM offer WHERE thing = ?",(str(row[0]),))   
                            rowss = len(cursor_select_passs.fetchall())
                        finSel = ' № '+str(row[0])+' Категория: '+str(row[1])+' Модель: '+str(row[2])+'\nВремя: '+str(row[3])+'\nКоличество: '+str(rowss)+'\n\n---------------------\n\n'+str(finSel)
                    finSel = finSel + 'Чтобы перейти от категории к объявлениям введите: \n Сбо-НОМЕР'
                    textMarkAdd = TextMessage(text=str(finSel))  
                    messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK) 
                    viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                    return Response(status=200)           


            

            if message == 'объявления':
                messageKeyMainMark = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_MAIN_ADS)
                textMarkAdd = TextMessage(text="Выберите что вы хотите сделать с ними")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyMainMark])
                return Response(status=200)
            if message == 'Добавить объявления':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: ДобавитьA-НАЗВАНИЕ/КРАТКОЕ ОПИСАНИЕ/ЦЕНА/НОМЕР КАТЕГОРИИ")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if message == 'Удалить объявления':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: УдалитьA-НОМЕР")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)              
            if message == 'Посмотреть все объявления':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: \n Пб <- Посмотреть все объявления \n НОМЕР <- Посмотреть объявление по номеру")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if message == 'Добавить фото к объявлениям':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: Номер-НОМЕР")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)

            if 'ДобавитьA' in message:
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("INSERT INTO offer (name,cost,dateof,thing,describe) VALUES(?,?,?,?,?)",(message.split('-')[1].split('/')[0],message.split('-')[1].split('/')[2],datetime.datetime.today().strftime("%m/%d/%Y"),message.split('-')[1].split('/')[3],message.split('-')[1].split('/')[1]))   
                    con.commit()   
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)     
                textMarkAdd = TextMessage(text="Объявление добавлена успешно")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if 'Номер' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)   
                res = make_response("Setting a cookie")
                res.set_cookie('id', message.split('-')[1], max_age=60*60*24*365*2)
                textMarkAdd = TextMessage(text="Загрузите фото")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient]) 
                return res  
            if 'УдалитьА' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("DELETE FROM offer WHERE id=?",(message.split('-')[1], ))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Объявление успешно удалено")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if 'Загрузить' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("UPDATE offer SET img = ? WHERE id = ?",(request.cookies.get('array_img'),request.cookies.get('id')))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Фото успешно загружено")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            
            if 'Загмарки' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("UPDATE mark SET img = ? WHERE id = ?",(request.cookies.get('array_img'),request.cookies.get('id')))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Фото успешно загружено")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)

            if 'Загмодели' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("UPDATE models SET img = ? WHERE id = ?",(request.cookies.get('array_img'),request.cookies.get('id')))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Фото успешно загружено")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)


            if 'Загкатегории' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("UPDATE things SET img = ? WHERE id = ?",(request.cookies.get('array_img'),request.cookies.get('id')))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Фото успешно загружено")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)

            if 'Пб' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM offer")   
                    rows = cursor_select_pass.fetchall()
                    finSel = ''
                    for row in rows:
                        if row[7] != 0:
                            finSel = ' № '+str(row[0])+' Название: '+str(row[1])+' Цена: '+str(row[2])+'\n\n Описание: '+str(row[3])+'\n\n Время: '+str(row[5])+'\n\n--------------------------------\n\n'+str(finSel)
                    finSel = 'Чтобы посмотреть объявление введите номер объявления\n\n---------------------------\n\n'+finSel + 'Чтобы посмотреть объявление введите номер объявления'
                textMarkAdd = TextMessage(text=str(finSel))   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])  
                return Response(status=200)

            if 'ПсА' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM offer WHERE thing = ?",(message.split('-')[1]))   
                    rows = cursor_select_pass.fetchall()
                    finSel = ''
                    for row in rows:
                        if row[7] != 0:
                            finSel = ' № '+str(row[0])+' Название: '+str(row[1])+' Цена: '+str(row[2])+'\n\n Описание: '+str(row[3])+'\n\n Время: '+str(row[5])+'\n\n---------------------------\n\n'+str(finSel)
                textMarkAdd = TextMessage(text=str(finSel))   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])  
                return Response(status=200)


            if 'оА' in message:
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM offer WHERE id = ?",(message.split('-')[1]))   
                    rows = cursor_select_pass.fetchall()[0]
                array_send = [TextMessage(text="Название: "+str(rows[1])+'\n\n'+'Описание: '+str(rows[3])+'\n\n\n'+'Время: '+str(rows[5])+'\n'+'Цена: '+str(rows[2]))]
                if rows[6] != None:
                    for row in rows[6].split('devider'):
                        if row != 'None':
                            array_send.append(PictureMessage(media=str(row)))  

                KEYBOARD_BUY = {
                "Type": "keyboard",
                "Buttons": [
                {
                "Columns": 3,
                "Rows": 1,
                "BgLoop": True,
                "ActionType": "reply",
                "ActionBody": "КУК-"+str(rows[0])+'/'+str(rows[2]),
                "ReplyType": "message",
                "Text": "Купить"
                },
                {
                "Columns": 3,
                "Rows": 1,
                "BgLoop": True,
                "ActionType": "reply",
                "ActionBody": "КУ2-"+str(rows[0]),
                "ReplyType": "message",
                "Text": "Своя цена"
                },
                            {
            "Columns": 3,
            "Rows": 1,
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "Контакты",
            "ReplyType": "message",
            "Text": "Контакты"
            },
                {
                "Columns": 3,
                "Rows": 1,
                "BgLoop": True,
                "ActionType": "reply",
                "ActionBody": "глаАд",
                "ReplyType": "message",
                "Text": "Назад"
                },
                ]
                }
                buyKeys = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_BUY)
                array_send.append(buyKeys)


                viber.send_messages(viber_request.sender.id, array_send)
                return Response(status=200)  
                                                      


            if 'Редактировать объявления' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите по образцу чтобы сделать изменения \n\nРедназ-ном/наз <- измен. название \nРедопис-ном/опис <- измен. описания \nРедцен-ном/цена <- измен. цены \nРедст-ном/статус <- измен. статуса \n Введите 0 чтобы товар не показывался") 
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if 'Редназ' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("UPDATE offer SET name = ? WHERE id = ?",(message.split('-')[1].split('/')[1],message.split('-')[1].split('/')[0],))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Изменения успешно внесены")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if 'Редопис' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("UPDATE offer SET describe = ? WHERE id = ?",(message.split('-')[1].split('/')[1],message.split('-')[1].split('/')[0]))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Изменения успешно внесены")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if 'Редст' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("UPDATE offer SET status = ? WHERE id = ?",(message.split('-')[1].split('/')[1],message.split('-')[1].split('/')[0]))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Изменения успешно внесены")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)



        
            if 'корзина' in message:
                messageKeyMainMark = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_CART)
                textMarkAdd = TextMessage(text="Что вы хотите посмотреть")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyMainMark])
                return Response(status=200)            
            if 'Куили' in message:
                messageKeyMainMark = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_CART_ONE)
                textMarkAdd = TextMessage(text="Те кто купили")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyMainMark])
                return Response(status=200)
            if 'Свц' in message:
                messageKeyMainMark = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_CART_TWO)
                textMarkAdd = TextMessage(text="Те кто предложили свою цену")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyMainMark])
                return Response(status=200)


            if message == 'Удкор' or message == 'Удсв':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: УдаК-НОМЕР")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if message == 'Редкор' or message == 'Редсв':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите по образцу :\n РедКС-номер заказа/пример'ожидает отправки' <- изменение статуcа заказа\n РедКП-номер заказа/пример'предоплата 500 грн'<- изменение предоплаты")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)

            

            if 'УдаК' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("DELETE FROM cart WHERE id=?",(message.split('-')[1], ))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Позиция в корзине успешно удалена")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)

            if 'РедКС' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("UPDATE cart SET status = ? WHERE id = ?",(message.split('-')[1].split('/')[1],message.split('-')[1].split('/')[0]))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Изменения успешно внесены")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)

            if 'РедКП' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("UPDATE cart SET opl = ? WHERE id = ?",(message.split('-')[1].split('/')[1],message.split('-')[1].split('/')[0]))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Изменения успешно внесены")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)           
            


            if message == 'Поскор':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: пкп")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)

            if message == 'Поссв':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: псц")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)

    
            if message == 'Выгрузка':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_DOWNLOAD)
                textMarkAdd = TextMessage(text="Выберите то что хотите выгрузить")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)


            if message == 'пкп':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM cart WHERE y_cost = 0")   
                    rows = cursor_select_pass.fetchall()
                    finSel = ''
                    for row in rows:
                        finSel = ' № '+str(row[0])+' Имя: '+str(row[2])+' Город: '+str(row[3])+' Телефон: '+str(row[5])+'\nДата добавления: '+str(row[9])+' Статус: '+str(row[7])+' Цена: '+str(row[4])+'\n\n Номер товара: '+str(row[1])+'\nПредоплата: '+str(row[8])+'\n\n----------------------------\n\n'+str(finSel)
                textMarkAdd = TextMessage(text=str(finSel))   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])  
                return Response(status=200)

            if message == 'псц':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("SELECT * FROM cart WHERE cost = 0")   
                    rows = cursor_select_pass.fetchall()
                    finSel = ''
                    for row in rows:
                        finSel = ' № '+str(row[0])+' Имя: '+str(row[2])+' Город: '+str(row[3])+' Телефон: '+str(row[5])+'\nДата добавления: '+str(row[9])+' Статус: '+str(row[7])+' Предложена цена: '+str(row[4])+'\n\n Номер товара: '+str(row[1])+'\nПредоплата: '+str(row[8])+'\n\n------------------------------\n\n'+str(finSel)
                textMarkAdd = TextMessage(text=str(finSel))   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])  
                return Response(status=200)


            if message == 'Сменпра':
                messageKeyMainMark = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_UPDATE)
                textMarkAdd = TextMessage(text="Здесь можно поменять пароли для разных типов пользователей")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyMainMark])
                return Response(status=200)

            if message == 'измм':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: Имен-ПАРОЛЬ")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)
            if message == 'изма':
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_ADMIN_BACK)
                textMarkAdd = TextMessage(text="Введите: Иадм-ПАРОЛЬ")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)

            if 'Иадм' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_CLIENT)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("UPDATE users SET password = ? WHERE name = ?",(message.split('-')[1],'admin'))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Изменения успешно внесены")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)  

            if 'Имен' in message:
                messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_CLIENT)
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("UPDATE users SET password = ? WHERE name = ?",(message.split('-')[1],'manager'))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Изменения успешно внесены")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)  

        if 'КУК' in message:
            messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_CLIENT_TWO)
            res = make_response("Setting a cookie")
            res.set_cookie(str(viber_request.sender.id)[:8]+'buy', message.split('-')[1], max_age=60*60*24*365*2) 
            textMarkAdd = TextMessage(text="Чтобы купить товар введите данные, и мы свяжемся с вами: \n\n Купить: ФИО/Город/Телефон \n\n Пример ввода: \n\n Купить: Иванов Иван/Липецк/7999999999") 
            viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
            return res
        if 'КУ2' in message:
            messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_CLIENT_TWO)
            res = make_response("Setting a cookie")
            res.set_cookie(str(viber_request.sender.id)[:8]+'buy2', message.split('-')[1], max_age=60*60*24*365*2) 
            textMarkAdd = TextMessage(text="Предложите свою цены, и мы с вами свяжемся.\nВведите ваши данные:\n\n Купить: ФИО/Город/Телефон/И Ваша цена за которую вы готовы купить \n\n Пример ввода: \n\n Купить: Иванов Иван/Липецк/7999999999/3000") 
            viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
            return res
                

        if 'Купить' in message:
            id_offer = request.cookies.get(str(viber_request.sender.id)[:8]+'buy').split('/')[0]
            id_offer2 = request.cookies.get(str(viber_request.sender.id)[:8]+'buy2')
            messageKeyClient = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_CLIENT)
            if len(id_offer) > 0:
                cost = request.cookies.get(str(viber_request.sender.id)[:8]+'buy').split('/')[1]
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("INSERT INTO cart (id_offer,name,city,phone,cost,dateof) VALUES(?,?,?,?,?,?)",(id_offer,message.split(':')[1].split('/')[0],message.split(':')[1].split('/')[1],message.split(':')[1].split('/')[2],cost,datetime.datetime.today().strftime("%m/%d/%Y")))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Ваш заказ успешно добавлен")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                res = make_response("Setting a cookie")
                res.set_cookie(str(viber_request.sender.id)[:8]+'buy', '', max_age=60*60*24*365*2) 
                return res
            elif len(id_offer2) > 0:
                with sqlite3.connect("db.db") as con:  
                    cursor_select_pass = con.cursor()
                    cursor_select_pass.execute("INSERT INTO cart (id_offer,name,city,phone,y_cost,dateof) VALUES(?,?,?,?,?,?)",(id_offer2,message.split(':')[1].split('/')[0],message.split(':')[1].split('/')[1],message.split(':')[1].split('/')[2],message.split(':')[1].split('/')[3],datetime.datetime.today().strftime("%m/%d/%Y")))   
                    con.commit()        
                textMarkAdd = TextMessage(text="Ваша заявка успешно добавлен")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                res = make_response("Setting a cookie")
                res.set_cookie(str(viber_request.sender.id)[:8]+'buy2', '', max_age=60*60*24*365*2) 
                return res
            else:
                textMarkAdd = TextMessage(text="Вы не выбрали товар")   
                viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyClient])
                return Response(status=200)



        if message == 'Контакты':
            messageKeyMainMark = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_CLIENT)
            textMarkAdd = TextMessage(text="Вас приветствует авторазборка Auto Parts USA🔥\n☎️Наши контакты\nМТС 📲0991689891\nКиевстар 📲0976072454\nМы всегда готовы Вас проконсультировать.")   
            viber.send_messages(viber_request.sender.id, [textMarkAdd,messageKeyMainMark])
            return Response(status=200)
   

        if int(message):
            with sqlite3.connect("db.db") as con:  
                cursor_select_pass = con.cursor()
                cursor_select_pass.execute("SELECT * FROM offer WHERE id = ?",(message))   
                rows = cursor_select_pass.fetchall()[0]
            array_send = [TextMessage(text=' № '+str(rows[0])+' Название: '+str(rows[1])+' Цена: '+str(rows[2])+'\n\n Описание: '+str(rows[3])+'\n\n Время: '+str(rows[5]))]
            if rows[6] != None:
                for row in rows[6].split('devider'):
                    if row != 'None':
                        array_send.append(PictureMessage(media=str(row)))  

            KEYBOARD_BUY = {
            "Type": "keyboard",
            "Buttons": [
            {
            "Columns": 3,
            "Rows": 1,
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "КУК-"+str(rows[0])+'/'+str(rows[2]),
            "ReplyType": "message",
            "Text": "Купить"
            },
            {
            "Columns": 3,
            "Rows": 1,
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "КУ2-"+str(rows[0]),
            "ReplyType": "message",
            "Text": "Своя цена"
            },
            {
            "Columns": 3,
            "Rows": 1,
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "Контакты",
            "ReplyType": "message",
            "Text": "Контакты"
            },
            {
            "Columns": 3,
            "Rows": 1,
            "BgLoop": True,
            "ActionType": "reply",
            "ActionBody": "На главную",
            "ReplyType": "message",
            "Text": "На главную"
            },
            ]
            }
            buyKeys = KeyboardMessage(tracking_data='tracking_data', keyboard=KEYBOARD_BUY)
            array_send.append(buyKeys)


            viber.send_messages(viber_request.sender.id, array_send)
            return Response(status=200)


   
    return Response(status=200)


if __name__ == '__main__':
    # Will make the server available externally as well
    app.run(host='0.0.0.0',debug=True)
