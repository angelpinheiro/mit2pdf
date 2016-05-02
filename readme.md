## mit2pdf

Utility to generate an annotated PDF from a MIT-BIH record.


      Options:
      -h, --help            show this help message and exit
      -r RECORD, --record=RECORD
                            Record to print
      -a ANNOTATOR, --annotator=ANNOTATOR
                            Annotator
      -o OFFSET, --offset=OFFSET
                            Offset to start printing in seconds or as an absolute
                            instant in the format hh:mm:ss (default=0)
      -l LIMIT, --limit=LIMIT
                            Limit to print in seconds or as an absolute instant in
                            the format hh:mm:ss (default=None)
      -p PAGESIZE, --pageSize=PAGESIZE
                            Number of seconds per page (default=10)
      -f FILTER, --filter=FILTER
                            Filter beat classes shown Ex:N,V
      -d OUTPUT, --destination=OUTPUT
                            Output file
      --showSamples         Show sample numbers

 

Example:     
    
    ./mit2pdf -r 203_250 -d example.pdf --showSamples --showGrid -f V,N --limit 00:03:30 --pageSize 10
    Loading data and annotations for record 203_250...
    Read 451388 samples
    Read 3108 annotations
    Generating PDF (21 pages) ...]
    Progress: [####################################--------------] 71.43% Complete. 0:00:04 remaining.



![mit2pdf example](example.jpg)