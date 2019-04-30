#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:32:43 2019

1.make sure that you have  pika module installed on your machine
#pip install pika
2.install rabbitmq
# it depend on you platform (better to google it)
@author: msaif
"""
import pika
def send_to_queue(msg,queue,server='ip-server',port='port',user='rabbitmq-user',code='rabbitmq-user-password'):
    """
    paprameters:
    msg:message to send to  rabitmq server
    queue : queue name , if it doesn't exist create new (to store messages)
    RabbitMQ_server info : rabbitmq server to connect to :
        1- RabbitMQ server's ip address
        2- port on which RabbitMQ server was configure to run .
        3. user and code(password) of RabbitMQ server user (credentials)
    function has no return
    """
    credentials = pika.PlainCredentials(user, code)
    parameters = pika.ConnectionParameters(server,port,'/',credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=msg)
    print (" [x] Sent '{}! to {}'".format(msg,queue))
    connection.close()


def receive_from_queue(queue,server='ip-server',port='port',user='rabbitmq-user',code='rabbitmq-user-password'):
    """
    parameters:
    queue : queue name to fetch message from
    RabbitMQ_server info : rabbitmq server to connect to :
        1- RabbitMQ server's ip address
        2- port on which RabbitMQ server was configure to run .
        3. user and code(password) of RabbitMQ server user (credentials)
    function will return one message for every call by the rule "FIFO"
    First In First Out
    """
    credentials = pika.PlainCredentials(user, code)
    parameters = pika.ConnectionParameters(server,port,'/',credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    method_frame, header_frame, body = channel.basic_get(queue = queue)
    if method_frame:
        if method_frame.NAME == 'Basic.GetEmpty':
            connection.close()
            return ''
        else:
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            print(' [*] Waiting for messages. To exit press CTRL+C')
            connection.close()
            print(" [X]  message has been fetched from {}".format(queue))
            return body
    else:
        print(" [X]  No messages")
