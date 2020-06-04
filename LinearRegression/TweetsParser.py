import pandas as pd
import ntpath
import numpy as np

TWEETS_FILE_PATH = r"C:\Users\Luxor\Documents\Text Mining\bitcoin-tweets-20160101-to-20190329\tweets.csv"

#TWEETS_FILE_PATH = r"C:\Users\Luxor\Documents\Text Mining\bitcoin-tweets-20160101-to-20190329.zip"

def binaryTranscribeFirstNLines( fullPath, size ):
    with open(fullPath, mode='rb') as fi:
        fullFilaPath, extension = fullPath.rsplit('.', 1)
        outputFile = '{}.{}.{}'.format( fullFilaPath, 'transcribed', extension )
        with open( outputFile, mode='wb' ) as fo:
            fo.write(fi.read(size))


def transcribeFirstNLines( fullPath, lines ):
    with open(fullPath, mode='r', encoding="utf8") as fi:
        fullFilaPath, extension = fullPath.rsplit('.', 1)
        outputFile = '{}.{}.{}'.format( fullFilaPath, 'transcribed', extension )
        with open( outputFile, mode='w', encoding='utf8' ) as fo:
            for _ in range(lines):
                fo.writelines( fi.readline())


dtype = {"date": str,
         "text": str,
         "language": str,
         "language_proba": float}

dtypes = {"id": str,
          "user": str,
          "fullname": str,
          "url": str,
          "timestamp": str,
          "replies": pd.Int64Dtype(),
          "retweets": pd.Int64Dtype(),
          "text": str}



import re
regexUrl = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")

otherRegexUrl = re.compile(r"(?i)https?://\s?\S+")

def main():
    #return binaryTranscribeFirstNLines(TWEETS_FILE_PATH, 10000)
    #return transcribeFirstNLines(TWEETS_FILE_PATH, 100)

    # big 14M tweets parser
    # df = pd.read_csv(TWEETS_FILE_PATH,sep=";", quotechar='"', dtype=dtypes, parse_dates = ["timestamp"], nrows = 1000)

    TWEETS_FILE_PATH = r"C:\Users\Luxor\Documents\Text Mining\bitcoin-tweets\BitcoinTweets.csv"

    print('Reading file')
    df = pd.read_csv(TWEETS_FILE_PATH, sep=",", nrows=1000000)
    print('File read')
    #print( df.head())
    #return
    #
    #a = df[df["text"].str.contains(r"elitetrader.ru", regex=False)]
    a = df
    for i, row in a.iterrows():
        text = row['text']
        if 'http' in text.lower():
            print( 'Before : |{}|'.format(text))
            print( 'After  : |{}|'.format(otherRegexUrl.sub("", text)))
            print('='*30)
    #print( a.head())


    return

    with open(TWEETS_FILE_PATH, mode='r', encoding="utf8") as f:
        for i in range(100):
            a = f.readline()
            print('===== {} ======'.format(i))
            print(a)


a = main()