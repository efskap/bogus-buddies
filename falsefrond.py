from scipy import spatial
import signal
import os
import sys
from typing import List, Union

# Whether or not to use the filtered word list for faster computation at the expense of comprehensiveness.
filtered = True
useRAM = True
if filtered:
    target_vec_file = "./wiki.no.align_filtered.vec"
    source_vec_file = "./wiki.sv.align_filtered.vec"
else:
    target_vec_file = "./wiki.no.align.vec"
    source_vec_file = "./wiki.sv.align.vec"

# When loading into RAM, maps a common_word to its original form and the vector.
source_vec_map = {}
target_vec_map = {}

def load_into_map(filepath, vecmap, max=0):
    print("Loading " + filepath + " into RAM", file=sys.stderr)
    file_size = os.path.getsize(filepath)
    with open(filepath, 'r') as fp:
        line = True
        while line:
            line = fp.readline()
            pos = fp.tell()
            if pos % 1024*1024 < 5:
                print(f'{pos/file_size*100:.2f}%\r', end='', file=sys.stderr)
            if max > 0 and pos > max:
                return
            try:
                word, vec = parse_vec_line(line)
            except ValueError as e:
                print("Could not parse:", file=sys.stderr)
                print(line, file=sys.stderr)
                print(e, file=sys.stderr)
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
    '''
    Parses a line of a .vec file into the word and its vector.
    '''
    split = line.split()
    vector = split[-300:]
    word = " ".join(split[:len(split)-300])
    parsed_vector = [float(x) for x in vector]
    return word, parsed_vector

def apply_transformations(source: str) -> str:
    '''
    Transform a Swedish or Norwegian word into a "common form".
    '''
    source = source.replace('ck', 'kk')
    source = source.replace('x',  'ks')
    source = source.replace('æ',  'ä')
    source = source.replace('ø',  'ö')
    return source

def cos_similarity(vec1, vec2):
    return 1 - spatial.distance.cosine(vec1, vec2)

def check(common_word, src_word, src_vec):
        # print(f"Looking for {src_word} -> {common_word} in {target_vec_file}")
        if useRAM:
            tar_data = target_vec_map.get(common_word)
        else:
            tar_data = find_word_in_vec_file(common_word, target_vec_file, transform=True)
        if tar_data is None:
            # print(f'no match for: {common_word} <- {src_word}', file=sys.stderr)
            return
        tar_word, tar_vec = tar_data
        if not src_vec or not tar_vec:
            return
        score = 1 - cos_similarity(src_vec, tar_vec)
        print(f'{score:.0%}\t{src_word}\t{common_word}\t{tar_word}')

header = "score\tsv\tcom\tno"
def main():
    if len(sys.argv) > 1:
        words = sys.argv[1:]
        vecSrc = (find_word_in_vec_file(word, source_vec_file) for word in words)
        dataSrc = ((apply_transformations(word), (word, vec)) for word, vec in vecSrc)
    else:
        if useRAM:
            load_into_map(target_vec_file, target_vec_map)#, max = 1024*1024*5)
            load_into_map(source_vec_file, source_vec_map)#, max = 1024*1024*5)
            dataSrc = source_vec_map.items()
        else:
            print("iterating " + source_vec_file, file=sys.stderr)
            fp = open(source_vec_file, 'r')
            next(fp)
            vecSrc = (parse_vec_line(line) for line in fp)
            dataSrc = ((apply_transformations(word), (word, vec)) for word, vec in vecSrc)
    print(header)
    for data in dataSrc:
        common_word, innerData = data
        src_word, src_vec = innerData
        check(common_word, src_word, src_vec)
        sys.stdout.flush()
        sys.stderr.flush()

if __name__ == "__main__":
    # don't print exception on ctrl-c or when pipe closes, just quit
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
