from aiogram import types
from aiogram.dispatcher import Dispatcher
from create_bot import dp
import json, string


#@dp.message_handler()
async def echo_send(message : types.Message):
    if {i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('list_mat.json')))) != set():
        await message.reply('Нецензурщина заборонена')
        await message.delete()

def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(echo_send)

