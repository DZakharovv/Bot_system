#!/usr/bin/python
import config
import telegram
import os
import subprocess
import sys
import shlex
import datetime
import emoji
import telebot
# import functools
# from functools import wraps
from subprocess import Popen, PIPE
from telegram.ext import CommandHandler
from imp import reload

from telegram.ext import Updater

updater = Updater(token=config.token)
dispatcher = updater.dispatcher
tgm_com_dir = "/root/telegram-bot/bot"

#################################################################################

from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardMarkup


# joke_keyboard = [['/Шути_ещё'], ['/Список_команд']]
# joke_markup = ReplyKeyboardMarkup(joke_keyboard, one_time_keyboard=True, resize_keyboard=True)


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


#################################################################################


def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    global textoutput
    textoutput = ''
    while True:
        global output
        output = process.stdout.readline()
        output = output.decode('utf8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print(emoji.emojize(output.strip()))
        textoutput = textoutput + '\n' + output.strip()
    rc = process.poll()
    return rc


def start(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin:
        bot.sendMessage(chat_id=update.message.chat_id, text="Добрый день!")


def help(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin:
        bot.sendMessage(chat_id=update.message.chat_id, text='''Список доступных команд:
        /help - помощь
        /id - id пользователя
        /test - тестовая команда
        /users_online - пользователи онлайн
        /kettle_on - включить чайник
        /joke - рассказать шуточку
        /moncam - прислать фото с камеры мониторинга
        /bookcam - прислать фото с камеры ноута
        ''')


# def testik(bot, update):
#    reload(config)
#    user = str(update.message.from_user.id)
#    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
#        markup = telebot.types.InlineKeyboardMarkup()
#        markup.add(telebot.types.InlineKeyboardButton(text='Три', callback_data=3))
#        markup.add(telebot.types.InlineKeyboardButton(text='Четыре', callback_data=4))
#        markup.add(telebot.types.InlineKeyboardButton(text='Пять', callback_data=5))
#        bot.sendMessage(chat_id=update.message.chat_id, text="test", reply_markup=markup)


####################################################################################
# Добавить описание новой команды выше
####################################################################################

# функция для декорации отправки картинки


# функция команады id
def myid(bot, update):
    userid = update.message.from_user.id
    bot.sendMessage(chat_id=update.message.chat_id, text=userid)


# функция команады test
def test(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin:  # если пользовательский id в списке admin то команда выполняется
        custom_keyboard = [['top-left', 'top-right'],
                           ['bottom-left', 'bottom-right']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        run_command("curlsh")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput, reply_markup=reply_markup)


# функция команады users_online
def users_online(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin:  # если пользовательский id в списке admin то команда выполняется
        #        bot.sendMessage(chat_id=update.message.chat_id, text="Сканирую, ждите...")
        run_command('/bin/bash /root/telegram-bot/bot/online.sh')
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)


def kettle_on(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin:  # если пользовательский id в списке admin то команда выполняется
        bot.sendMessage(chat_id=update.message.chat_id, text="Пробую включить чайник...")
        run_command('/bin/bash /root/telegram-bot/bot/kettle.sh %(name)s' % {'name': update.message.chat_id})
        #        run_command("kettle_on")
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)


def joke(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.admin:  # если пользовательский id в списке admin то команда выполняется
        run_command('/bin/bash /root/telegram-bot/bot/joke.sh')
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)


def bookcam(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.cam:  # если пользовательский id в списке admin то команда выполняется
        run_command('/bin/bash /root/telegram-bot/bot/bookcam.sh')
        bot.send_photo(chat_id=update.message.chat_id, photo=open('/root/telegram-bot/bot/Img/bookcam/image.jpg', 'rb'),
                       caption="Список команд /help")
    if user not in config.cam:
        bot.sendMessage(chat_id=update.message.chat_id, text="А Вам сюда нельзя!")


def moncam(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.cam:  # если пользовательский id в списке admin то команда выполняется
        run_command('/bin/bash /root/telegram-bot/bot/moncam.sh')
        bot.send_photo(chat_id=update.message.chat_id, photo=open('/root/telegram-bot/bot/Img/moncam/image.jpg', 'rb'),
                       caption="Список команд /help")
    if user not in config.cam:
        bot.sendMessage(chat_id=update.message.chat_id, text="А Вам сюда нельзя!")


def workout(bot, update):
    reload(config)
    user = str(update.message.from_user.id)
    if user in config.workout:  # если пользовательский id в списке workout то команда выполняется
        run_command('/bin/bash /root/telegram-bot/bot/workout/workout.sh %(name)s' % {'name': user})
        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)
    if user not in config.workout:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="А ты куда - тебя в группе нет! Запишись в группу WORKOUT и тренься!")


#################################  [1]  ###########################################################
########## Вставить этот код выше с новой переменой, заменить test своим названием ################
##функция команады test
# def test(bot, update):
#    reload(config)
#    user = str(update.message.from_user.id)
#    if user in config.admin: #если пользовательский id в списке admin то команда выполняется
#        run_command("test")
#        bot.sendMessage(chat_id=update.message.chat_id, text=textoutput)
###################################################################################################

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

test_handler = CommandHandler('test', test)
dispatcher.add_handler(test_handler)

myid_handler = CommandHandler('id', myid)
dispatcher.add_handler(myid_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

users_online_handler = CommandHandler('users_online', users_online)
dispatcher.add_handler(users_online_handler)

kettle_on_handler = CommandHandler('kettle_on', kettle_on)
dispatcher.add_handler(kettle_on_handler)

joke_handler = CommandHandler('joke', joke)
dispatcher.add_handler(joke_handler)

# testik_handler = CommandHandler('testik', testik)
# dispatcher.add_handler(testik_handler)

bookcam_handler = CommandHandler('bookcam', bookcam)
dispatcher.add_handler(bookcam_handler)

moncam_handler = CommandHandler('moncam', moncam)
dispatcher.add_handler(moncam_handler)

workout_handler = CommandHandler('workout', workout)
dispatcher.add_handler(workout_handler)

###################################  [2]  #########################################################
########## Вставить этот код выше с новой переменой, заменить test своим названием ################
# test_handler = CommandHandler('test', test)
# dispatcher.add_handler(test_handler)
###################################################################################################

###################################  [3]  #########################################################
# сделать символическую ссылку на свою команды на сервере
# ln -s /root/telegram-bot/bot/test.sh /usr/sbin/test
###################################################################################################
updater.start_polling()
