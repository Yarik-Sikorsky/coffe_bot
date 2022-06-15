from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

b1 = KeyboardButton('/Графік_роботи')
b2 = KeyboardButton('/Де_ви')
b3 = KeyboardButton('/Меню')
#b4 = KeyboardButton('Поділитись номером', request_contact=True)
#b5 = KeyboardButton('Відправити де я', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b1,b2,b3)
