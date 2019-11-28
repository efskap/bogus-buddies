from scipy import spatial
import signal
import os
import sys
from typing import List, Union

target_vec_file = "./wiki.no.align.vec"
source_vec_file = "./wiki.sv.align.vec"


source_vec_map = {}
target_vec_map = {}

def load_into_map(filepath, vecmap):
    print("Loading " + filepath + " into RAM")
    file_size = os.path.getsize(filepath)
    with open(filepath, 'r') as fp:
        line = True
        while line:
            line = fp.readline()
            pos = fp.tell()
            if pos % 1024*1024 < 5:
                print(f'{pos/file_size*100:.2f}%\r', end='')
            try:
                word, vec = parse_vec_line(line)
            except ValueError as e:
                print("Could not parse:")
                print(line)
                print(e)
                continue
            vecmap[apply_transformations(word)] = word, vec


def find_word_in_vec_file(word: str, filepath: str, transform=False):
    with open(filepath, 'r') as fp:
        next(fp)
        for line in fp:
            w = line.split()[0]
            if transform:
                w = apply_transformations(w)
            if w == word:
                return parse_vec_line(line)
    print(f'could not find {word} in {filepath}', file=sys.stderr)

def parse_vec_line(line: str) -> Union[str, List[float]]:
    split = line.split()
    vector = split[-300:]
    word = " ".join(split[:len(split)-300])
    parsed_vector = [float(x) for x in vector]
    return word, parsed_vector

def apply_transformations(source: str) -> str:
    source = source.replace('ck', 'kk')
    source = source.replace('x',  'ks')
    source = source.replace('æ',  'ä')
    source = source.replace('ø',  'ö')
    # ...
    return source

def cos_similarity(vec1, vec2):
    return 1 - spatial.distance.cosine(vec1, vec2)

def check(src_word, src_vec):
        common_word = apply_transformations(src_word)
        # print(f"Looking for {src_word} -> {common_word} in {target_vec_file}")
        tar_data = find_word_in_vec_file(common_word, target_vec_file, transform=True)
        # tar_data = target_vec_map.get(common_word)
        if tar_data is None:
            print(f'no match for: {common_word} <- {src_word}', file=sys.stderr)
            return
        tar_word, tar_vec = tar_data
        sim = cos_similarity(src_vec, tar_vec)
        print(f'{sim:.0%}\t{src_word}\t{common_word}\t{tar_word}')
header = "sim\tsrcWord\tcommonWord\ttarWord"
def main():
    # load_into_map(target_vec_file, source_vec_map)
    if len(sys.argv) > 1:
        print(header)
        for word in sys.argv[1:]:
            data = find_word_in_vec_file(word, source_vec_file)
            if not data:
                return
            src_word, src_vec = data
            check(src_word, src_vec)
        return
    print("iterating " + source_vec_file, file=sys.stderr)
    with open(source_vec_file, 'r') as fp:
        next(fp)
        print(header)
        for line in fp:
            src_word, src_vec = parse_vec_line(line)
            check(src_word, src_vec)
            sys.stdout.flush()
            sys.stderr.flush()

if __name__ == "__main__":
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
