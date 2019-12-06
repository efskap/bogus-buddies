import os
from typing import Dict

sv_list = "./sv_full.txt"
no_list = "./no_full.txt"

sv_map = {}
no_map = {}

def fill_map(filepath, dest_map):
    with open(filepath, 'r') as fp:
        for line in fp:
            word, freq = line.split()
            dest_map[word] = int(freq)


def fix(this_map, other_map, out_file):
    with open(out_file, 'w') as out_file:
        for word, freq in this_map.items():
            other_freq = other_map.get(word)
            if not other_freq or freq >= other_freq:
                out_file.write(f'{word} {freq}\n')
            else:
                print("bad ->" ,word, ":", freq, "vs", other_freq)

def fix2(this_map, char_set, out_file):
    with open(out_file, 'w') as out_file:
        for word, freq in this_map.items():
            if not any(x in word for x in char_set):
                out_file.write(f'{word} {freq}\n')
            else:
                print("bad ->", word)


fill_map(sv_list, sv_map)
fill_map(no_list, no_map)

fix2(no_map, "öä", "./no_fixed2.txt")
fix2(sv_map, "øæ", "./sv_fixed2.txt")

# fix(no_map, sv_map, "./no_fixed.txt")
# fix(sv_map, no_map, "./sv_fixed.txt")
