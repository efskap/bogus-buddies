# Installation

- You need python 3, probably > 3.5

- Install scipy, probably with `pip install scipy`.

- Download norwegian and swedish vectors from https://fasttext.cc/docs/en/aligned-vectors.html and put them in the same folder

- The command to filter each .vec file based on a frequency list is `grep -Fwf <(cut no_50k.txt -f 1 -d ' ') wiki.no.align.vec > no_filtered.vec`

- We tried frequency lists from [here](https://github.com/hermitdave/FrequencyWords/tree/master/content/2018/)

# Usage

`python3 falsefrond.py`  
Scan through swedish vector list and report all common words (takes a long time)

`python3 falsefrond.py barn lov`  
Print the score for the words `barn` and `lov` (you can specify  as many words as you want)

(linux / macos only, as it uses unix pipes):  
`python3 falsefrond.py | head -n 50 | sort -nr`  
Process first 50 matches, and sort them by similarity

## Example output:


```
λ › python3 falsefrond.py barn barnet barns barnets man sjö åt samlag skede | sort -n                    ~/LDA_project master
score   srcWord commonWord      tarWord
27%     barn    barn    barn
29%     barnets barnets barnets
31%     man     man     man
33%     barnet  barnet  barnet
33%     barns   barns   barns
72%     sjö     sjö     sjø
82%     samlag  samlag  samlag
84%     åt      åt      åt
87%     skede   skede   skede
```


With `filtered = True` in the source code:
```
λ › python3 falsefrond.py 2>/dev/null | head -n 50 | sort -n
score   srcWord commonWord      tarWord
19%     han     han     han
23%     var     var     var
31%     har     har     har
38%     de      de      de
41%     provinsen       provinsen       provinsen
42%     i       i       i
42%     som     som     som
43%     eller   eller   eller
43%     juli    juli    juli
44%     men     men     men
46%     kan     kan     kan
46%     på      på      på
46%     under   under   under
48%     av      av      av
49%     ligger  ligger  ligger
51%     med     med     med
53%     en      en      en
53%     of      of      of
56%     den     den     den
56%     det     det     det
57%     km      km      km
57%     millimeter      millimeter      millimeter
59%     delen   delen   delen
59%     meter   meter   meter
60%     att     att     att
60%     om      om      om
64%     °c      °c      °c
64%     lake    lake    lake
64%     mm      mm      mm
65%     för     för     før
66%     inte    inte    inte
66%     kvadratkilometer        kvadratkilometer        kvadratkilometer
66%     per     per     per
67%     havet   havet   havet
71%     till    till    till
72%     närheten        närheten        nærheten
72%     sjö     sjö     sjø
73%     ett     ett     ett
73%     landet  landet  landet
74%     över    över    över
78%     då      då      då
81%     vid     vid     vid
82%     life    life    life
84%     och     och     och
86%     finns   finns   finns
90%     är      är      är
91%     trakten trakten trakten
92%     råder   råder   råder
93%     inga    inga    inga
```
