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


## Functions


## Script

# Parse arguments
parser = argparse.ArgumentParser (description="PAT: Plagiat Auto-Tester; essaye de determiner combien du travail entré se trouve sur Google.")
parser.add_argument ("file", type=file, help="Texte à tester")
args = parser.parse_args()

print "Chargement du texte...",

# Open text file, get contents
with args.file as textFile :
    text = textFile.read ()
    
# Cleanup
del args
del parser

print "fait!"
print "Traitement du texte:",

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
    print "  Traitement du bloc de phrases [" + str (i+1) + "/" + str (totalLine - howManyWordsByCheck) + "]:"
    print "   Téléchargement des résultats Google...",
    
    # Everyday in flusheling
    sys.stdout.flush()
    
    (fileName, Null) = urllib.urlretrieve ("http://www.google.fr/search?q=\"" + urllib.quote_plus (sentence) + "\"")
    
    print "fait!"
    print "   Analyse de la page...",
        
    plagiat = False
    with open (fileName) as page :

        if not re.search ("www.gstatic.com/m/images/icons/warning.gif|Aucun document ne correspond", page.read ()) :
            plagiat = True
            
    
    print "fait!"
    
    if plagiat :
        print "    /!\\ Oops, plagiat detecté dans \"" + sentence + "\""
        totalPlagiat = totalPlagiat + 1
    
    
    
print "--"
print str (totalPlagiat) + " occurences de plagiat on été trouvées"
print str (totalLine - howManyWordsByCheck)    + " mots ont été traitées"
print "Ce qui nous donne un magnifique total de " + str (totalPlagiat * 100 / (totalLine - howManyWordsByCheck)) + "% de plagiat! (valeur indicative)"
