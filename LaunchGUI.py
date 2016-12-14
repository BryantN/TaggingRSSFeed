from Tkinter import *
import OrganizeHelper
import KeywordRecognize
from nltk.tag.stanford import StanfordNERTagger
import os
import random
import matplotlib
import math
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

java_path = "C:/Program Files/Java/jre1.8.0_111/bin/java.exe"
os.environ['JAVAHOME'] = java_path

"""
Gui Created to make project More intuitive.
Has the code to run the tests and demonstrate the keyword detection and Tag prediction


"""
#Tkinter Application Class, that houses most of the logic
class Application(Frame):
    # constructor for the tkinter Application
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.LABELS = ['Verb', 'Noun', 'Proper Noun', 'Name']
        self.tagPredictor = 0
        self.english_nertagger = StanfordNERTagger('.\NER\classifiers\english.all.3class.distsim.crf.ser.gz',
                                                   '.\NER\stanford-ner.jar')
        self.compiledData = 0
        self.createWidgets()

    # Creates the Widgests from Tkinter
    # also positions said Widgets
    def createWidgets(self):
        self.frameL = Frame(self)
        self.frameL.pack(side=LEFT, fill=BOTH, expand=True)
        self.frameR = Frame(self)
        self.frameR.pack(side=RIGHT, fill=BOTH, expand=True)
        self.frameB = Frame(self)
        self.frameB.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.QUIT = Button(self.frameB)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit
        self.QUIT.pack(side=BOTTOM, anchor=S, expand=True)

        self.analysisBut = Button(self.frameR)
        self.analysisBut["text"] = 'Run Analysis'
        self.analysisBut["command"] = self.runAnalysis
        self.analysisBut.pack()

        self.v = StringVar()
        self.resultLabel = Label(self.frameR, textvariable=self.v)
        self.resultLabel.pack(side=LEFT, fill=BOTH, expand=True)
        self.v.set("Results")

        self.nounvar = IntVar()
        self.verbvar = IntVar()
        self.pnounvar = IntVar()
        self.namevar = IntVar()

        self.inputTitle = Entry(self.frameL, width=100)
        self.inputTitle.pack(fill=X, expand=False)
        self.inputTitle.insert(0, 'DEFAULT VALUE')

        self.resultWindow = Text(self.frameL)
        self.resultWindow.pack(fill=X, expand=True)

        self.IDKeywordsBut = Button(self.frameL)
        self.IDKeywordsBut.pack()
        self.IDKeywordsBut["text"] = "VIEW KEYWORDS"
        self.IDKeywordsBut["command"] = self.HighlightKeywords

        self.Nounbox = Checkbutton(self.frameL, text="Nouns", variable=self.nounvar)
        self.Nounbox.pack(side=TOP)
        self.VerbBox = Checkbutton(self.frameL, text="Verbs", variable=self.verbvar)
        self.VerbBox.pack(side=TOP)
        self.ProperNounBox = Checkbutton(self.frameL, text="Proper Nouns", variable=self.pnounvar)
        self.ProperNounBox.pack(side=TOP)
        self.NameBox = Checkbutton(self.frameL, text="Names", variable=self.namevar)
        self.NameBox.pack(side=TOP)

        self.f = Figure(figsize=(5, 5), dpi=100)
        self.graph = self.f.add_subplot(111)
        self.graph.set_ylim([0, 1])
        self.graph.bar(range(4), [.50, .50, .50, .5], align="center")
        self.graph.set_xticks(range(len(self.LABELS)))
        self.graph.set_xticklabels(self.LABELS)
        self.canvas = FigureCanvasTkAgg(self.f, self.frameR)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frameR)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)



    # Simply Compiles the Data, into a usable vairbale format.
    # also Outputs the Data, to compiledInput file.
    def CompileAllData(self):
        self.compiledData = OrganizeHelper.CompileData()

    # runs analysis on the given types of Keywords.
    # identifies Succsess by seeing if the Top 3 predicted Tags were tweeted with the atcual article.
    def __runAnalysis(self, wordsToSearch, nameId):
        if self.compiledData == 0:
            self.CompileAllData()
        random.shuffle(self.compiledData)
        testData = self.compiledData[:len(self.compiledData) / 10]
        trainData = self.compiledData[len(self.compiledData) / 10:]
        tagPredictor = KeywordRecognize.generatetagpredictor(trainData, False)
        results = []
        length=len(testData)
        print length
        count=0
        for datapoint in testData:
            count+=1
            if count == math.floor(length/2):
                print "Halfway"
            importantwords = KeywordRecognize.idwordtype(datapoint['title'], wordsToSearch)
            if nameId:
                importantwords += KeywordRecognize.idNames(datapoint['title'], self.english_nertagger)
            Allpossible = dict()
            for word in importantwords:
                word_l = word.lower()
                if word_l in tagPredictor:
                    Allpossible = OrganizeHelper.combinedict(tagPredictor[word_l], Allpossible)
            tagsByFrequency = sorted(Allpossible, key=Allpossible.get, reverse=True)
            top3 = tagsByFrequency[0:3 if len(tagsByFrequency) >= 3 else len(tagsByFrequency)]
            nummatches = 0
            alllowered = [x.lower() for x in datapoint['links']]
            for i in top3:
                if i in alllowered:
                    nummatches += 1
            results.append(nummatches)
        print float(sum(results)) / float(len(results) * 3)
        return float(sum(results)) / float(len(results) * 3)

    def runAnalysis(self):
        verbPercent = self.__runAnalysis(['V'],False)
        nounPercent = self.__runAnalysis(['N'],False)
        ProperNounPercent = self.__runAnalysis(['NNP'],False)
        NamePercent = self.__runAnalysis(['NNP'], True)
        self.f.clear()
        self.graph = self.f.add_subplot(111)
        self.graph.set_ylim([0, 1])
        self.graph.set_xticks(range(len(self.LABELS)))
        self.graph.set_xticklabels(self.LABELS)
        self.graph.bar(range(4), [verbPercent,nounPercent,ProperNounPercent, NamePercent],align="center")
        self.canvas.draw()

    # using the input from the Text Box, highlights the chosen types of keywords, and
    # Shows the Top 6 Tags below it.
    def HighlightKeywords(self):
        self.resultWindow.tag_configure("highlight", background="yellow")
        headline = self.inputTitle.get()
        self.resultWindow.delete(1.0, END)
        self.resultWindow.insert(1.0, headline)
        tagsToSearchFor = []
        if self.nounvar.get() == 1:
            tagsToSearchFor += ['N']
        if self.verbvar.get() == 1:
            tagsToSearchFor += ['V']
        if self.pnounvar.get() == 1:
            tagsToSearchFor += ['NNP']
        importantWords = KeywordRecognize.idwordtype(headline, tagsToSearchFor)
        if self.namevar.get() == 1:
            importantWords += KeywordRecognize.idNames(headline, self.english_nertagger)
        for i in importantWords:
            self.resultWindow.tag_add("highlight", "1." + str(headline.find(i)), "1." + str(headline.find(i) + len(i)))
        if self.tagPredictor == 0:
            if self.compiledData == 0:
                self.CompileAllData()
            self.tagPredictor = KeywordRecognize.generatetagpredictor(self.compiledData, False)
        allPossible = {}
        for word in importantWords:
            word_l = word.lower()
            if word_l in self.tagPredictor:
                allPossible = OrganizeHelper.combinedict(self.tagPredictor[word_l], allPossible)
        tagsByFrequency = sorted(allPossible, key=allPossible.get, reverse=True)
        topTags = tagsByFrequency[0:12 if len(tagsByFrequency) >= 12 else len(tagsByFrequency)]
        for i in range(len(topTags)):
            self.resultWindow.insert(END, '\n' + topTags[i])
# Launch the Gui itself
root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()