from telebot import TeleBot

from src.BotHandlers.CallbackHandlers import audio_source_for_video
from src.BotHandlers.MediaHandlers import audio_file_handler, youtube_link_audio_handler, video_file_handler, \
    audio_file_for_video_handler, youtube_link_audio_for_video_handler, youtube_link_video_handler
from src.KeyboardLayouts.InlineKeyboards.AppFuncs import app_funcs_keyboard
from src.KeyboardLayouts.InlineKeyboards.AudioFuncsKeyboard import audio_speed_func, audio_funcs_keyboard, \
    audio_pitch_func, audio_reverb_func, audio_bass_boost_func
from src.KeyboardLayouts.InlineKeyboards.AudioSourceKeyboard import audio_source_from_file, audio_source_from_youtube
from src.KeyboardLayouts.InlineKeyboards.VideoSourceKeyboard import video_source_from_file, video_source_from_youtube
from src.KeyboardLayouts.ReplyKeyboards.CommandsKeyboard import starting_keyboard
from src.classes.AudioEditor import AudioEditor
from src.classes.UserInputWaiter import user_input_waiter
from src.classes.UsersFunctionsDict import users_functions_dict


def get_audio_funcs_markup_for_user(user_id):
    markup = audio_funcs_keyboard()
    if users_functions_dict.audio_funcs_dict.keys().__contains__(user_id):
        user_audio_funcs = []
        for func in users_functions_dict.audio_funcs_dict[user_id]:
            user_audio_funcs.append(next(iter(func.keys())))

        to_delete_buttons = []
        for row in markup.keyboard:
            button = row[0]
            if user_audio_funcs.__contains__(button.callback_data):
                to_delete_buttons.append(row)

        for to_delete_button in to_delete_buttons:
            markup.keyboard.remove(to_delete_button)

    return markup


# Handler for any message from user from whom the bot is waiting for the source
def message_from_waited_user_handler(bot: TeleBot, message):
    if user_input_waiter.is_waiting_for_input(message.chat.id, audio_source_for_video):
        if message.audio:
            return audio_file_for_video_handler(bot, message)
        else:
            return youtube_link_audio_for_video_handler(bot, message)

    if message.audio and user_input_waiter.is_waiting_for_input(message.chat.id, audio_source_from_file):
        return audio_file_handler(bot, message)

    if message.video and user_input_waiter.is_waiting_for_input(message.chat.id, video_source_from_file):
        return video_file_handler(bot, message)

    if user_input_waiter.is_waiting_for_input(message.chat.id, audio_source_from_youtube):
        return youtube_link_audio_handler(bot, message)

    if user_input_waiter.is_waiting_for_input(message.chat.id, video_source_from_youtube):
        return youtube_link_video_handler(bot, message)

    if user_input_waiter.is_waiting_for_input(message.chat.id, audio_speed_func):
        if 0 < float(message.text) <= 3.0:
            user_input_waiter.end_waiting_for_user_input(
                message.chat.id,
                audio_speed_func
            )
            users_functions_dict.add_user_audio_func(message.chat.id, audio_speed_func, float(message.text))
            return bot.send_message(
                message.chat.id,
                "Choose function you want to execute",
                reply_markup=get_audio_funcs_markup_for_user(message.chat.id)
            )

    if user_input_waiter.is_waiting_for_input(message.chat.id, audio_pitch_func):
        if 0 < float(message.text) <= 3.0:
            user_input_waiter.end_waiting_for_user_input(
                message.chat.id,
                audio_pitch_func
            )
            users_functions_dict.add_user_audio_func(message.chat.id, audio_pitch_func, float(message.text))
            return bot.send_message(
                message.chat.id,
                "Choose function you want to execute",
                reply_markup=get_audio_funcs_markup_for_user(message.chat.id)
            )

    if user_input_waiter.is_waiting_for_input(message.chat.id, audio_reverb_func):
        if 0 < int(message.text) <= 100:
            user_input_waiter.end_waiting_for_user_input(
                message.chat.id,
                audio_reverb_func
            )
            users_functions_dict.add_user_audio_func(message.chat.id, audio_reverb_func, int(message.text))
            return bot.send_message(
                message.chat.id,
                "Choose function you want to execute",
                reply_markup=get_audio_funcs_markup_for_user(message.chat.id)
            )

    if user_input_waiter.is_waiting_for_input(message.chat.id, audio_bass_boost_func):
        if 0 < int(message.text) <= 25:
            user_input_waiter.end_waiting_for_user_input(
                message.chat.id,
                audio_bass_boost_func
            )
            users_functions_dict.add_user_audio_func(message.chat.id, audio_bass_boost_func, int(message.text))
            return bot.send_message(
                message.chat.id,
                "Choose function you want to execute",
                reply_markup=get_audio_funcs_markup_for_user(message.chat.id)
            )

    bot.send_message(
        message.chat.id,
        ', '.join(user_input_waiter.usersInputWaiter.get(message.chat.id))
    )


# Handler for work starting message "Start work"
def message_start_work_handler(bot, message):
    bot.send_message(
        message.chat.id,
        "Choose function",
        reply_markup=app_funcs_keyboard()
    )


# Handler for
def question_message_handler(bot, message):
    bot.reply_to(
        message,
        "Do you wanna start working?",
        reply_markup=starting_keyboard()
    )
