## mit2pdf

Utility to generate an annotated PDF from a MIT-BIH record.

### Getting started 

This tool relies on the[WFDB software package](http://www.physionet.org/physiotools/wfdb.shtml) for signal and annotation reading purposes. 
Once this dependency is satisfied, you can get a PDF from a record as shown in the following examples:

- Limit to 50 seconds, use del annotator, show grid and plot pages of 5 seconds 

        ./mit2pdf -r data/100_250 -a del -l 50 --showGrid -d 100.pdf -p 5

- Plot from second 00:20 to to 01:10 with pages of 5 seconds, without grid

        ./mit2pdf -r data/100_250 -a del -o 00:00:20 -l 00:01:10  -d 100.pdf -p 10   

- Plot only p and t wave peaks

        ./mit2pdf -r data/100_250 -a del -l 50 -d 100.pdf --filter p,t

Result will look like this:

![mit2pdf example](annotations_example.jpg)

### Annotations

At this time only a subset of [annotation codes](https://www.physionet.org/physiotools/wpg/wpg_32.htm) is supported:
 
 * Beat annotations: `N`, `L`, `R`, `B`, `A`, `a`, `J`, `S`, `V`, `r`, `F`, `e`, `j`, `n`, `E`, `/`, `f`, `Q`, `?`
 * Wave start and end annotations: `(`,`)` 
 * P-wave and T-wave peaks: `p`, `t`
 * R-peak: Use a note code `"` with an `r` in the `aux` field


### Available options:

      
 `-r RECORD` `--record=RECORD` Record to print
      
 `-a ANNOTATOR` `--annotator=ANNOTATOR` Annotator(s) to use. Use `,` to separate more than one (default=atr). 
       
 `-o OFFSET` `--offset=OFFSET` Offset to start printing in seconds or as an absolute instant in the format hh:mm:ss (default=0)
      
 `-l LIMIT` `--limit=LIMIT`  Limit to print in seconds or as an absolute instant in the format hh:mm:ss (default=0)
      
 `-p PAGESIZE` `--pageSize=PAGESIZE` Number of seconds per page (default=10)
      
 `-f FILTER` `--filter=FILTER` Filter beat classes shown Ex:N,V
      
 `-b BEATINFO` `--beatInfo=BEATINFO` File with beat info (i.e. waves, peaks, ...)
      
 `-d OUTPUT` `--destination=OUTPUT` Output file




