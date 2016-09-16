import nltk
from nltk.tree import *
from nltk.tag.perceptron import PerceptronTagger
from csv import reader
from textblob import TextBlob

improvements = []
freqtrack = []
locations = []
locparts = []
locranks = []
check = False
tagger = PerceptronTagger()

def readFile():
    f = open("yellowpagesdata.csv")
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
                print location + " has a review of " + review
                getProblem(text,review,location)
            if int(float(review)) == 2:
                print location + " has a review of " + review
                getProblem(text,review,location)
            if int(float(review)) == 3:
                print location + " has a review of " + review
                getProblem(text,review,location)
            if int(float(review)) == 4:
                print location + " has a review of " + review
                getProblem(text,review,location)
            if int(float(review)) == 5:
                print location + " has a review of " + review
                getProblem(text,review,location)
    f.close()

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
            
            
            

'''def results():
    m = max(freqtrack)
    for x in range(m,0,-1):
        indexes = [i for i, j in enumerate(freqtrack) if j == x]
    #indexes = [i for i, j in enumerate(freqtrack) if j == m]
    print "List of Most Needed Improvements:"
    for i in indexes:
        print improvements[i] + " - " + locations[i]
    print freqtrack
    print indexes
    lm = max(locranks)
    lmin = min(locranks)
    for y in range(lm,(lmin-1),-1):
        lindexes = [i for i, j in enumerate(locranks) if j == y]
    print "List of Hospitals (Best to Worst):"
    print locparts
    print locranks
    print lindexes
    print lm, lmin
    #for l in lindexes:
        #print locparts[l] + " - " + str(locranks[l])'''

def traverse(tree,rank,location):
    for n in tree:
        if isinstance(n,Tree):
            if n.label() == 'Basic Chunk':
                nouns = []
                nouns.append(" ".join([a for (a,b) in n.leaves() if (b=="NN" or b=="NNS" or b=="NNP" or b=="NNPS")]))
                print nouns
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
                    print sentence + " is Negative"
                elif pol == 0:
                    print sentence + " is Neutral"
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
                    print sentence + " is Positive"
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
        chunkParser = nltk.RegexpParser(chunkGram)
        chunked = chunkParser.parse(tagged)
        traverse(chunked,rank,location)

    except Exception as e:
        print(str(e))
    

if __name__ == '__main__':
    readFile()
    results()
