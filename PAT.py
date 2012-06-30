#!/usr/bin/python
# -*- coding: UTF8 -*-


## PAT: Plagiat Auto-Tester
#   Version 0.0.1


## Configuration
howManyWordsByCheck = 20 # Maximum 32; words delimited by "'", "-", space and newline


## Imports
import argparse # For the command-line parsing
import re       # To split the file in sentences
import urllib   # Download Google's results
import sys      # To flush!


## Script

# Parse arguments
parser = argparse.ArgumentParser (description="PAT: Plagiat Auto-Tester; try to determine how much of your text is on Google.")
parser.add_argument ("file", type=file, help="Text to test")
args = parser.parse_args()

print "Loading text...",

# Open text file, get contents
with args.file as textFile :
    text = textFile.read ()
    
# Cleanup
del args
del parser

print "done!"
print "Text processing:",

# Making a nice list
sentences = re.split ("[ -'\n]", text)
del text

for i in range (sentences.count ("")) :
    sentences.remove ("")

# Setup some variables
totalLine    = len (sentences)
totalPlagiat = 0
sentence     = ""


# Main part
for i in range (totalLine - howManyWordsByCheck) :

    # New Google ID
    if i % 100 == 0 :
    
        class AppURLopener(urllib.FancyURLopener):
            version = str (i)
        urllib._urlopener = AppURLopener()

    sentence = ""
    for text in sentences [i:i+howManyWordsByCheck] :
    
        if not sentence == "" :
            sentence = sentence + " " + text
        
        else :
            sentence = text

    print
    print "  Processing of text-bloc [" + str (i+1) + "/" + str (totalLine - howManyWordsByCheck) + "]:"
    print "   Downloading Google's result...",
    
    # Everyday in flusheling
    sys.stdout.flush()
    
    (fileName, Null) = urllib.urlretrieve ("http://www.google.co.uk/search?q=\"" + urllib.quote_plus (sentence) + "\"")
    
    print "done!"
    print "   Page processing...",
        
    plagiat = False
    with open (fileName) as page :

        if not re.search ("www.gstatic.com/m/images/icons/warning.gif| - did not match any documents.", page.read ()) :
            plagiat = True
            
    
    print "done!"
    
    if plagiat :
        print "    /!\\ Oops, plagiat detected in \"" + sentence + "\""
        totalPlagiat = totalPlagiat + 1
    
    
    
print "--"
print str (totalPlagiat) + " plagiat's occurence were found"
print str (totalLine - howManyWordsByCheck)    + " words were processed"
print "what give us a beautiful score of " + str (totalPlagiat * 100 / (totalLine - howManyWordsByCheck)) + "% of palgiat! (more or less)"
