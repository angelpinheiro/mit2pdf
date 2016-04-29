#!/bin/bash
################################################################################
# @author       : Ángel Piñeiro
# @date         : 29/04/2016
# @version      : 1.0
# @usage        : ./mit2pdf folder record [samplesLimit]
# @description  : Generates an annotated PDF from a MIT record
################################################################################
currdir=`pwd`
if [ $# -lt 2 ]; then
    echo "Usage: sshowMitRecord <path ><record> <limit>"
    exit 0
fi

# Set WFDB environmet variable to the current directory (prevent conflitcs)
export WFDB=.
targetDir=$1
record=$2

if [ $# -eq 3 ]; then
    limit=$2
fi
cd ${targetDir}

echo "Converting signal file..."
rdsamp -r ${record}  -c > ${currdir}/${record}.csv

echo "Converting annotations file..."
echo "{\"beats\":[{\"sample\":0}" > ${currdir}/${record}.ecgbeats

#while read -r line; do echo $line; done < <(rdann -r 100_250 -a atr)

while read -r line
do
  sampleNumber=$(echo $line | cut -d' ' -f2)
  echo ",{\"sample\":"${sampleNumber}"}" >> ${currdir}/${record}.ecgbeats
done < <(rdann -r ${record} -a atr)
echo "]}" >> ${currdir}/${record}.ecgbeats

cd ${currdir}
echo "Generating PDF..."

python plotEcgToPDF.py -i ${record}.csv -a ${record}.ecgbeats --limit 15000 -c 2 --showQRS true -o  ${record}.pdf

echo "Cleaning up..."
rm ${record}.csv 2> /dev/null
rm ${record}.ecgbeats 2> /dev/null

echo "Done. Check "${record}.pdf
