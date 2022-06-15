from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()


#bot = Bot(token=os.getenv('TOKEN'))
bot = Bot('5552135835:AAF1fqFhHPH_mZmtHX4A_6hiHJuYh_vV-eo')
dp = Dispatcher(bot,storage = storage)

