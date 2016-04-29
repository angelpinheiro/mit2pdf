#!/bin/bash
################################################################################
# @author       : Ángel Piñeiro
# @date         : 29/04/2016
# @version      : 1.0
# @usage        : ./mit2pdf record [samplesLimit] [samplesOffset]
# @description  : Generates an annotated PDF from a MIT record
################################################################################
currdir=`pwd`

if [ $# -lt 0 ]; then
    echo "Usage: sshowMitRecord record [limit]"
    exit 0
fi

# Set WFDB environmet variable to the current directory (prevent conflitcs)
export WFDB=/:.
record=$1
recordName=$(basename ${record})
limit=10000
offset=0

if [ $# -eq 2 ]; then
    limit=$2
fi

if [ $# -eq 3 ]; then
    limit=$2
    offset=$3
fi

echo "Converting signal file..."
rdsamp -r ${record}  -c > ${recordName}.csv

echo "Converting annotations file..."
echo "{\"beats\":[{\"sample\":0}" > ${recordName}.ecgbeats

while read -r line
do
  sampleNumber=$(echo $line | cut -d' ' -f2)
  cls=$(echo $line | cut -d' ' -f3)
  echo ",{\"sample\":"${sampleNumber}", \"cls\":\""${cls}"\"}" >> ${recordName}.ecgbeats
done < <(rdann -r ${record} -a atr)
echo "]}" >> ${recordName}.ecgbeats

echo "Generating PDF..."
python plotEcgToPDF.py -i ${recordName}.csv -a ${recordName}.ecgbeats --limit ${limit}  --offset ${offset} -c 2 --showQRS true -o  ${recordName}.pdf

echo "Cleaning up..."
rm ${recordName}.csv 2> /dev/null
#rm ${recordName}.ecgbeats 2> /dev/null

echo "Done. Check "${recordName}.pdf
