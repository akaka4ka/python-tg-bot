from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

video_funcs_in_row = 1

"""
    Video funcs dictionary: "callback data": "video_func"
"""
video_loop_on_music_func = 'video_loop_on_music_func'
video_overlap_with_music = 'video_overlap_with_music'
video_funcs = {
    video_loop_on_music_func: 'Loop a video to music',
    video_overlap_with_music: 'Superimpose music on a video'
}


def video_funcs_keyboard():
    markup = InlineKeyboardMarkup()

    for key, value in video_funcs.items():
        markup.add(InlineKeyboardButton(value, callback_data=key))

    return markup
