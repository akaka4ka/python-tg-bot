import os
import urllib.request

from dotenv import load_dotenv

from src.KeyboardLayouts.InlineKeyboards.AudioFuncsKeyboard import audio_funcs_keyboard
from src.KeyboardLayouts.InlineKeyboards.AudioSourceKeyboard import audio_source_from_file
from src.KeyboardLayouts.InlineKeyboards.VideoFuncsKeyboard import video_funcs_keyboard
from src.KeyboardLayouts.InlineKeyboards.VideoSourceKeyboard import video_source_from_file
from src.classes.UserInputWaiter import user_input_waiter
from src.classes.UsersFunctionsDict import users_functions_dict

load_dotenv()

token = os.environ.get("BOT_TOKEN")

"""
    Class for downloading/uploading user files
"""


class UserFilesDownloader:
    def __init__(self, bot, user_id, message_id):
        self.bot = bot
        self.user_id = user_id
        self.message_id = message_id
        self.download_type = None

    # Download audio file
    def download_user_audio_file(self, file_path, file_format, callback=None):
        self.download_type = 'audio'
        download_callback = callback if callback is not None else self.user_file_downloader_callback
        urllib.request.urlretrieve(
            rf'https://api.telegram.org/file/bot{token}/{file_path}',
            rf'.\input_audios\{self.user_id}.{file_format}',
            reporthook=download_callback
        )
        if len(users_functions_dict.video_funcs_dict.keys()) > 0:
            users_functions_dict.video_funcs_dict.pop(self.user_id)
            os.remove(rf".\input_audios\{self.user_id}.{file_format}")

    # Download video file
    def download_user_video_file(self, file_path, file_format, callback=None):
        self.download_type = 'video'
        download_callback = callback if callback is not None else self.user_file_downloader_callback
        urllib.request.urlretrieve(
            rf'https://api.telegram.org/file/bot{token}/{file_path}',
            rf'input_videos\{self.user_id}.{file_format}',
            reporthook=download_callback
        )

    # Download user file
    def download_user_file(self, file_path, file_format):
        urllib.request.urlretrieve(
            rf'https://api.telegram.org/file/bot{token}/{file_path}',
            rf'tmp{self.user_id}.{file_format}'
        )

    # User file downloader callback
    # It passed to urlretrieve
    def user_file_downloader_callback(self, current_blocks, block_size, file_size):
        if current_blocks * block_size >= file_size:
            markup = None
            if self.download_type == 'audio':
                markup = audio_funcs_keyboard()
                markup.keyboard.pop()
                user_input_waiter.end_waiting_for_user_input(self.user_id, audio_source_from_file)
            else:
                markup = video_funcs_keyboard()
                user_input_waiter.end_waiting_for_user_input(self.user_id, video_source_from_file)

            self.bot.edit_message_text(
                "File downloaded. Choose function you want to execute",
                self.user_id,
                self.message_id,
                reply_markup=markup
            )
            user_files_downloaders.__delitem__(self.user_id)


# Dictionary for downloaders
# "user_id": "downloader"
user_files_downloaders = {}
