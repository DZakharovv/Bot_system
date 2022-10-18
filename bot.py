import time
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

logging.basicConfig(level=logging.INFO)

TOKEN = "5572620592:AAHMnYrYZ3DEkT1mxG6sKa9ctz9zW66Ms30"
MSG = "Are you here?"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


# @dp.message_handler(commands=['start'])
# async def start_handler(message: types.Message):
#     user_id = message.from_user.id
#     user_name = message.from_user.first_name
#     user_full_name = message.from_user.full_name
#     logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
#     await message.reply(f"Привет, {user_full_name}!")
#
#     for i in range(10):
#         time.sleep(60)
#         await bot.send_message(user_id, MSG.format(user_name))

@dp.message_handler(commands=['start'])
async def start_cmd_handler(message: types.Message):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=4)
    text_and_data = (
        ('help', 'help'),
        ('help2', 'help'),
        ('help3', 'help'),
        ('help4', 'help'),
        ('help5', 'help'),
        ('help6', 'help'),
        ('help7', 'help'),
        ('help8', 'help'),
        ('help9', 'help'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)

    keyboard_markup.add(*row_btns)
    # keyboard_markup.add(*row_btns_2)

    await message.reply("Hi!\nDo you love aiogram?", reply_markup=keyboard_markup)


@dp.callback_query_handler(text='no')
@dp.callback_query_handler(text='yes')
@dp.callback_query_handler(text='help')
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
