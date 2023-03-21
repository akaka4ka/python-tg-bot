from __future__ import unicode_literals
import youtube_dl
from telebot import TeleBot

from src.KeyboardLayouts.InlineKeyboards.AudioFuncsKeyboard import audio_funcs_keyboard
from src.KeyboardLayouts.InlineKeyboards.AudioSourceKeyboard import audio_source_from_youtube
from src.KeyboardLayouts.InlineKeyboards.VideoFuncsKeyboard import video_funcs_keyboard
from src.KeyboardLayouts.InlineKeyboards.VideoSourceKeyboard import video_source_from_youtube
from src.classes.UserInputWaiter import user_input_waiter

"""
    This class is for loading audio and video from youtube by handling url link
"""


class YouTubeLoader:
    def __init__(self, bot: TeleBot, user_id, message_id, download_type, url, callback=None):
        self.bot = bot
        self.user_id = user_id
        self.message_id = message_id
        self.url = url
        self.options = {
            'format': 'bestaudio' if download_type == 'audio' else 'bestvideo',
            'outtmpl': (rf'.\input_audios\{self.user_id}.mp3'
                        if download_type == 'audio' else
                        rf'.\input_videos\{self.user_id}.mp4'),
            'noplaylist': True,
            'progress_hooks': [callback if callback is not None else self.finish_loading_hook],
        }

    def load_user_file(self):
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.extract_info(self.url)

    def finish_loading_hook(self, download_obj):
        if download_obj['status'] == 'finished':
            markup = None
            if user_input_waiter.is_waiting_for_input(self.user_id, audio_source_from_youtube):
                markup = audio_funcs_keyboard()
                markup.keyboard.pop()
                user_input_waiter.end_waiting_for_user_input(self.user_id, audio_source_from_youtube)
            else:
                markup = video_funcs_keyboard()
                user_input_waiter.end_waiting_for_user_input(self.user_id, video_source_from_youtube)

            self.bot.edit_message_text(
                "File downloaded. Choose function you want to execute",
                self.user_id,
                self.message_id,
                reply_markup=markup
            )
            user_youtube_downloaders.__delitem__(self.user_id)


# Dictionary for YouTube downloaders
# "user_id": "downloader"
user_youtube_downloaders = {}
