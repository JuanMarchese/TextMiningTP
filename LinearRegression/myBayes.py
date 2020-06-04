import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from functools import partial

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression

from pprint import pprint

import nltk
nltk.download('stopwords')

pd.options.display.max_columns=None


from DataSources import BitcoinHistoricalDataReader, AutoTweetReader
from utils import log, Timer, MultiDate
from textProcessing import SuperCounter, AutoToken, TweetFuncs
from workflows import AutoWorkflow, enrichWithPrice, discretize


def histogramPrices():
    prices = BitcoinHistoricalDataReader.read()['Price']

    allPs = []
    lsatP = None
    for p in prices:
        if lsatP is not None:
            variance = p / lsatP - 1
            allPs.append(variance)
        lsatP = p

    plt.hist(allPs, bins=np.linspace(-0.1, 0.1, 20))
    plt.show()



def main():
    print('YO! starting')

    data = AutoWorkflow.getTweets(100)

    ## restrict to 1 month:
    #data = data[data['date'] < '2019-06-01']

    superData = enrichWithPrice(data)

    # dates = {date: datetime.datetime.strptime(date, DATE_FORMAT) for date in dateAsString.unique()}

    # discretize columns
    with Timer('Discretizing columns'):
        for colName in superData.columns:
            if colName.startswith('offset_col'):
                superData[colName] = superData[colName].apply(partial(discretize, .02))

    xTrain = superData[superData['date'] < '2019-11-01']['text']
    yTrain = superData[superData['date'] < '2019-11-01']['offset_col0']

    # Defino el pipeline
    pipeline_NB = Pipeline([
        ('tfidf', TfidfVectorizer(
            # preprocessor=clean_text,
            tokenizer=AutoToken(),
            stop_words="english")),
        ('clf', MultinomialNB())
    ])

    pipeline = Pipeline([('tfidf', TfidfVectorizer(tokenizer=AutoToken(),
                                                   stop_words="english",
                                                   ngram_range=(1, 3),
                                                   min_df=0.03)),

                         ('clf', LogisticRegression(random_state=0,
                                                    multi_class='multinomial',
                                                    solver='lbfgs',
                                                    penalty='l2',
                                                    class_weight='balanced',
                                                    n_jobs=-1))])

    with Timer('training logistic regression'):
        m = pipeline.fit(xTrain, yTrain)


    #check what's important
    features = m[0].vocabulary_
    weights = m[1].coef_[0]
    stuff = sorted([(w, f) for f, w in zip(features, weights)], key=lambda x: abs(x[0]), reverse=True)
    log(stuff)

    # #check balance
    # txts = list(xTrain)[:100000]
    # p = m.predict(txts)
    #
    # print(len([i for i in p if i > 0]) / len(p))
    # print(len([i for i in p if i == 0]) / len(p))
    # print(len([i for i in p if i < 0]) / len(p))


    avgValue = {}
    for date in sorted(set(superData['date'])):
        textsForDate = superData[superData['date'] == date]
        with Timer(' predicting for date {} => {}'.format(date, len(textsForDate))):
            avg = sum(m.predict(textsForDate['text'])) / len(textsForDate)
        log('   avg: {}'.format(avg))
        avgValue[date] = avg

    pprint( avgValue )
    return avgValue



if __name__ == '__main__':
    #histogramPrices()
    main()



    print('Done!')

