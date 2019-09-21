import os
import re
import sys; sys.setrecursionlimit(10000)
import time
import json
import logging

import telebot
from tqdm import tqdm

import utils
from methods import T2S, S2T


telebot.apihelper.proxy = ...
bot = telebot.TeleBot(...)

logging.basicConfig(filename='logs.txt', level=logging.INFO, filemode="w")


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, 'Help')


@bot.message_handler(content_types=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Start')


@bot.message_handler(content_types=['voice'])
@utils.trier
@utils.logger
def handle_file(message):
    S2T(bot).transform(message.voice.file_id).send(message.chat.id)


@bot.message_handler(content_types=['text'])
@utils.trier
@utils.logger
def handle_text(message):
    T2S(bot).transform(message.text).send(message.chat.id)


if __name__ == '__main__':
    while True:
        try:
            print('start')
            logging.info('start')
            bot.polling(none_stop=True, timeout=0)
        except Exception as e:
            print('restart')
            logging.info('restart')
        for i in tqdm(range(10), 'Restart: '):
            time.sleep(1)