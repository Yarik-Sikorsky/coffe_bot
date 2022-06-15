from aiogram import types
from aiogram.dispatcher import Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db

#@dp.message_handler(commands=['start','help'])
async def command_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Смачного',reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('спілкуйтесь з ботом в ЛС !\n https://t.me/coffee_border_bot')


#@dp.message_handler(commands=['Графік_роботи'])
async def coffe_open_command(message : types.Message):
        await bot.send_message(message.from_user.id, 'Пн-Пт з 9:00 до 21:00')


#@dp.message_handler(commands=['Де_ви'])
async def coffe_place_command(message : types.Message):
        await bot.send_message(message.from_user.id, 'Біля БУга',reply_markup=ReplyKeyboardRemove())

#dp.message_handler(commands=['Меню'])
async def coffe_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start,commands=['start','help'])
    dp.register_message_handler(coffe_open_command,commands=['Графік_роботи'])
    dp.register_message_handler(coffe_place_command,commands=['Де_ви'])
    dp.register_message_handler(coffe_menu_command,commands=['Меню'])
