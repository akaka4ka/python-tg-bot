from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

sources_in_row = 1

"""
    Audio sources dictionary: "callback data": "audio_source"
"""
audio_source_from_file = 'from_audio_file'
audio_source_from_youtube = 'from_youtube_audio'
audio_sources = {
    audio_source_from_file: 'Load as audio file',
    audio_source_from_youtube: 'Load as youtube link'
}


# Get inline keyboard for audio sources
def audio_sources_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = sources_in_row

    for key, value in audio_sources.items():
        markup.add(InlineKeyboardButton(value, callback_data=key))

    return markup
