from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

audio_funcs_in_row = 1

"""
    Audio funcs dictionary: "callback data": "audio_func"
"""
audio_speed_func = 'audio_speed_func'
audio_pitch_func = 'audio_pitch_func'
audio_reverb_func = 'audio_reverb_func'
audio_bass_boost_func = 'audio_bass_boost_func'
end_selecting_audio_func = 'end_selecting_audio_func'
audio_funcs = {
    audio_speed_func: 'Change play speed',
    audio_pitch_func: 'Change audio pitch',
    audio_reverb_func: 'Apply reverb',
    audio_bass_boost_func: 'Apply bass boost',
    end_selecting_audio_func: 'Confirm'
}


def audio_funcs_keyboard():
    markup = InlineKeyboardMarkup()

    for key, value in audio_funcs.items():
        markup.add(InlineKeyboardButton(value, callback_data=key))

    return markup
