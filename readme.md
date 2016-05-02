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
                            the format hh:mm:ss (default=60)
      -p PAGESIZE, --pageSize=PAGESIZE
                            Number of seconds per page (default=10)
      -f FILTER, --filter=FILTER
                            Filter beat classes shown Ex:N,V
      -d OUTPUT, --destination=OUTPUT
                            Output file
      --showSamples         Show sample numbers

 

Resulting PDFs will look like the [example pdf](example.pdf) in this repo, that was generated with:
 
      
    ./mit2pdf -r 203 -d example.pdf --showSamples --showGrid -f V,N --offset 00:00:10 --limit 00:00:30 --pageSize 5


![mit2pdf example](example.jpg)