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
λ › python3 falsefrond.py barn barnet barns barnets man sjö åt | sort -nr
73%     barn    barn    barn
71%     barnets barnets barnets
69%     man     man     man
67%     barns   barns   barns
67%     barnet  barnet  barnet
28%     sjö     sjö     sjø
16%     åt      åt      åt
sim     srcWord commonWord      tarWord
```


```
λ › python3 falsefrond.py | head -n 50 | sort -nr
62%     de      de      de
58%     som     som     som
58%     i       i       i
58%     .       .       .
57%     -       -       -
56%     ,       ,       ,
54%     på      på      på
52%     av      av      av
51%     ligger  ligger  ligger
49%     med     med     med
47%     of      of      of
47%     en      en      en
46%     )       )       )
46%     #       #       #
45%     (       (       (
45%     '       '       '
44%     det     det     det
44%     den     den     den
43%     km      km      km
41%     </s>    </s>    </s>
41%     meter   meter   meter
41%     delen   delen   delen
40%     om      om      om
40%     att     att     att
39%     #omdirigering   #omdirigering   #omdirigering
36%     mm      mm      mm
36%     °c      °c      °c
35%     för     för     før
33%     havet   havet   havet
29%     till    till    till
27%     underarter      underarter      underarter
27%     landet  landet  landet
27%     ett     ett     ett
26%     över    över    över
22%     då      då      då
21%     }}      }}      }}
20%     släktet släktet släktet
19%     månaden månaden månaden
18%     life    life    life
18%     familjen        familjen        familjen
16%     och     och     och
14%     finns   finns   finns
13%     catalogue       catalogue       catalogue
10%     är      är      är
9%      trakten trakten trakten
9%      kallaste        kallaste        kallaste
7%      inga    inga    inga
4%      runt    runt    runt
1%      ingår   ingår   ingår
sim     srcWord commonWord      tarWord
```
