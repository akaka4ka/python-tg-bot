import glob
import os
import time

from telebot import TeleBot

from src.BotHandlers.CallbackHandlers import audio_source_for_video
from src.KeyboardLayouts.InlineKeyboards.AudioSourceKeyboard import audio_source_from_file
from src.KeyboardLayouts.InlineKeyboards.VideoFuncsKeyboard import video_loop_on_music_func
from src.classes.UserInputWaiter import user_input_waiter
from src.classes.UsersFunctionsDict import users_functions_dict
from src.classes.VideoEditor import VideoEditor
from src.classes.YouTubeLoader import YouTubeLoader, user_youtube_downloaders
from src.utils.UserFilesLoader import user_files_downloaders, UserFilesDownloader


# Handler for audio file message
def audio_file_handler(bot: TeleBot, message):
    index_before_format = 0
    try:
        index_before_format = message.audio.file_name.rindex('.')
    except ValueError:
        bot.send_message(message.chat.id, "Sorry, I can't recognize file format, try another file with correct format")
        return

    new_message = bot.send_message(message.chat.id, "Got it! Downloading your file...")
    downloader = UserFilesDownloader(bot, message.chat.id, new_message.id)
    user_files_downloaders[message.chat.id] = downloader
    downloader.download_user_audio_file(
        bot.get_file(message.audio.file_id).file_path,
        message.audio.file_name[index_before_format + 1:]
    )


# Handler for YouTube link message
def youtube_link_audio_handler(bot: TeleBot, message):
    if (r"youtube.com" not in message.text) and (r"youtu.be" not in message.text):
        return bot.send_message(
            message.chat.id,
            "This is not valid YouTube link"
        )

    new_message = bot.send_message(message.chat.id, "Got it! Downloading your file...")
    downloader = YouTubeLoader(bot, message.chat.id, new_message.message_id, 'audio', message.text)
    user_youtube_downloaders[message.chat.id] = downloader
    downloader.load_user_file()


# Handler for audio file message
def audio_file_for_video_handler(bot: TeleBot, message):
    index_before_format = 0
    try:
        index_before_format = message.audio.file_name.rindex('.')
    except ValueError:
        bot.send_message(message.chat.id, "Sorry, I can't recognize file format, try another file with correct format")
        return

    new_message = bot.send_message(message.chat.id, "Got it! Downloading your file...")
    downloader = UserFilesDownloader(bot, message.chat.id, new_message.id)
    user_files_downloaders[message.chat.id] = downloader
    downloader.download_user_audio_file(
        bot.get_file(message.audio.file_id).file_path,
        message.audio.file_name[index_before_format + 1:],
        lambda current_blocks, block_size, file_size: _audio_file_download_handler(
            current_blocks,
            block_size,
            file_size,
            bot,
            message.chat.id,
            new_message.message_id
        )
    )


def _audio_file_download_handler(current_blocks, block_size, file_size, bot, user_id, message_id):
    if current_blocks * block_size >= file_size:
        user_input_waiter.end_waiting_for_user_input(user_id, audio_source_for_video)
        user_files_downloaders.__delitem__(user_id)
        audio_file_path = glob.glob(rf".\input_audios\{user_id}.*")[0]
        bot.edit_message_text(
            "File downloaded. Processing...",
            user_id,
            message_id,
            reply_markup=None
        )
        audio_format = audio_file_path[audio_file_path.rindex('.') + 1:]
        video_file_path = glob.glob(rf".\input_videos\{user_id}.*")[0]
        video_format = video_file_path[video_file_path.rindex('.') + 1:]
        video_editor = VideoEditor(video_format, audio_format, user_id)

        if next(iter(users_functions_dict.video_funcs_dict.values())) == video_loop_on_music_func:
            video_editor.merge_audio_and_looped_video()
        else:
            video_editor.overlap_audio_and_video()

        output_file_path = glob.glob(rf".\processed\{user_id}.*")[0]
        bot.edit_message_text(
            "That's it! Have fun!",
            user_id,
            message_id,
            reply_markup=None
        )
        video = open(output_file_path, "rb")
        bot.send_video(user_id, video=video)
        video.close()
        os.remove(output_file_path)
        os.remove(video_file_path)
        users_functions_dict.video_funcs_dict.pop(user_id)
        user_input_waiter.usersInputWaiter.pop(user_id)


# Handler for YouTube link message
def youtube_link_audio_for_video_handler(bot: TeleBot, message):
    if (r"youtube.com" not in message.text) and (r"youtu.be" not in message.text):
        return bot.send_message(
            message.chat.id,
            "This is not valid YouTube link"
        )

    new_message = bot.send_message(message.chat.id, "Got it! Downloading your file...")
    downloader = YouTubeLoader(
        bot,
        message.chat.id,
        new_message.message_id,
        'audio',
        message.text,
        lambda download_obj: _finish_loading_hook(
            download_obj,
            bot,
            message.chat.id,
            new_message.message_id
        )
    )
    user_youtube_downloaders[message.chat.id] = downloader
    downloader.load_user_file()


def _finish_loading_hook(download_obj, bot, user_id, message_id):
    if download_obj['status'] == 'finished':
        bot.edit_message_text(
            "File downloaded. Processing...",
            user_id,
            message_id,
            reply_markup=None
        )
        user_youtube_downloaders.__delitem__(user_id)
        user_input_waiter.end_waiting_for_user_input(user_id, audio_source_for_video)
        audio_file_path = glob.glob(rf".\input_audios\{user_id}.*")[0]
        audio_format = audio_file_path[audio_file_path.rindex('.') + 1:]
        video_file_path = glob.glob(rf".\input_videos\{user_id}.*")[0]
        video_format = video_file_path[video_file_path.rindex('.') + 1:]
        video_editor = VideoEditor(video_format, audio_format, user_id)
        if next(iter(users_functions_dict.video_funcs_dict.values())) == video_loop_on_music_func:
            video_editor.merge_audio_and_looped_video()
        else:
            video_editor.overlap_audio_and_video()

        output_file_path = glob.glob(rf".\processed\{user_id}.*")[0]
        bot.edit_message_text(
            "That's it! Have fun!",
            user_id,
            message_id,
            reply_markup=None
        )
        video = open(output_file_path, "rb")
        bot.send_video(user_id, video=video)
        video.close()
        os.remove(output_file_path)
        os.remove(audio_file_path)
        os.remove(video_file_path)
        users_functions_dict.video_funcs_dict.pop(user_id)
        user_input_waiter.usersInputWaiter.pop(user_id)


# Handler for audio file message
def video_file_handler(bot: TeleBot, message):
    index_before_format = 0
    try:
        index_before_format = message.video.file_name.rindex('.')
    except ValueError:
        bot.send_message(message.chat.id, "Sorry, I can't recognize file format, try another file with correct format")
        return

    new_message = bot.send_message(message.chat.id, "Got it! Downloading your file...")
    downloader = UserFilesDownloader(bot, message.chat.id, new_message.id)
    user_files_downloaders[message.chat.id] = downloader
    downloader.download_user_video_file(
        bot.get_file(message.video.file_id).file_path,
        message.video.file_name[index_before_format + 1:]
    )


# Handler for YouTube link message
def youtube_link_video_handler(bot: TeleBot, message):
    if (r"youtube.com" not in message.text) and (r"youtu.be" not in message.text):
        return bot.send_message(
            message.chat.id,
            "This is not valid YouTube link"
        )

    new_message = bot.send_message(message.chat.id, "Got it! Downloading your file...")
    downloader = YouTubeLoader(bot, message.chat.id, new_message.message_id, 'video', message.text)
    user_youtube_downloaders[message.chat.id] = downloader
    downloader.load_user_file()
