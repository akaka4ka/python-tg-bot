import os

from telebot import TeleBot

from src.KeyboardLayouts.InlineKeyboards.AppFuncs import app_func_audio_work, app_func_video_work
from src.KeyboardLayouts.InlineKeyboards.AudioFuncsKeyboard import audio_speed_func, end_selecting_audio_func, \
    audio_pitch_func, audio_reverb_func, audio_bass_boost_func
from src.KeyboardLayouts.InlineKeyboards.AudioSourceKeyboard import audio_sources_keyboard, audio_sources, \
    audio_source_from_file, audio_source_from_youtube
from src.KeyboardLayouts.InlineKeyboards.VideoFuncsKeyboard import video_loop_on_music_func, video_overlap_with_music
from src.KeyboardLayouts.InlineKeyboards.VideoSourceKeyboard import video_sources_keyboard, video_sources, \
    video_source_from_file, video_source_from_youtube
from src.classes.UserInputWaiter import user_input_waiter
from src.classes.UsersFunctionsDict import users_functions_dict


audio_source_for_video = 'audio_source_for_video'


def callback_from_waited_user_handler(bot, callback):
    bot.send_message(
        callback.message.chat.id,
        ', '.join(user_input_waiter.usersInputWaiter.get(callback.message.chat.id))
    )


# Handler for app function selection via inline keyboard
def callback_func_choose_handler(bot, callback):
    new_message = ''
    new_keyboard = ''

    if callback.data == app_func_audio_work:
        new_message = 'Choose audio source'
        new_keyboard = audio_sources_keyboard()

    if callback.data == app_func_video_work:
        new_message = 'Choose video source'
        new_keyboard = video_sources_keyboard()

    # Edit message for chosen function
    bot.edit_message_text(
        new_message,
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=new_keyboard
    )


# Handler for audio source selection via inline keyboard
def callback_audio_source_handler(bot, callback):
    user_input_waiter.add_user_input_waiter(callback.message.chat.id, callback.data)

    if callback.data == audio_source_from_file:
        # Edit message for chosen function
        bot.edit_message_text(
            'Okay! Now, send me your audio file.',
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=None
        )

    if callback.data == audio_source_from_youtube:
        # Edit message for chosen function
        bot.edit_message_text(
            'Okay! Now, send me YouTube link (only full links or shorten by YouTube).',
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=None
        )


# Handler for video source selection via inline keyboard
def callback_video_source_handler(bot, callback):
    user_input_waiter.add_user_input_waiter(callback.message.chat.id, callback.data)

    if callback.data == video_source_from_file:
        text = """Okay! Now, send me your video file.
But please note, the size of the video file cannot exceed 20 MB."""
        # Edit message for chosen function
        bot.edit_message_text(
            text,
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=None
        )

    if callback.data == video_source_from_youtube:
        text = "Okay! Now, send me YouTube link (only full links or shorten by YouTube)."
        # Edit message for chosen function
        bot.edit_message_text(
            text,
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=None
        )


# Handler for audio function selection via inline keyboard
def callback_audio_func_handler(bot: TeleBot, callback):
    # Delete Keyboard
    bot.edit_message_reply_markup(callback.message.chat.id,
                                  callback.message.message_id,
                                  reply_markup=None)

    if callback.data == audio_speed_func:
        user_input_waiter.add_user_input_waiter(callback.message.chat.id, callback.data)
        text = """Enter speed ratio. It must be float from 0 to 3 (excludes 0).
Passing 1 does not change audio speed.
(format: [digits].[digits])"""
        return bot.edit_message_text(
                   text,
                   callback.message.chat.id,
                   callback.message.message_id
               )

    if callback.data == audio_pitch_func:
        user_input_waiter.add_user_input_waiter(callback.message.chat.id, callback.data)
        text = """Enter pitch ratio. It must be float from 0 to 3 (excludes 0).
Passing 1 does not change audio pitch.
(format: [digits].[digits])"""
        return bot.edit_message_text(
            text,
            callback.message.chat.id,
            callback.message.message_id
        )

    if callback.data == audio_reverb_func:
        user_input_waiter.add_user_input_waiter(callback.message.chat.id, callback.data)
        text = """Enter reverb ratio. It must be integer from 0 to 100 (in percents).
Passing 0 does not change audio.
(format: [digits])"""
        return bot.edit_message_text(
            text,
            callback.message.chat.id,
            callback.message.message_id
        )

    if callback.data == audio_bass_boost_func:
        user_input_waiter.add_user_input_waiter(callback.message.chat.id, callback.data)
        text = """Enter gain ratio. It must be integer from 0 to 25.
Passing 0 does not change audio.
(format: [digits])"""
        return bot.edit_message_text(
            text,
            callback.message.chat.id,
            callback.message.message_id
        )

    if callback.data == end_selecting_audio_func:
        bot.edit_message_text(
            "Okay! Processing your file...",
            callback.message.chat.id,
            callback.message.message_id
        )
        file_full_name = users_functions_dict.apply_user_audio_funcs(callback.message.chat.id)
        file_stream = open(rf"./processed/{file_full_name}", "rb")
        bot.edit_message_text(
            "That's it! Enjoy your music!",
            callback.message.chat.id,
            callback.message.message_id
        )
        bot.send_audio(
            callback.message.chat.id,
            audio=file_stream
        )
        file_stream.close()
        os.remove(rf".\input_audios\{file_full_name}")
        os.remove(rf".\processed\{file_full_name}")
        return

    # Edit message for chosen function
    bot.edit_message_text(
        'You have chosen ' + audio_sources[callback.data],
        callback.message.chat.id,
        callback.message.message_id
    )


# Handler for video function selection via inline keyboard
def callback_video_func_handler(bot: TeleBot, callback):
    # Delete Keyboard
    bot.edit_message_reply_markup(callback.message.chat.id,
                                  callback.message.message_id,
                                  reply_markup=None)

    users_functions_dict.add_user_video_func(callback.message.chat.id, callback.data)

    if (callback.data == video_loop_on_music_func) or (callback.data == video_overlap_with_music):
        user_input_waiter.add_user_input_waiter(callback.message.chat.id, audio_source_for_video)
        text = "Okay! Now send me audio file or youtube link..."
        return bot.edit_message_text(
            text,
            callback.message.chat.id,
            callback.message.message_id
        )
