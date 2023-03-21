from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

funcs_in_row = 1

'''
    Functions dictionary: "callback data": "function name in tg"
'''
app_func_audio_work = 'audio_work'
app_func_video_work = 'video_work'
funcs = {
    app_func_audio_work: 'Work with audio',
    app_func_video_work: 'Work with video'
}


# Get inline keyboard for app functions
def app_funcs_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = funcs_in_row

    for key, value in funcs.items():
        markup.add(InlineKeyboardButton(value, callback_data=key))

    return markup
