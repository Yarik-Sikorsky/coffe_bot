from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

#Отримуєм ID теперіщнього модератора
@dp.message_handler(commands=['moderator'], is_chat_admin = True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id

    await bot.send_message(message.from_user.id, 'Що тобі потрібно??? ', reply_markup=admin_kb.button_case_admin)
    await message.delete()


#Початок діалогу загрузки нового пункту меню
#@dp.message_handler(commands='Завантажити', state=None)
async def cm_state(message : types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Завантажити фото')


#Вихід з состояния
#@dp.message_handler(state="*",commands='відміна')
#@dp.message_handler(Text(equals='відміна',ignor_case=True), state="*")
async def cancrl_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')



#Ловимо першу відповідь користувача
#@dp.message_handler(content_types=['photo'], state=FMSAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Тепер введи назву')

#Ловимо другу відповідь
#@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введіть опис')


#Ловимо третю відповідь
#@dp.message_handler(state=FSMAdmin.description)
async def load_discription(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Тепер вкажи ціну')


#Ловимо четверту відповідь
#@dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        await sqlite_db.sql_add_command(state)
        await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ',''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} видалено.', show_alert=True)


#@dp.message_handler(commands='Видалити')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n Опис: {ret[2]}\n Ціна: {ret[-1]}')
            inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text=f'Видалити {ret[1]}', callback_data=f'del {ret[1]}'))
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=inkb)


#Реєструємо хеедлери
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_state,commands=['Завантажити'], state=None)
    dp.register_message_handler(cancrl_handler, state="*", commands='відміна')
    dp.register_message_handler(cancrl_handler, Text(equals='відміна', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_discription, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin = True)
#    dp.register_message_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_item, commands='Видалити')