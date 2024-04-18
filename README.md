# GuCi
Small script/lib for calculating GC content

## Quickstart

```console
$ python3 guci.py
```
### Dependencies
```console
$ # pyfastx
$ # polars
$ # matplotlib
$ pip install -r requirements.txt
```

## Usage
```
usage: guci.py [-h] -f FASTA -w WINDOW [-o OUT_FOLDER] [-p {png,pdf}]

Plot GC content of genomes.

options:
  -h, --help            show this help message and exit
  -f FASTA, --fasta FASTA
                        Fasta file
  -w WINDOW, --window WINDOW
                        Size of sliding window
  -o OUT_FOLDER, --out_folder OUT_FOLDER
                        Output folder
  -p {png,pdf}, --plot_type {png,pdf}
                        How to save the plots
```

## Example
[example](examples/gc_ua159.png)

## Contribute
* Please give the repo a star!
* PR´s are welcome!
