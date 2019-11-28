# Installation

- You need python 3, probably > 3.5

- Install scipy, probably with `pip install scipy`.

- Download norwegian and swedish vectors from https://fasttext.cc/docs/en/aligned-vectors.html and put them in the same folder

# Usage

`python3 falsefrond.py`  
Scan through swedish vector list and report all common words (takes a long time)

`python3 falsefrond.py barn lov`  
Print the score for the words `barn` and `lov` (you can specify  as many words as you want)
