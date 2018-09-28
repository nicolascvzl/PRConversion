import pretty_midi
import matplotlib.pyplot as plt
from copy import deepcopy
import os
from tqdm import tqdm

src_dir = "data"
SRC_PATH = os.path.join(os.getcwd(), src_dir)
dest_dir = "single_track_midi"
DEST_PATH = os.path.join(os.getcwd(), dest_dir)
c = 0

def track_extraction(file_name):
    try:
        midi_data = pretty_midi.PrettyMIDI(os.path.join(SRC_PATH, file_name))
        if len(midi_data.time_signature_changes) == 1 and midi_data.time_signature_changes[0].denominator == 4 and midi_data.time_signature_changes[0].numerator == 4:
            for i, instrument in enumerate(midi_data.instruments):
                if not instrument.is_drum:
                    tmp_midi = deepcopy(midi_data)
                    tmp_midi.instruments = [tmp_midi.instruments[i]]
                    tmp_midi.write(os.path.join(DEST_PATH, file_name.split(".mid")[0] + "_" + str(i) + ".mid"))
            return True
    except (OSError, KeyError, ValueError, TypeError, RuntimeError, AttributeError, Warning, AssertionError, EOFError):
        print(f'Problem found while converting {file_name}')
        return False

def extract_all_midi():
    c = 0
    list_of_names = list(os.listdir(SRC_PATH))[:]
    for file_name in tqdm(list_of_names):
        if track_extraction(file_name):
            c+= 1
    return c

print(f'{extract_all_midi()} files have been converted!')