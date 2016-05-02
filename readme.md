## mit2pdf
Utility to generate an annotated PDF from a MIT-BIH record.

    Usage: mit2pdf [options]

    Options:      
  
    -r RECORD, --record=RECORD  Record to print
  
    -a ANNOTATOR, --annotator=ANNOTATOR Annotator
  
    -o OFFSET, --offset=OFFSET First sample to print (default=0)
  
    -l LIMIT, --limit=LIMIT Number of samples of each channel to print (default=all)
  
    -c CHANNELS, --channels=CHANNELS Number of channels in the input file (default=2)
  
    -p PAGESIZE, --pageSize=PAGESIZE Number of samples per page (default=3000)
  
    -f FILTER, --filter=FILTER Filter beat classes shown Ex:N,V
  
    -d DESTINATION, --destination=DESTINATION Output file
 

Resulting PDFs will look like the [example pdf](example.pdf) in this repo, that was generated with:
 
      
    ./mit2pdf -r 207 --limit 15000 --showSamples -d example.pdf