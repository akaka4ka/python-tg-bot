"""
    Class for tracking what bot awaits from user.
    For example, user choices Work with audio -> Load as audio file
    Then bot will ignore other messages from that user until they upload audio file
"""
from src.KeyboardLayouts.InlineKeyboards.AudioSourceKeyboard import audio_source_from_file


class UserInputWaiter:
    def __init__(self):
        """
            Dictionary for users inputs: "user id": "[awaited sources]"
        """
        self.usersInputWaiter = {}

    def is_waiting_for_input(self, user_id, input_type):
        return self.usersInputWaiter.get(user_id).__contains__(input_type)

    def add_user_input_waiter(self, user_id, input_type):
        if self.is_wait_for_user_input(user_id):
            if not self.usersInputWaiter[user_id].__contains__(input_type):
                self.usersInputWaiter[user_id].append(input_type)
        else:
            self.usersInputWaiter[user_id] = [input_type]

    def is_wait_for_user_input(self, user_id):
        return self.usersInputWaiter.__contains__(user_id)

    def end_waiting_for_user_input(self, user_id, input_type):
        if self.is_wait_for_user_input(user_id):
            if self.usersInputWaiter[user_id].__contains__(input_type):
                self.usersInputWaiter[user_id].remove(input_type)


user_input_waiter = UserInputWaiter()
