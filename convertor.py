import os
import pickle
from typing import List
from tqdm import tqdm
import numpy as np
from seq.converter import Converter
from seq.smart_multi_track import SmartMultiTrack
from seq.track import SmartTrack

data_root = os.path.join(os.getcwd(), 'single_track_midi')


def save_as_pickled_object(obj, filepath):
    """
    This is a defensive way to write pickle.write, allowing for very large files on all platforms
    """
    max_bytes = 2**31 - 1
    bytes_out = pickle.dumps(obj)
    n_bytes = sys.getsizeof(bytes_out)
    with open(filepath, 'wb') as f_out:
        for idx in range(0, n_bytes, max_bytes):
            f_out.write(bytes_out[idx:idx+max_bytes])


def try_to_load_as_pickled_object_or_None(filepath):
    """
    This is a defensive way to write pickle.load, allowing for very large files on all platforms
    """
    max_bytes = 2**31 - 1
    try:
        input_size = os.path.getsize(filepath)
        bytes_in = bytearray(0)
        with open(filepath, 'rb') as f_in:
            for _ in range(0, input_size, max_bytes):
                bytes_in += f_in.read(max_bytes)
        obj = pickle.loads(bytes_in)
    except:
        return None
    return obj


piano_roll_list = [None] * 1000000
c = 0
time_sig = (4, 4)
atom = 24
n_bars = 2

for file_name in os.listdir(data_root):

    try:

        if c == 50000:
            save_as_pickled_object(piano_roll_list[:50000], 'data/piano_roll_50k.pkl')

        if c == 100000:
            save_as_pickled_object(piano_roll_list[:100000], 'data/piano_roll_100k.pkl')


        if c == 200000:
            save_as_pickled_object(piano_roll_list, 'data/piano_roll_200k.pkl')
            break

        st = SmartMultiTrack.read(name=file_name,
                                  file_name=os.path.join(data_root, file_name),
                                  atomic_size_in_beats=0,
                                  residual_ratio=0)

        if st.time_sig == time_sig:
            st.pad_to_next_bar()
            bar_len = st.beats_to_ticks(4)
            bars = st.split_every(step=bar_len * n_bars,
                                  start=0 * bar_len,
                                  end=int(st.ticks_to_beats(st.duration) / st.time_sig[1]) * bar_len)
            for bar in bars:
                for track_idx in range(len(bar.smart_tracks)):
                    pr_matrix = Converter.as_boolean_matrix(bar.track(track_idx), n_steps=atom*n_bars)
                    if pr_matrix.sum() > atom * n_bars // 2:
                        piano_roll_list[c] = pr_matrix
                        c += 1

    except (KeyError, ValueError, TypeError, RuntimeError, AttributeError, Warning, AssertionError):
        continue


print(f'{c} files converted.')