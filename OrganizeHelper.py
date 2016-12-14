from KeywordRecognize import generatetagpredictor,idNames,idwordtype
import json
from os import listdir
from os.path import isfile, join


def CompileData():
    onlyfiles = [f for f in listdir("./InputData") if isfile(join("./InputData", f))]

    #goals, kay compile input to single output, with training data
    ALLDATA=[]
    for input_f in onlyfiles:
        ALLDATA += json.load(open('./InputData/'+input_f))
    f = open('./MappedKeyWords/CompiledInput', 'w')
    json.dump(ALLDATA, f)
    return ALLDATA

def combinedict(dict1,dict2):
    dictret=dict()
    for key, val in dict1.iteritems():
        if key in dict2:
            dict2[key]+=dict1[key]
        else:
            dict2[key]=dict1[key]
    return dict2
"""
Depricated Code moved to the Gui
if __name__=="__main__":
    all_data = CompileData()
    testData = all_data[:len(all_data)/10]
    trainData = all_data[len(all_data)/10:]
    tagPredictor = generatetagpredictor(trainData, False)
    results=[]
    for datapoint in testData:
        importantwords = idwordtype(datapoint['title'], ['V'])
        max_occurence = 0
        max_tag = 'nfl'
        compiledALLTAGS_freq=[]
        Allpossible=dict()
        for word in importantwords:
            word_l=word.lower()
            if word_l in tagPredictor:
                Allpossible=combinedict(tagPredictor[word_l],Allpossible)

        tagsByFrequency = sorted(Allpossible, key=Allpossible.get, reverse=True)
        top3=tagsByFrequency[0:3 if len(tagsByFrequency)>=3 else len(tagsByFrequency)]
        nummatches=0
        alllowered=[x.lower() for x in datapoint['links']]
        for i in top3:
            if i in alllowered:
                nummatches+=1
        results.append(nummatches)
    print float(sum(results))/float(len(results)*3)
"""