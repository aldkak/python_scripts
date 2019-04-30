#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:57:27 2019

@author: msaif
"""
import requests,base64

def Handling_errors(func):
    def wrabber(*args,**kwargs):
        try:
            return fun(*args,**kwargs)
        except Exception as err:
            return "Error : {}".format(err)
    return wrabber

class TelegramBotHandler:
    def __init__(self, token="your_bot_token_paste_here"):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    @Handling_errors
    def get_updates(self, offset=None, timeout=30):
        """
        return information about the messages in json format
        """
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params=params)
        return resp.json()['result']

    @Handling_errors
    def send_message(self, chat_id, text):
        """
        send message take two args , chat id (int) and the message itself(str)
        """
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(url=self.api_url + method, params=params)
        return {"response":resp}
    @Handling_errors
    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]
        return {"response":last_update}

    @Handling_errors
    def get_chat_id(self):
        """
        ask user to write this command /subscribe
        token must be generate by
        """
        get_reuslt=self.get_updates()
        chat_ids=[]
        for item in get_reuslt:
            print(item)
            if item["message"]["text"]=='/subscribe':
                chat_ids.append(item["message"]["chat"]["id"])
        for chat_id in chat_ids:
            self.send_message(str(chat_id)," successfully subscribed ")
        return {"list_chat_ids":chat_ids}

def send_telegram_message(chat_id,message):
    """
    #instruction
    #1- create an object with the token  from the @botFather in telegram
    #2- you must have a chat_id , you can get it by get_updates or get_last_update
    # it will return the information in json format , loop through all of them get
    # the information and store it in file with all subscribers and thier chat_id
    """
    telegram=TelegramBotHandler()
    return telegram.send_message(chat_id,message)

def send_email(recipients,msg):
    """
    EmailNotifier  has just two parameters
    1- receiver_email : email to send the message to (string)
    2-  msg= the content of the message (string)
    you must pass a design of the message for example (message in html and css for browsers )
    you can specify the content type of the message in Content-type : text/html for example
    3- subject default==>Notification (string)
    note: make sure that you have smtplib, ssl packges installed on your machine
    """
    subject="Notification"
    import smtplib, ssl
    port = 465  # For SSL
    # configure the server of your Email address
    # keep in mine in some servers like gmail you must modify you account setting to accept
    # this type of connection
    #line 98: email of sender is no-replay@example.com ==> change to yours inside the script
    #line 104 : message with red text wrabbed inside a <div> and <p> tag
    message ="""From:no-replay@example.com
To:  {}
MIME-Version: 1.0
Content-type: text/html
Subject: {}

<div><p style="color:red;font-family:courier;font-size:160%;">{}</p></div>
""".format(recipients,subject,msg)
    #line 108-110 :  change server , email and password to yours.
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('stmp_email_srver(example==> smtp.yandex.ru)', port, context=context) as server:
        server.login('no-replay@example.com', 'email_password')
        server.sendmail('no-replay@example.com', recipients, message)
        return {"status":"Email has been sent" ,"To":recipients,"subject":subject,"Text":msg}
