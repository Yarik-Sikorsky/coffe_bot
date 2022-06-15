from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
import os, hashlib


#bot = Bot(token=os.getenv('TOKEN'))
bot = Bot('5552135835:AAF1fqFhHPH_mZmtHX4A_6hiHJuYh_vV-eo')
dp = Dispatcher(bot)

@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or 'echo'
    link = 'https://uk.wikipedia.org/wiki/'+text
    result_id: str = hashlib.md5(text.encode()).hexdigest()

    articles = [types.InlineQueryResultArticle(
        id = result_id,
        title = 'Стаття вікипедія',
        url = link,
        inpud_message_content = types.InputTextMessageContent(
            message_text = link))]

    await query.answer(articles, cache_time=1, is_personal=True)

executor.start_polling(dp, skip_updates=True)

