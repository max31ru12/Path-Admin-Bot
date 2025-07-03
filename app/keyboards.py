from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class KeyboardMessages:
    ORGANIZE_MEETING = "Запланировать встречу"
    CANCEL_ADDING = "Отменить планирование встречи"


base_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=KeyboardMessages.ORGANIZE_MEETING)]
    ],
    resize_keyboard=True
)

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=KeyboardMessages.CANCEL_ADDING)]
    ],
    resize_keyboard=True
)