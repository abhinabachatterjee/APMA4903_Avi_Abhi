import nltk
from nltk import *
import random
from xlrd import open_workbook
import re
import datetime
from datetime import time
from time import strftime
import string

#Edited Dataset of Classified & Filtered Tweets for Simulation
tweets = open_workbook('Final_Tweet_Table_sim_edited.xlsx')

for s in tweets.sheets():
    numb_row = s.nrows
    numb_col = s.ncols

    time_vector = []
    user_vector = []
    unigrams_vector = []
    bigrams_vector = []
    trigrams_vector = []
    ngrams_vector = []
    text_vector = []
    disclosure_vector = []

    for row in range(1, numb_row):
        timetweet = s.cell(row, 0).value
        dt = datetime.datetime.fromtimestamp(timetweet)
        hh = dt.hour
        user = str(s.cell(row, 1).value)
        text = str(s.cell(row, 2).value)
        words = [word.lower().strip(string.punctuation) for word in text.split(" ")]
        new_ngrams = []
        c = 0
        #for TRIGRAMS
        #while c < len(words) - 1:
            #new_ngrams.append((words[c], words[c + 1]))
            #c += 1
        c = 0
        #for BIGRAMS
        #while c < len(words) - 2:
            #new_ngrams.append((words[c], words[c + 1], words[c + 2]))
            #c += 1
        disclosure = s.cell(row, 3).value
        user_vector.append(user)
        time_vector.append((hh, disclosure))
        ngrams_vector.append((list(words), disclosure))
        #unigrams_vector.append((list(words), disclosure))
        #bigrams_vector.append((list(new_bigrams), disclosure))
        #trigrams_vector.append((list(new_trigrams), disclosure))
        #text_vector.append(unigrams_vector)
        #text_vector.append(bigrams_vector)
        text_vector = ngrams_vector

random.shuffle(text_vector)

all_words = []
#for vector in text_vector:
for (tweet, category) in text_vector:
    for t in tweet:
        all_words.append(t)

all_words = nltk.FreqDist(all_words)

word_features = list(all_words.keys())

def find_features(blurb):
    words = set(blurb)
    features = {}
    #print(blurb)
    for w in word_features:
        features[w] = (w in words)
    return features

allfeatures = []
#for vector in text_vector:
featuresets = [(find_features(tw), category)  for (tw, category) in text_vector]
#print(featuresets[:5])

training_set = featuresets[:500]
testing_set = featuresets[500:]

classifier = nltk.NaiveBayesClassifier.train(training_set)

print("Naive Bayes Algo accuracy:", (nltk.classify.accuracy(classifier, testing_set)))
classifier.show_most_informative_features(10)