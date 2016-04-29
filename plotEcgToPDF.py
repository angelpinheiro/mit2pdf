# -*- coding: utf-8 -*-
"""
Created on Thu Oct  2 09:29:21 2014

@author: Ángel Piñeiro Souto
###############################################################################
Exports ecg data, beat marks, QRS annotations and morphological families from 
resulting files of mBeat execution to PDF
###############################################################################
Usage: python ecgToPDF.py [options]

Options:
  -h, --help            show this help message and exit
  -i FILE, --input=FILE
                        Input data file
  -a ANNOTATIONSFILE, --annotations=ANNOTATIONSFILE
                        Annotations file
  -f FAMILIESFILE, --families=FAMILIESFILE
                        Families file
  -c CHANNELS, --channels=CHANNELS
                        Number of leads in the input file (default=8)
  --limit=LIMIT         Max number of samples to load from the input file
  --offset=OFFSET       Start at the specified sample number
  --showQRS=SHOWANNS    Show QRST annotations
  --showFamilies=SHOWFAMILIES
                        Show morphological families
  -o OUTPUT, --output=OUTPUT
                        Output file

                     
Example:
                        
python ecgToPDF.py -i ecg.csv -c 2 -a ecg.ecgbeats -f ecg.ecgfamilies --showQRS true --showFamilies true
###############################################################################
"""
from optparse import OptionParser
import matplotlib.pyplot as plt
import numpy as np
import struct
import itertools
import os
import json

from matplotlib.backends.backend_pdf import PdfPages
from operator import itemgetter, attrgetter

"""
 Load ecg from a file in the mBeatDump format
"""
def loadDataFromMbeatDump(filepath, samples, offset=0, channels=8):
    with open(filePath, 'rb') as f:
        # print "Seek to " + str(offset*4*channels) + " and read " + str(samples*channels*4) + " bytes..."
        f.seek(offset * 4 * channels)  # testing
        unpackOptions = '>' + str(samples * channels) + 'f';
        data = struct.unpack(unpackOptions, f.read(samples * channels * 4))
        minData = min(data)
        clean_data = [x if x != 1000 else minData for x in data]
        return clean_data


"""
Load ecg from a file in csv format
"""
def loadDataFromCsv(filepath, samples, offset=0, channels=2, data=[]):
    segment = []
    for i in xrange(offset, offset + samples):
        segment.extend(data[i])
    return segment


"""
 Load annotations from a json file
"""
def loadAnnotationsFromJson(annotationsFile):
    anns = []
    if annotationsFile != "":
        json_data = open(annotationsFile)
        js = json.load(json_data)
        anns = js["beats"]
        print str(len(anns)) + " annotations in file"
    return anns


"""
 Load annotations from a json file
"""
def loadEventsFromJson(eventsFile):
    events = []
    if eventsFile != "":
        json_data = open(eventsFile)
        js = json.load(json_data)
        events = js["events"]
        events.sort(key=itemgetter("position"))
        print str(len(events)) + " events in file"
    return events


"""
 Plot annotations in the specified plot
"""
def plotAnnotationsFromJson(annotations, offset, plt, channel, data):
    top = max(data)
    minSample = offset
    maxSample = offset + len(data) / channels
    for a in annotations:
        sampleNumber = a["sample"]
        cls = a["cls"] if "cls" in a.keys() else "?"
        # print cls
        if (sampleNumber > minSample):
            if (sampleNumber < maxSample):
                family = str(a["family"]) if "family" in a.keys() else None
                plt.axvline(x=sampleNumber - offset, color='black', linestyle=':', lw=0.8)
                plt.text(sampleNumber - offset - 13, top, u'♡', color='black', fontsize=8)  # " " + str(sampleNumber)
                plt.text(sampleNumber - offset, top, " " + cls + " " + str(sampleNumber), color='black',
                         fontsize=11)  # " " + str(sampleNumber)
                if (showAnns):
                    plotBeatInfo(plt, a, channel, offset, data, family)
            else:
                break

def sampleValue(position, offset, data):
    return data[position - offset]


"""
 Plot events in the specified plot
"""
def plotEventsFromJson(events, offset, plt, channel, data):
    top = max(data)
    minSample = offset
    maxSample = offset + len(data) / channels
    for e in events:
        type = e["type"]
        start = e["position"]
        end = e["endPosition"]
        lead = e["lead"]
        # find artifacts that start or end in this page
        if type == "ARTIFACT" and lead == channel:
            if start > minSample < maxSample or end > minSample < maxSample:
                if start < minSample:
                    start = minSample
                if end > maxSample:
                    end = maxSample

                print type, start, end, lead

                plt.hlines(0, start - offset, end - offset, color='red', lw=30, alpha=0.2)
                # plt.text(start-offset,0,"Start: " + str(start), color='black',fontsize=8)
                #plt.text(end-offset,0,"End: " + str(end), color='black',fontsize=8)


"""
# Plot wave mark
"""
def plotWaveMark(plt, pos, label, offset, color, sampleVal=0, ymin=0.2, ymax=0.8, line=True):
    if line:
        plt.axvline(x=pos - offset, color=color, ymin=ymin, ymax=ymax, lw=0.3)
    plt.text(pos - offset - 4, sampleVal, label, fontsize=7, color=color)


"""
# Plot beat info
"""
def plotBeatInfo(plt, a, channel, offset, data, label):
    ldata = data[channel::channels]
    dmin = min(data)
    dmax = max(data)
    drange = dmax - dmin
    pad = (drange) / 20
    minData = dmin - pad * 2
    try:
        if not "leads" in a.keys():
            return;

        info = a["leads"][channel]
        # P Wave

        p = info["P_wave"]

        posp = p["pos"]
        if posp != 0:
            val = sampleValue(posp, offset, ldata)
            plotWaveMark(plt, posp, "p", offset, 'orange', sampleVal=val + pad, ymin=0.3, ymax=0.5)
        onp = a["P"]["onset_pos"]
        if onp != 0:
            plotWaveMark(plt, onp, "[", offset, 'green', sampleVal=sampleValue(onp, offset, ldata) - pad, line=False)
        offp = a["P"]["offset_pos"]
        if offp != 0:
            plotWaveMark(plt, offp, "]", offset, 'green', sampleVal=sampleValue(offp, offset, ldata) - pad, line=False)

        # Q Wave

        q = info["Q_wave"]["pos"]
        if q != 0:
            plotWaveMark(plt, q, "q", offset, 'red', minData)

        # R wave
        r = info["R_wave"]["pos"]
        if r != 0:
            plotWaveMark(plt, r, "r", offset, 'brown', minData)
        s = info["S_wave"]["pos"]
        if s != 0:
            plotWaveMark(plt, s, "s", offset, 'blue', minData)

        # T wave
        t = info["T_wave"]
        post = t["pos"]
        if post != 0:
            val = sampleValue(post, offset, ldata)
            plotWaveMark(plt, post, "t", offset, 'orange', sampleVal=val + pad, ymin=0.2, ymax=0.7)
        ont = a["T"]["onset_pos"]
        if ont != 0:
            plotWaveMark(plt, ont, "[", offset, 'green', sampleVal=sampleValue(ont, offset, ldata) - pad, line=False)
        offt = a["T"]["offset_pos"]
        if offt != 0:
            plotWaveMark(plt, offt, "]", offset, 'green', sampleVal=sampleValue(offp, offset, ldata) - pad, line=False)

    except IndexError:
        return


"""
# Plot ecg in mbeatDump format
"""
def plotEcgDump(data, channnels, annotations=[], events=[], offset=0, pdf=None):
    if len(data):
        dataMin = min(data);
        dataMax = max(data);
        yAxInit = dataMin - (dataMax - dataMin) / 5
        yAxEnd = dataMax + (dataMax - dataMin) / 5
        # build the plot
        # plt.suptitle('ECG')
        for i in range(channels):
            if pdf is not None:
                fig = plt.gcf()
                fig.set_size_inches(24, 1.5 * channels)
            sp = plt.subplot(channels, 1, i + 1)
            sp.get_yaxis().set_visible(True)
            sp.get_xaxis().set_visible(False)
            sp.set_xlim(axInit, axEnd)
            sp.set_ylim(yAxInit, yAxEnd)
            sp.axis('off')
            sp.plot(data[i::channels], linewidth=0.8)
            plotAnnotationsFromJson(annotations, offset, plt, i, data)
            plotEventsFromJson(events, offset, plt, i, data)
        plt.text(-80, -100, str(offset))
        plt.text(pageSize + 20, -100, str(offset + len(data) / channels))
        plt.tight_layout()
        # show plot
        if pdf is not None:
            plt.suptitle(' Samples ' + str(offset) + " to " + str(offset + len(data) / channels))
            fig.savefig(pdf, format='pdf', dpi=600)
            plt.close()
        else:
            plt.show()


"""
 Plot morphological families
"""
def plotFamilies(familiesFile, pdf):
    json_data = open(familiesFile)
    data = json.load(json_data)
    families = data["families"]
    nFamilies = len(families)
    maxleads = 0
    for f in range(nFamilies):
        family = families[f]
        if family is not None:
            maxleads = max(len(family["segments"]), maxleads)

    for f in range(nFamilies):
        family = families[f]
        if family is not None:
            fid = str(family["id"])
            leads = len(family["segments"])
            print "Family " + str(f) + ", leads: " + str(leads)
            for i in range(leads):
                color = "b"
                beat = family["segments"][i]["samples"]
                fig = plt.gcf()
                fig.set_size_inches(24, 3.5)
                sp = plt.subplot(1, maxleads, i + 1)
                sp.axis('off')
                sp.set_title("Family " + fid + " lead " + str(i))
                sp.plot(beat, color=color)
            plt.tight_layout()
            fig.savefig(pdf, format='pdf', dpi=600)
            plt.close()


"""
 Read annotations
"""
def readAnnotations(annotationsFile):
    annotations = []
    if annotationsFile != "":
        print "Reading annotations file " + annotationsFile + "..."
        annotations = loadAnnotationsFromJson(annotationsFile)
        annotations.sort(key=itemgetter("sample"))

    return annotations

# ##############################################################################
# Main program
###############################################################################
# parse arguments
parser = OptionParser()
parser.add_option("-i", "--input", dest="file", default="", help="Input data file")
parser.add_option("-a", "--annotations", dest="annotationsFile", default="", help="Annotations file")
parser.add_option("-e", "--events", dest="eventsFile", default="", help="Events file")
parser.add_option("-f", "--families", dest="familiesFile", default="", help="Families file")
parser.add_option("-c", "--channels", dest="channels", default=8, help="Number of leads in the input file (default=8)")
parser.add_option("--limit", dest="limit", default=0, help="Max number of samples to load from the input file")
parser.add_option("--offset", dest="offset", default=0, help="Start at the specified sample number")
parser.add_option("--showQRS", dest="showAnns", default=False, help="Show QRST annotations")
parser.add_option("--showFamilies", dest="showFamilies", default=False, help="Show morphological families")
parser.add_option("-o", "--output", dest="output", default="ecg.pdf", help="Output file")
(options, args) = parser.parse_args()

# get options
filePath = options.file
annotationsFile = options.annotationsFile
eventsFile = options.eventsFile
channels = int(options.channels)
limit = int(options.limit)
offset = int(options.offset) * channels
showAnns = options.showAnns
showFamilies = options.showFamilies
familiesFile = options.familiesFile
toPdf = options.output

# read input files
print "Reading file " + filePath + "..."
data = np.genfromtxt(filePath, delimiter=",", usecols=(1, 2))
annotations = readAnnotations(annotationsFile)
events = loadEventsFromJson(eventsFile);

totalSamples = len(data)
samplesPerLead = totalSamples / channels
samples = min(samplesPerLead, limit) if limit > 0 else samplesPerLead
pageSize = 3000  # by channel
start = offset
axInit = 0
axEnd = pageSize
pages = samples / pageSize + 1
pg = 1

pdf = PdfPages(toPdf)

print "\nResulting PDF will have " + str(pages) + " pages"

# iterate and print pages      
while start < samples:
    if start + pageSize > samples:
        pageSize = samples - start
    print "Printing page " + str(pg) + " of " + str(pages) + "..."
    plotEcgDump(loadDataFromCsv(filePath, pageSize, start, channels, data), channels, annotations, events, start, pdf)
    start = start + pageSize
    pg = pg + 1

# plot families if needed
if showFamilies is not False:
    plotFamilies(familiesFile, pdf)

pdf.close()

print "Done."