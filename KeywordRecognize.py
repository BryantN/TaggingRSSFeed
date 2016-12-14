import nltk
import os
from nltk.tag.stanford import StanfordNERTagger

"""
This File contains the Keyword Tagging Logic
Fairly Simple Tagging on parts of speech
Named Entity Recognition takes approximately 30 seconds to run per sentence.
Often Will fail, on bad charcter encodes
"""

#Simple Part of Speech Tagging.
def idwordtype(sentence, wordtypes):
    nouns=[]
    words = nltk.pos_tag(nltk.word_tokenize(sentence))
    for word in words:
        for typew in wordtypes:
            if len(typew) == 1 and word[1][0] == typew:
                nouns.append(word[0])
            elif len(typew) > 1 and word[1] == typew:
                nouns.append(word[0])
    return nouns

#More Complex Name Tagging
def idNames(sentence,english_nertagger):
    Names=[]
    try:
        NERfromWords = english_nertagger.tag(sentence.split())
        for obj in NERfromWords:
            if obj[1] == 'PERSON':
                Names.append( obj[0])
    except Exception as e:
        print e
    return Names


def generatetagpredictor(Titles_and_tags, identifyNames):
    java_path = "C:/Program Files/Java/jre1.8.0_111/bin/java.exe"
    os.environ['JAVAHOME'] = java_path
    english_nertagger = StanfordNERTagger('.\NER\classifiers\english.all.3class.distsim.crf.ser.gz',
                                          '.\NER\stanford-ner.jar')
    keywordsToTags = dict()
    for i in xrange(len(Titles_and_tags)):
        title=Titles_and_tags[i]['title']
        words = idwordtype(title, ['N', 'V', 'NNp'])
        names = idNames(title,english_nertagger) if identifyNames else []
        AllKeyWords = list(set(words+names))#deletes duplicates
        for word in AllKeyWords:
            word = word.lower()
            for tag in Titles_and_tags[i]['links']:
                tag = tag.lower()
                if keywordsToTags.has_key(word):
                    if keywordsToTags[word].has_key(tag):
                        keywordsToTags[word][tag] += 1
                    else:
                        keywordsToTags[word][tag] = 1
                else:
                    keywordsToTags[word] = dict()
    return keywordsToTags
    #print Titles_and_tags[i]['links']