import time
import logging
import config

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_cmd_handler(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    text_and_data = (
        ('Помощь', 'help'),
        ('ID', 'id'),
        ('test', 'test'),
        ('В сети', 'users_online'),
        ('Чайник', 'kettle_on'),
        ('Шутка', 'joke'),
        ('Мониторинг', 'moncam'),
        ('Бук', 'bookcam'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

    keyboard_markup.add(*row_btns)

    await bot.send_message(chat_id=message.from_user.id, text="Привет!\nЧего надобно, старче?",
                           reply_markup=keyboard_markup)



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
    await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text="Чайник готов")
    await bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=keyboard_markup)

@dp.callback_query_handler(text='id')
@dp.callback_query_handler(text='test')
@dp.callback_query_handler(text='help')
@dp.callback_query_handler(text='users_online')
@dp.callback_query_handler(text='joke')
@dp.callback_query_handler(text='moncam')
@dp.callback_query_handler(text='bookcam')

@dp.callback_query_handler(text='on_menu')

async def menu(query: types.CallbackQuery):


async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    answer_data = query.data
    await query.answer(f'You answered with {answer_data!r}')

    if answer_data == 'yes':
        text = 'Great, me too!'
    elif answer_data == 'no':
        text = 'Oh no...Why so?'
    elif answer_data == 'help':
        text = '/help'
    else:
        text = f'Unexpected callback data {answer_data!r}!'

    await bot.send_message(query.from_user.id, text)


if __name__ == '__main__':
    executor.start_polling(dp)
