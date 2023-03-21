import functools

import ffmpeg

"""
    Class for editing audio. Takes path to audio, applies filters and output new edited audio file.
"""

# IR_church = 'IR.wav'
# IR_hall_1 = 's1r2_0_1.mp3'
# IR_hall_2 = 'ir_row_1l_sl_centre.wav'
# IR_church = 'church.mp3'
# IR_mausoleum = 'mausoleum.wav'
IR_studio = 'studio_1.wav'


class AudioEditor:
    def __init__(self, file_name):
        self.path = rf'.\input_audios\{file_name}'
        self.stream = ffmpeg.input(self.path)

    def change_speed(self, coefficient):
        self.stream = self.stream.filter('asetrate', int(self.get_audio_frequency() * coefficient))
        return self

    def reverb(self, wet=2):
        impulse_response = ffmpeg.input(rf'.\impulse_responses\{IR_studio}')
        self.stream = ffmpeg.filter([self.stream, impulse_response], 'afir', dry=10-wet, wet=wet)
        return self

    def bass_boost(self, gain=15, frequency=100):
        self.stream = self.stream.filter('bass', gain=gain, frequency=frequency)
        return self

    def change_pitch(self, pitch_scale):
        self.stream = self.stream.filter('rubberband', pitch=pitch_scale)
        return self

    # should async?
    def save(self, output_file_name, audio_format='mp3'):
        self.stream.output(rf'.\processed\{output_file_name}.{audio_format}').global_args('-y').run()

    # private methods
    def get_audio_frequency(self):
        return int(ffmpeg.probe(self.path)['streams'][0].get('sample_rate'))


# n = int(input())
# input_arr = [int(x) for x in str(input()).split()]
# employees = {}
# while len(input_arr) == 2:
#     if not employees.keys().__contains__(input_arr[0]):
#         employees[input_arr[0]] = {}
#         employees[input_arr[0]]['children'] = []
#     employees[input_arr[0]]['children'].append(input_arr[1])
#     input_arr = [int(x) for x in str(input()).split()]
#
# for i in range(1, n + 1):
#     if not employees.keys().__contains__(i):
#         employees[i] = {}
#         employees[i]['children'] = []
#     employees[i]['opinion'] = input_arr[i - 1]
#
# fire = 0
#
#
# def reduce_function(value, child_id, main_opinion, diff_children):
#     if employees[child_id]['opinion'] != main_opinion:
#         value += 1
#         diff_children.append(child_id)
#
#     return value
#
#
# def check_if_no_diff(element):
#     if len(employees[element]['children']) == 0:
#         return True
#
#     diff_children = []
#     diff = functools.reduce(
#         lambda val, el: reduce_function(val, el, root['opinion'], diff_children),
#         root['children'],
#         0
#     )
#
#     if diff > 0:
#         return False
#
#     for child in employees[element]['children']:
#         if not check_if_no_diff(child):
#             return False
#
#     return True
#
#
# def foo():
#     for i in range(n):
#         root = employees[i + 1]
#         diff_children = []
#         diff = functools.reduce(
#             lambda val, el: reduce_function(val, el, root['opinion'], diff_children),
#             root['children'],
#             0
#         )
#
#         if diff == 0:
#
#
#         if diff == 1:
#             fire = diff_children[0]
#
#         if diff > 1:
#             for child in root['children']:
#                 if not check_if_no_diff(child):
#                     print("NO")
#                     return
#
#             print("YES")
#             print(i + 1)
#             return
#
#
# foo()

def check_if_disagree(master, slaves, opinions):
    current_disagreement = 0
    for i in slaves:
        if opinions[master - 1] != opinions[i - 1]:
            if current_disagreement:
                return -1
            else:
                current_disagreement = i
    if current_disagreement:
        return current_disagreement
    else:
        return 0


def solve():
    n = int(input())
    master_slaves = {}
    for _ in range(n - 1):
        master, slave = map(int, input().split())
        if master in master_slaves:
            master_slaves[master].append(slave)
        else:
            master_slaves[master] = [slave]
    opinions = list(map(int, input().split()))
    if sum(opinions) == len(opinions) or sum(opinions) == 0:
        print('YES')
        print(len(opinions))
        return

    ans = 0

    for master, slaves in master_slaves.items():
        if ans != master:
            d_slave = check_if_disagree(master, slaves, opinions)
            if d_slave and not ans:
                if d_slave == -1:
                    ans = master
                else:
                    if d_slave in master_slaves and check_if_disagree(d_slave, master_slaves[d_slave], opinions) > 0:
                        ans = d_slave
                    else:
                        ans = max(master, d_slave)
            elif d_slave:
                print('NO')
                return

    print('YES')
    print(ans)


solve()
