from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import os

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot('5552135835:AAF1fqFhHPH_mZmtHX4A_6hiHJuYh_vV-eo')#token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

answ = dict()

#Конопка ссилка
urlkb = InlineKeyboardMarkup(row_width=1)
urlButton = InlineKeyboardButton(text='Ссилка', url = 'youtube.com/watch?v=gpCIfQUbYlY')
urlButton2 = InlineKeyboardButton(text='Ссилка', url = 'youtube.com/watch?v=gpCIfQUbYlY')
urlkb.add(urlButton, urlButton2)

@dp.message_handler(commands='посилання')
async def url_command(message: types.Message):
    await message.answer('Посилання:', reply_markup=urlkb)

inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Like', callback_data='like_1'),\
                                             InlineKeyboardButton(text='Not Like', callback_data='like_-1'))


@dp.message_handler(commands='test')
async def test_command(message : types.Message):
    await message.answer('за відео', reply_markup=inkb)

@dp.callback_query_handler(Text(startswith='like_'))
async def www_call(callback : types.CallbackQuery):
    res = int(callback.data.split('_')[1])
    if f'{callback.from_user.id}' not in answ:
        answ[f'{callback.from_user.id}'] = res
        await callback.answer('ви проголосували')
    else:
        await callback.answer('ви вже проголосували', show_alert=True)


executor.start_polling(dp,skip_updates=True)