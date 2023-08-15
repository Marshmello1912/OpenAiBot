from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

chat = InlineKeyboardButton('ChatGpt', callback_data= '/ask')
image = InlineKeyboardButton("Image generation", callback_data='/img')

exitB = KeyboardButton('На главную')

selectChat = InlineKeyboardMarkup().row(chat).row(image)
exitChat = ReplyKeyboardMarkup(resize_keyboard= True).add(exitB)
clear = ReplyKeyboardRemove()