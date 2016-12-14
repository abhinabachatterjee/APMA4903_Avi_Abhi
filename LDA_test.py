from xlrd import open_workbook
import string

tweets = open_workbook('Final_Tweet_Table_simulation.xlsx')


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
        text = str(s.cell(row, 2).value)
        #print(text)
        words = [word.lower().strip(string.punctuation) for word in text.split(" ")]
        new_ngrams = []
        #c = 0
        #while c < len(words) - 1:
            #new_ngrams.append((words[c], words[c + 1]))
            #c += 1
        #c = 0
        #while c < len(words) - 2:
            #new_ngrams.append((words[c], words[c + 1], words[c + 2]))
            #c += 1
        
        disclosure = s.cell(row, 3).value
        #if disclosure == 1:
        text_vector.append(text)
        #user_vector.append(user)
        #time_vector.append((hh, disclosure))
        #ngrams_vector.append((list(words), disclosure))
        #unigrams_vector.append((list(words), disclosure))
        #bigrams_vector.append((list(new_bigrams), disclosure))
        #trigrams_vector.append((list(new_trigrams), disclosure))
        #text_vector.append(unigrams_vector)
        #text_vector.append(bigrams_vector)
        #text_vector = ngrams_vector
        
#print(text_vector)

#doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."

#doc_b = "My mother spends a lot of time driving my brother around to baseball practice."

#doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."

#doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."

docs = []

for tweet in text_vector:
    docs.append(tweet)

import gensim
from gensim import corpora, models
import nltk
from nltk.stem.porter import PorterStemmer
p_stemmer = PorterStemmer()
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')
texts = []

for documents in docs:
    low = documents.lower()
    tokens = tokenizer.tokenize(low)
    filtered_words = [word for word in tokens if word not in stopwords.words('english')]
    stemmed_tokens = [p_stemmer.stem(i) for i in filtered_words]
    texts.append(stemmed_tokens)

dictionary = corpora.Dictionary(texts)

corpus = [dictionary.doc2bow(text) for text in texts]

print(corpus[0])

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 6, id2word = dictionary, passes=20)

print(ldamodel.print_topics(num_topics=6, num_words=5))
