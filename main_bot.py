import asyncio
import time
import logging
import config
import subprocess
import shlex
import emoji
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.token)
dp = Dispatcher(bot=bot)


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


@dp.message_handler(commands=['start'])
async def start_kettle_handler(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    text_and_data = (
        ('В меню', 'on_menu'),
        ('Помощь', 'help'),
        ('Мимо проходил...', 'walk'),

    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.add(*row_btns)
    await bot.send_message(chat_id=message.from_user.id, text="Привет!\nА Вам куда?", reply_markup=keyboard_markup)


@dp.callback_query_handler(text='walk')
async def walk_user_handler(query: types.CallbackQuery):
    await bot.send_message(chat_id=query.from_user.id, text="Давай до свиданья")
    await asyncio.sleep(5)
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    text_and_data = (
        ('В меню', 'on_menu'),
        ('Помощь', 'help'),
        ('Мимо проходил...', 'walk'),

    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.add(*row_btns)
    await bot.send_message(chat_id=query.from_user.id, text="Привет!\nА Вам куда?", reply_markup=keyboard_markup)


@dp.callback_query_handler(text='kettle_on')
async def start_kettle_handler(query: types.CallbackQuery):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    text_and_data = (
        ('Включить', 'on'),
        ('Температура', 'tmp'),
        ('В меню', 'on_menu'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.add(*row_btns)
    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                text="Задание для чайника:")
    await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                        reply_markup=keyboard_markup)


@dp.callback_query_handler(text='on')
async def start_kettle_on_handler(query: types.CallbackQuery):
    user = str(query.from_user.id)
    if user in config.admin:
        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    text="Пробую включить...")

        run_command('/bin/bash /root/telegram-bot/bot/kettle.sh %(name)s' % {'name': query.message.chat_id})
        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    text=textoutput)
        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
        text_and_data = (
            ('Включить', 'on'),
            ('Температура', 'tmp'),
            ('В меню', 'on_menu'),
        )

        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.add(*row_btns)

        await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                            reply_markup=keyboard_markup)
        # await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)


@dp.callback_query_handler(text='tmp')
async def kettle_tmp_func(query: types.CallbackQuery):
    user = str(query.from_user.id)
    if user in config.admin:
        run_command('/bin/bash /root/telegram-bot/bot/kettle_temp.sh')
        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
        text_and_data = (
            ('Включить', 'on'),
            ('Температура', 'tmp'),
            ('В меню', 'on_menu'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.add(*row_btns)
        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    text=textoutput)
        await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                            reply_markup=keyboard_markup)


@dp.callback_query_handler(text='id')
async def get_id(query: types.CallbackQuery):
    # await bot.send_message(query.from_user.id, text=)
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    text_and_data = (
        ('В меню', 'on_menu'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

    keyboard_markup.add(*row_btns)

    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                text=query.from_user.id)
    await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=query.message.message_id,
                                        reply_markup=keyboard_markup)


@dp.callback_query_handler(text='help')
async def help_func(query: types.CallbackQuery):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    text_and_data = (
        ('Получить ID', 'id'),
        ('В меню', 'on_menu'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

    keyboard_markup.add(*row_btns)

    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                text="Меню помощи:")
    await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=query.message.message_id,
                                        reply_markup=keyboard_markup)


@dp.callback_query_handler(text='on_menu')
async def menu(query: types.CallbackQuery):
    user = str(query.from_user.id)
    if user in config.admin:
        keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
        text_and_data = (
            ('Чайник', 'kettle_on'),
            # ('ID', 'id'),
            ('В сети', 'users_online'),
            ('Шутка', 'joke'),
            ('Камеры', 'cams'),
            # ('test', 'test'),
            ('Помощь', 'help'),
        )

        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

        keyboard_markup.add(*row_btns)

        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    text="Основное меню:")
        await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=query.message.message_id,
                                            reply_markup=keyboard_markup)
    else:
        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    text="А Вам сюда нельзя!")


# @dp.callback_query_handler(text='test')
@dp.callback_query_handler(text='users_online')
async def users_online_func(query: types.CallbackQuery):
    user = str(query.from_user.id)
    if user in config.admin:
        run_command('/bin/bash /root/telegram-bot/bot/online.sh')
        keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
        text_and_data = (
            ('В меню', 'on_menu'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

        keyboard_markup.add(*row_btns)

        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    text=textoutput)
        await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=query.message.message_id,
                                            reply_markup=keyboard_markup)


@dp.callback_query_handler(text='joke')
async def joke(query: types.CallbackQuery):
    user = str(query.from_user.id)
    if user in config.admin:
        run_command('/bin/bash /root/telegram-bot/bot/joke.sh')
        keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
        text_and_data = (
            ('В меню', 'on_menu'),
        )
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

        keyboard_markup.add(*row_btns)

        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    text=textoutput)
        await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=query.message.message_id,
                                            reply_markup=keyboard_markup)


@dp.callback_query_handler(text='moncam')
async def monitoring_camera(query: types.CallbackQuery):
    # await bot.send_message(chat_id=query.from_user.id, text="Камера не подключена")
    run_command('/bin/bash /root/telegram-bot/bot/moncam.sh')
    # await asyncio.sleep(5)
    bot.send_photo(chat_id=query.from_user.id, photo=open('/root/telegram-bot/bot/Img/moncam/image.jpg', 'rb'))
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    text_and_data = (
        ('Мониторинг', 'moncam'),
        ('Бук', 'bookcam'),
        ('В меню', 'on_menu'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

    keyboard_markup.add(*row_btns)

    await bot.send_message(chat_id=query.from_user.id, text="Меню камер:", reply_markup=keyboard_markup)


# @dp.callback_query_handler(text='bookcam')
@dp.callback_query_handler(text='cams')
async def cams_func(query: types.CallbackQuery):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2)
    text_and_data = (
        ('Мониторинг', 'moncam'),
        ('Бук', 'bookcam'),
        ('В меню', 'on_menu'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

    keyboard_markup.add(*row_btns)

    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                text="Меню камер:")
    await bot.edit_message_reply_markup(chat_id=query.from_user.id, message_id=query.message.message_id,
                                        reply_markup=keyboard_markup)


if __name__ == '__main__':
    executor.start_polling(dp)
