import sys

sv_list = "./sv_fixed2.txt"
no_list = "./no_fixed2.txt"

sv_map = {}
no_map = {}

def fill_map(filepath, dest_map):
    with open(filepath, 'r') as fp:
        for line in fp:
            word = line.split()[0]
            dest_map[word] = True

def filter_by(vec_path, filter_map):
    with open(vec_path, 'r') as fp:
        with open(vec_path.replace(".vec", "_filtered.vec"), 'w') as outfp:
            for line in fp:
                if line.split()[0] in filter_map:
                    outfp.write(line + "\n")

fill_map(sv_list, sv_map)
fill_map(no_list, no_map)

filter_by("wiki.no.align.vec", no_map)
filter_by("wiki.sv.align.vec", sv_map)
