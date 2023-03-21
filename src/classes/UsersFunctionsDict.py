import glob

from src.KeyboardLayouts.InlineKeyboards.AudioFuncsKeyboard import audio_speed_func, audio_pitch_func, \
    audio_reverb_func, audio_bass_boost_func
from src.classes.AudioEditor import AudioEditor
from src.classes.UserInputWaiter import user_input_waiter


class UsersFunctionsDict:
    def __init__(self):
        self.audio_funcs_dict = {}
        self.video_funcs_dict = {}

    def add_user_audio_func(self, user_id, func, ratio):
        if self.audio_funcs_dict.keys().__contains__(user_id):
            self.audio_funcs_dict[user_id].append({func: ratio})
        else:
            self.audio_funcs_dict[user_id] = [{func: ratio}]

    def add_user_video_func(self, user_id, func):
        if not self.video_funcs_dict.keys().__contains__(user_id):
            self.video_funcs_dict[user_id] = func

    def apply_user_audio_funcs(self, user_id):
        if not self.audio_funcs_dict.keys().__contains__(user_id):
            return

        funcs = self.audio_funcs_dict[user_id]
        file_path = glob.glob(rf".\input_audios\{user_id}.*")[0]
        file_name = file_path[file_path.rindex('\\') + 1:file_path.rindex('.')]
        file_format = file_path[file_path.rindex('.') + 1:]
        audio_editor = AudioEditor(f'{file_name}.{file_format}')
        for func in funcs:
            func_name = next(iter(func))

            if func_name == audio_speed_func:
                audio_editor.change_speed(func[func_name])

            if func_name == audio_pitch_func:
                audio_editor.change_pitch(func[func_name])

            if func_name == audio_reverb_func:
                audio_editor.reverb(func[func_name] / 10)

            if func_name == audio_bass_boost_func:
                audio_editor.bass_boost(gain=func[func_name])

        audio_editor.save(file_name, file_format)
        self.audio_funcs_dict.pop(user_id)
        user_input_waiter.usersInputWaiter.pop(user_id)
        return f'{file_name}.{file_format}'


users_functions_dict = UsersFunctionsDict()
