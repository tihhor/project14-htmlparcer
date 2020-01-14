import telebot
from telebot import apihelper
import time
import os
from parcer import curr_parcer

import parcer

TOKEN = '983129325:AAGeCTPbV0oXc54Ox5CaC6aUI98knTLqBbk'

date_to_print = ''

# proxies = {
#     'http': 'http://167.86.96.4:3128',
#     'https': 'http://167.86.96.4:3128',
# }
#
# apihelper.proxy = proxies

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я бот курсов валют Центрального Банка России!")
    bot.send_message(message.chat.id, "Чтобы узнать курсы валют на определенную дату:")
    bot.send_message(message.chat.id, 'Введите дату командой:  /date ДД.MM.ГГГГ')
    bot.send_message(message.chat.id, 'Введите коды валют командой:  /curr AAA BBB ...')

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Команды:")
    bot.send_message(message.chat.id, '/date ДД.MM.ГГГГ  - ввод даты в указанном формате. Последняя введенная дата сохраняется. При неверном формате используется текущая дата')
    bot.send_message(message.chat.id, '/curr AAA BBB ... - ввод кодов курсов валют через пробел. Например: USD EUR GBP ...')

# Обработка команд
@bot.message_handler(commands=['date'])
def get_date(message):
    global date_to_print
    date_to_print = ' '.join(message.text.split(' ')[1:])
    bot.reply_to(message,  f'Дата: {date_to_print}')


@bot.message_handler(commands=['curr'])
def get_curr(message):
    global date_to_print
    curr_to_print = ' '.join(message.text.split(' ')[1:])
    bot.reply_to(message,  f'Коды валют: {curr_to_print}')
    ans = curr_parcer(curr_to_print, date_to_print)
    for str_ans in ans:
        bot.send_message(message.chat.id, str_ans)



bot.polling()