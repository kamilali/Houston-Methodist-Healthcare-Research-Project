import nltk
import csv
from tabulate import tabulate
from nltk.tree import *
from nltk.tag.perceptron import PerceptronTagger
from csv import reader
from textblob import TextBlob
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt

improvements = []
freqtrack = []
locations = []
locparts = []
locranks = []
check = False
tagger = PerceptronTagger()

def combineCSV():
    ifile  = open('yellowpagesdata.csv', "rb")
    i2file = open('yelpdata.csv', "rb")
    reader = csv.reader(ifile)
    reader2 = csv.reader(i2file)
    ofile  = open('totaldata.csv', "wb")
    writer = csv.writer(ofile)
    for row in reader:
        writer.writerow(row)
    isheader = True
    for row in reader2:
        if isheader:
            isheader = False
        else:
            if not row[2].startswith("Houston"):
                if not row[2].startswith("San Jacinto"):
                    row[2] = "Houston " + row[2]
            writer.writerow(row)

    ifile.close()
    ofile.close()

def readFile():
    f = open("totaldata.csv")
    fin = reader(f)
    isheader = True

    for r in fin:
        if isheader:
            isheader = False
        else:
            location = r[2]
            text = r[1]
            review = r[0]
            if int(float(review)) == 1:
                getProblem(text,review,location)
            if int(float(review)) == 2:
                getProblem(text,review,location)
            if int(float(review)) == 3:
                getProblem(text,review,location)
            if int(float(review)) == 4:
                getProblem(text,review,location)
            if int(float(review)) == 5:
                getProblem(text,review,location)
    f.close()

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

def showchart(f):
    headers = ["Willowbrook","St John", "San Jacinto", "Sugar Land", "St. Catherine", "West", "Main Houston"]
    all_locations = remove_duplicates(locations)
    data = []
    wi = []
    sjo = []
    sja = []
    sl = []
    sc = []
    we = []
    re = []
    for f_x in f:
        if locations[f_x] == "Houston Methodist Willowbrook Hospital":
            wi.append(f_x)
        if locations[f_x] == "Houston Methodist St John Hospital":
            sjo.append(f_x)
        if locations[f_x] == "San Jacinto Methodist Hospital":
            sja.append(f_x)
        if locations[f_x] == "Houston Methodist Sugar Land Hospital":
            sl.append(f_x)
        if locations[f_x] == "Houston Methodist St. Catherine Hospital":
            sc.append(f_x)
        if locations[f_x] == "Houston Methodist West Hospital":
            we.append(f_x)
        if locations[f_x] == "Houston Methodist Hospital":
            re.append(f_x)
    maxval = max(len(wi),max(len(sjo),max(len(sja),max(len(sl),max(len(sc),max(len(we),len(re)))))))

    for i in range(0,maxval):
        data.append([ (improvements[wi[i]] if i < len(wi) else " "), (improvements[sjo[i]] if i < len(sjo) else " "), (improvements[sja[i]] if i < len(sja) else " "), (improvements[sl[i]] if i < len(sl) else " "), (improvements[sc[i]] if i < len(sc) else " "), (improvements[we[i]] if i < len(we) else " "), (improvements[re[i]] if i < len(re) else " ") ])
    print tabulate(data,headers)
    word_frequencies = [[improvements[a],a] for a in sl]
    plotWordCloud(word_frequencies,"Houston Methodist Sugar Land Hospital")
    
def results():
    max_f = max(freqtrack)
    max_r = max(locranks)
    min_r = min(locranks)
    f_x = []
    r_x = []
    for f in range(max_f,0,-1):
        if f in freqtrack:
            for i, j in enumerate(freqtrack):
                if j == f:
                    f_x.append(i)

    for r in range(max_r,(min_r - 1),-1):
        if r in locranks:
            for i, j in enumerate(locranks):
                if j == r:
                    r_x.append(i)

    print "List of Improvements Needed at Specific Hospital:"
    for x in f_x:
        print improvements[x] + " - " + locations[x]

    print "\nList of Hospitals (Best to Worst):"
    for x in r_x:
        print locparts[x]
    print "\n"
    print "Table of Improvements:"
    print "\n"
    showchart(f_x)

global titleFontSize
titleFontSize = 5

def plotWordCloud(word_freqs, title): 
    fig = plt.figure(figsize=(10,10),dpi=720)
    
    wordcloud = WordCloud(max_font_size=40, relative_scaling=0.5).fit_words(word_freqs)
    
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title(title,fontsize=titleFontSize)    
    plt.show()    

def traverse(tree,rank,location):
    for n in tree:
        if isinstance(n,Tree):
            if n.label() == 'Basic Chunk':
                nouns = []
                nouns.append(" ".join([a for (a,b) in n.leaves() if (b=="NN" or b=="NNS" or b=="NNP" or b=="NNPS")]))
                #print nouns
                '''test
                yeet = ""
                for pp in nouns:
                    yeet = yeet + pp
                w = nltk.word_tokenize(yeet)
                t = nltk.pos_tag(w)
                namedEnt = nltk.ne_chunk(t)
                print namedEnt
                test end'''
                adjectives = []
                adjectives.append(" ".join([a for (a,b) in n.leaves() if (b=="JJ" or b=="JJR" or b=="JJS")]))
                #tried using senti-classifier... does not come pre-trained (installed for later use)
                sentence = ""
                for part in adjectives:
                    sentence = sentence + part
                sentence = TextBlob(sentence)
                pol = sentence.sentiment.polarity
                if pol < 0:
                    addition = ""
                    for part in nouns:
                        addition = addition + part
                    exists = False
                    for i in range(0,len(improvements)):
                        if(improvements[i] == addition):
                            freqtrack[i] = freqtrack[i] + 1
                            exists = True
                    if not exists:
                        improvements.append(addition)
                        freqtrack.append(1)
                        locations.append(location)
                    #print sentence + " is Negative"
                elif pol == 0:
                    pass
                    #print sentence + " is Neutral"
                else:
                    addition = ""
                    for part in nouns:
                        addition = addition + part
                    exists = False
                    for i in range(0,len(improvements)):
                        if(improvements[i] == addition):
                            freqtrack[i] = freqtrack[i] - 1
                            exists = True
                    if not exists:
                        improvements.append(addition)
                        freqtrack.append(-1)
                        locations.append(location)
                    #print sentence + " is Positive"
                ex = False
                for l in range(0,len(locparts)):
                    if location == locparts[l]:
                        locranks[l] = locranks[l] + (int(float(rank))-3)
                        ex = True
                if not ex:
                    locparts.append(location)
                    locranks.append(int(float(rank))-3)
                            

def getProblem(text,rank,location):
    #get frequency of negative words in the text provided
    #based on frequency, add to improvements and freqtrack in order of greatest freq to least freq
    #then list the improvements alongside frequency to show what needs improvement
    try:
        tokenized = nltk.word_tokenize(text)
        tagged = nltk.tag._pos_tag(tokenized,None,tagger)
        #chunkGram = r"""Chunk:{<DT>?<JJ.?>*<NN.*>*<VB.?>?<JJ>*<RB.?>*<VB.?>?<IN>?<JJ.?>*<RB.?>*}"""
        #basic chunk gram
        chunkGram = r"""
            Basic Chunk: {<DT>?<JJ.?>+<NN.*>+}
                         {<DT>?<NN.*>+<VB.?>?<RB.?>*<JJ.?>+}
        """
        if len(tagged) == 0:
            pass
        else:
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)
            traverse(chunked,rank,location)

    except Exception as e:
        pass
        #print(str(e))
    

if __name__ == '__main__':
    combineCSV()
    readFile()
    results()
