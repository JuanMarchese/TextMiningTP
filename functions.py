import pandas as pd
import os
import re
import time
import csv
import random
from datetime import timedelta
import numpy as np

# Esta función es para poder asegurarme que el archivo cambió cuando lo importo en google colab
def v():
    print("2020-05-30 11:33")

def loadDatasets(path = "/content/drive/My Drive/Datamining/TextMining/Dataset/"):
    
    file_list = [
        # No vamos a usar la 1ra y la 2da isla
        # 'Tweets_2017-01-01_2017-01-31.csv.gz',
        # 'Tweets_2017-01-31_2017-03-02.csv.gz',
        # 'Tweets_2017-03-02_2017-04-01.csv.gz',
        # 'Tweets_2017-04-01_2017-05-01.csv.gz',
        # 'Tweets_2017-05-01_2017-05-31.csv.gz',
        # 'Tweets_2017-05-31_2017-06-30.csv.gz',
        # 'Tweets_2017-06-30_2017-07-30.csv.gz',
        # 'Tweets_2017-07-30_2017-08-29.csv.gz',
        # 'Tweets_2017-08-29_2017-09-28.csv.gz',
        # 'Tweets_2017-09-28_2017-10-28.csv.gz',
        # 'Tweets_2017-10-28_2017-11-27.csv.gz',
        # 'Tweets_2017-11-27_2017-12-27.csv.gz',
        # 'Tweets_2017-12-27_2018-01-26.csv.gz',
        
        # 'Tweets_2018-01-26_2018-02-25.csv.gz',
        # 'Tweets_2018-02-25_2018-03-27.csv.gz',
        # 'Tweets_2018-07-11_2018-07-15.csv.gz',
        # 'Tweets_2018-07-15_2018-07-19.csv.gz',
        # 'Tweets_2018-07-19_2018-07-23.csv.gz',
        # 'Tweets_2018-07-23_2018-07-27.csv.gz',

        'Tweets_2019-05-10_2019-05-14.csv.gz',
        'Tweets_2019-05-14_2019-05-18.csv.gz',
        'Tweets_2019-05-18_2019-05-22.csv.gz',
        'Tweets_2019-05-22_2019-05-26.csv.gz',
        'Tweets_2019-05-26_2019-05-30.csv.gz',
        'Tweets_2019-05-30_2019-06-03.csv.gz',
        'Tweets_2019-06-03_2019-06-07.csv.gz',
        'Tweets_2019-06-07_2019-06-11.csv.gz',
        'Tweets_2019-06-11_2019-06-15.csv.gz',
        'Tweets_2019-06-15_2019-06-19.csv.gz',
        'Tweets_2019-06-19_2019-06-23.csv.gz',
        'Tweets_2019-06-23_2019-06-27.csv.gz',
        'Tweets_2019-06-27_2019-07-01.csv.gz',
        'Tweets_2019-07-01_2019-07-05.csv.gz',
        'Tweets_2019-07-05_2019-07-09.csv.gz',
        'Tweets_2019-07-09_2019-07-13.csv.gz',
        'Tweets_2019-07-13_2019-07-17.csv.gz',
        'Tweets_2019-07-17_2019-07-21.csv.gz',
        'Tweets_2019-07-21_2019-07-25.csv.gz',
        'Tweets_2019-07-25_2019-07-29.csv.gz',
        'Tweets_2019-07-29_2019-08-02.csv.gz',
        'Tweets_2019-08-02_2019-08-06.csv.gz',
        'Tweets_2019-08-06_2019-08-10.csv.gz',
        'Tweets_2019-08-10_2019-08-14.csv.gz',
        'Tweets_2019-08-14_2019-08-18.csv.gz',
        'Tweets_2019-08-18_2019-08-22.csv.gz',
        'Tweets_2019-08-22_2019-08-26.csv.gz',
        'Tweets_2019-08-26_2019-08-30.csv.gz',
        'Tweets_2019-08-30_2019-09-03.csv.gz',
        'Tweets_2019-09-03_2019-09-07.csv.gz',
        'Tweets_2019-09-07_2019-09-11.csv.gz',
        'Tweets_2019-09-11_2019-09-15.csv.gz',
        'Tweets_2019-09-15_2019-09-19.csv.gz',
        'Tweets_2019-09-19_2019-09-23.csv.gz',
        'Tweets_2019-09-23_2019-09-27.csv.gz',
        'Tweets_2019-09-27_2019-10-01.csv.gz',
        'Tweets_2019-10-01_2019-10-05.csv.gz',
        'Tweets_2019-10-05_2019-10-09.csv.gz',
        'Tweets_2019-10-09_2019-10-13.csv.gz',
        'Tweets_2019-10-13_2019-10-17.csv.gz',
        'Tweets_2019-10-17_2019-10-21.csv.gz',
        'Tweets_2019-10-21_2019-10-25.csv.gz',
        'Tweets_2019-10-25_2019-10-29.csv.gz',
        'Tweets_2019-10-29_2019-11-02.csv.gz',
        'Tweets_2019-11-02_2019-11-06.csv.gz',
        'Tweets_2019-11-06_2019-11-10.csv.gz',
        'Tweets_2019-11-10_2019-11-14.csv.gz',
        'Tweets_2019-11-14_2019-11-18.csv.gz',
        'Tweets_2019-11-18_2019-11-22.csv.gz',
        'Tweets_2019-11-22_2019-11-26.csv.gz'
        ]
    dataframe_list = []

    dtype = {"date": str, 
            "text": str, 
            "language": str, 
            "language_proba": float}

    for file_name in file_list:
        dataframe_list.append(pd.read_csv(os.path.join(path, file_name),
            quotechar='"', encoding = "utf-8", dtype=dtype, quoting=csv.QUOTE_NONNUMERIC, sep=";"))
        #try:
            #dataframe_list.append(pd.read_csv(file_name, quotechar='"', encoding = "utf-8", dtype=dtype, quoting=csv.QUOTE_NONNUMERIC, sep=";"))
            #dataframe_list.append(pd.read_csv(os.path.join(path, file_name), compression = "gzip", engine="c", dtype=dtype))
        #except Exception:
        #    print (file_name)
    
    return pd.concat(dataframe_list, axis=0, ignore_index=True)


def loadSampleDataSetFromSpread(gc, url):
    """
    Carga el sample dataset desde una google spread.
    Antes de usar hay que agregar las siguientes líneas:

    from google.colab import auth
    auth.authenticate_user()
    import gspread
    from oauth2client.client import GoogleCredentials
    # Esta es la variable que tiene que mandarse como primer parámetro
    gc = gspread.authorize(GoogleCredentials.get_application_default())

    """
    wb = gc.open_by_url(url)
    df = pd.DataFrame(wb.worksheets()[0].get_all_values())
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    df.drop(['date', 'month', 'name', 'is_news_spam'], axis = 1, inplace = True)
    df = df[df['is_spam'] != '']
    df['is_news'] = df['is_news'].apply(lambda x: np.NaN if x == '' else x)
    df['sentiment'] = df['sentiment'].apply(lambda x: np.NaN if x == '' else x)
    schema = {
        'text': df['text'].astype(str),
        'is_spam': df['is_spam'].astype(float),
        'is_news': df['is_news'].astype(float),
        'sentiment': df['sentiment'].astype(float)
    }
    df = pd.DataFrame(schema).reset_index(drop = True)
    df['is_spam'] = df['is_spam'].apply(lambda x: True if x == 1.0 else False)
    return df

def getSampleWithNames(dfWithMonth, monthsToSample, sampleSizePerMonth, language = 'en'):
    dfList = []
    names = ['Barbii', 'Juan', 'Mauro', 'Nico', 'Seba']
    tweetsPerNamePerMonth = sampleSizePerMonth / len(names)

    if(tweetsPerNamePerMonth != int(tweetsPerNamePerMonth)):
        raise ValueError(
            'tweetsPerNamePerMonth',
            'Must be an int. Change the sampleSizePerMonth to be divisible by ' + str(len(names)) + '.')

    tweetsPerNamePerMonth = int(tweetsPerNamePerMonth)

    monthNames = []
    for i in range(0, len(names)):
        monthNames = monthNames + ([names[i]] * tweetsPerNamePerMonth)

    for month in monthsToSample:
        df = dfWithMonth[
                    (dfWithMonth['month'] == month) & (dfWithMonth['language'] == language)
                    ].sample(n = sampleSizePerMonth)
        random.shuffle(monthNames)
        df['name'] = monthNames

        dfList.append(df)

    return pd.concat(dfList, axis = 0, ignore_index = True)

def getMonth(date):
    dateparts = date.split('-')
    try:
      return int(dateparts[1])
    except:
      return 0

def addIsSpamColumn(df, countThreshold = 2, languageProbaThreshold = 0.5):
    df_countByText = df.groupby('text').size().reset_index(name = 'count')
    df_countByText["is_spam"] = df_countByText['count'] >= countThreshold
    df_countByText.drop(['count'], axis = 1, inplace = True)
    
    df = df.merge(df_countByText, left_on='text', right_on='text')

    df['is_spam'] = df['is_spam'] | (df['language_proba'] <= languageProbaThreshold)

    return df

def normalizeHashtagsAndMentions(text):
    # Algunos hashtags están separados de la palabra, y lo mismo con los mentions.
    # Aprovechamos también por las dudas para separar el hashtag/mention de la palabra anterior.
    return text.replace("# ", "#").replace("#", " #" ).replace("@ ", "@").replace("@", " @" )

# Guardamos la regex compiladas porque es más rápido para usarlas muchas veces después.
__regexSpace = re.compile(r"\s")
# https://www.geeksforgeeks.org/python-check-url-string/
__regexUrl = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
__regexSimpleUrl = re.compile(r"\shttps?://\S+")
# https://www.regextester.com/95875
__regexHashtagsAndMentions = re.compile(r"\s([@#][\w_-]+)")
__regexHashtags = re.compile(r"\s([#][\w_-]+)")
__regexMentions = re.compile(r"\s([@][\w_-]+)")
__regexMultipleSpaces = re.compile(r"\s+")
__regexMultiplePunctuations = re.compile(r"([\.,:;}{()])\1+")

# Numeros
__regexPriceDollar = re.compile(r'\$(?:\d+[,\.])?(?:\d+[,\.])?\d+[,\.]\d+')
__regexPriceK = re.compile(r'(?:\d+[,\.])?(?:\d+[,\.])?\d+[,\.]\d+k')
__regexFloat = re.compile(r'(?:\d+[,\.])?(?:\d+[,\.])?\d+[,\.]\d+')
__regexFloatStartingWithDot = re.compile(r'\.\d+')
__regexIntegerPriceDollar = re.compile(r'$(?:\d+)?\d+')
__regexIntegerPriceK = re.compile(r'(?:\d+)?\d+k')
__regexInteger = re.compile(r'(?:\d+)?\d+')

def replaceUrls(text, new = ""):
    
    # Algunos textos no tienen ningún espacio (ni \r\t\n\f). Los consideramos basura, porque no vamos a poder
    # clasificar el idoma de todas formas.
    if(not __regexSpace.search(text)):
        return ""

    # Reemplazamos los puntos duplicados por un solo punto (si hay muchos puntos se rompe la regex de búsqueda de urls).
    text = __regexMultiplePunctuations.sub("\1", text)
    text = __regexSimpleUrl.sub(" " + new, text) # Acá reemplazamos por un espacio porque los captura la regex
    return __regexUrl.sub(new, text)

def replaceHashtags(text, new = ""):
    text = normalizeHashtagsAndMentions(text)
    # Reemplazamos los espacios duplicados por un solo espacio.
    text = __regexMultipleSpaces.sub(" ", text)
    return __regexHashtags.sub(new, text)

def replaceMentions(text, new = ""):
    text = normalizeHashtagsAndMentions(text)
    # Reemplazamos los espacios duplicados por un solo espacio.
    text = __regexMultipleSpaces.sub(" ", text)
    return __regexMentions.sub(new, text)

def replaceHashtagsAndMentions(text):
    text = normalizeHashtagsAndMentions(text)
    # Reemplazamos los espacios duplicados por un solo espacio.
    text = __regexMultipleSpaces.sub(" ", text)
    return __regexHashtagsAndMentions.sub("", text)

def replaceUrlsHashtagsAndMentions(text):
    return replaceHashtagsAndMentions(replaceUrls(text))

def normalizeForTokenization(text, normalizeHashtags = True, normalizeNumbers = True):
    text = replaceUrls(text.lower(), new=" <URL> ")
    if (normalizeHashtags):
        text = replaceHashtags(text, new=" <HASHTAG> ")
    text = replaceMentions(text, new=" <MENTION> ")

    if (normalizeNumbers):
        text = __regexPriceDollar.sub(" <PRICE>", text)
        text = __regexPriceK.sub(" <PRICE>", text)
        text = __regexFloat.sub(" <NUMBER> ", text)
        text = __regexFloatStartingWithDot.sub(" <NUMBER> ", text)
        text = __regexIntegerPriceDollar.sub(" <PRICE>", text)
        text = __regexIntegerPriceK.sub(" <PRICE>", text)
        text = __regexInteger.sub(" <NUMBER> ", text)

    return __regexMultipleSpaces.sub(" ", text).strip()