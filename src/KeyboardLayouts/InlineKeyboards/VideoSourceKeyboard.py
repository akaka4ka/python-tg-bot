from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

sources_in_row = 1

"""
    Audio sources dictionary: "callback data": "video_source"
"""
video_source_from_file = 'from_video_file'
video_source_from_youtube = 'from_youtube_video'
video_sources = {
    video_source_from_file: 'Load as video file',
    video_source_from_youtube: 'Load as youtube link'
}


# Get inline keyboard for audio sources
def video_sources_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = sources_in_row

    for key, value in video_sources.items():
        markup.add(InlineKeyboardButton(value, callback_data=key))

    return markup
