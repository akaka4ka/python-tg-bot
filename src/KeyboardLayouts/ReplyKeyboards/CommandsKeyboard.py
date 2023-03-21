from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def starting_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, is_persistent=True)
    audio_effects_btn = KeyboardButton("Start work")
    markup.add(audio_effects_btn)
    return markup
