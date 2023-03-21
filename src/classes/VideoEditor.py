import os
import time

import ffmpeg

"""
    Class for editing video
"""


class VideoEditor:
    def __init__(self, video_format, audio_format, user_id):
        self.output_format = video_format
        self.video_path = rf'.\input_videos\{user_id}.{video_format}'
        self.audio_path = rf'.\input_audios\{user_id}.{audio_format}'
        self.user_id = user_id

    def merge_audio_and_looped_video(self):
        command = rf'ffmpeg -stream_loop -1 -i {self.video_path} -i {self.audio_path} ' \
                  rf'-map 0:v:0 -map 1:a:0 -shortest .\processed\{self.user_id}.{self.output_format}'
        os.system(command)

        while not os.path.exists(rf'.\processed\{self.user_id}.{self.output_format}'):
            time.sleep(0.5)

    def overlap_audio_and_video(self):
        command = rf'ffmpeg -i {self.video_path} -i {self.audio_path} -map 0:v -map 1:a ' \
                  rf'-y .\processed\{self.user_id}.{self.output_format}'

        # ffmpeg.concat(
        #     ffmpeg.input(rf'{self.video_path}'),
        #     ffmpeg.input(rf'{self.audio_path}'),
        #     v=1,
        #     a=1
        # ).output(rf'.\processed\{self.user_id}.{self.output_format}').run()
        #
        # time.sleep(1)

        os.system(command)

        while not os.path.exists(rf'.\processed\{self.user_id}.{self.output_format}'):
            time.sleep(0.5)
