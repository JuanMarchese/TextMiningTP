import pandas as pd
import numpy as np
import time
from datetime import timedelta

import re

import fasttext


# Guardamos la regex compiladas porque es más rápido para usarlas muchas veces después.
__regexSpace = re.compile(r"\s")
# https://www.geeksforgeeks.org/python-check-url-string/
__regexUrl = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
__regexSimpleUrl = re.compile(r"\shttps?://\S+")
# https://www.regextester.com/95875
__regexHashtagsAndMentions = re.compile(r"\s([@#][\w_-]+)")
__regexMultipleSpaces = re.compile(r"\s+")
__regexMultiplePunctuations = re.compile(r"[\.,:;}{()]+")

def replaceUrls(text):
    
    # Algunos textos no tienen ningún espacio (ni \r\t\n\f). Los consideramos basura, porque no vamos a poder
    # clasificar el idoma de todas formas.
    if(not __regexSpace.search(text)):
        return ""

    # Reemplazamos los puntos duplicados por un solo punto (si hay muchos puntos se rompe la regex de búsqueda de urls).
    text = __regexMultiplePunctuations.sub(".", text)
    text = __regexSimpleUrl.sub(" ", text) # Acá reemplazamos por un espacio porque los captura la regex
    return __regexUrl.sub("", text)

def replaceHashtagsAndMentions(text):
    # Algunos hashtags están separados de la palabra, y lo mismo con los mentions.
    # Aprovechamos también por las dudas para separar el hashtag/mention de la palabra anterior.
    text = text.replace("# ", "#").replace("#", " #" ).replace("@ ", "@").replace("@", " @" )
    # Reemplazamos los espacios duplicados por un solo espacio.
    text = __regexMultipleSpaces.sub(" ", text)
    return __regexHashtagsAndMentions.sub("", text)

def replaceUrlsHashtagsAndMentions(text):
    return replaceHashtagsAndMentions(replaceUrls(text))


#Source: https://github.com/indix/whatthelang
MODEL_FILE = "lid.176.ftz"

model = fasttext.load_model(MODEL_FILE)

def get_language(text):
    result = ["-",0.0]

    if (type(text) == str):
        # Para obtener el idioma sin eliminar las urls, los hashtags y los mentions, comentar la siguiente línea.
        text = replaceUrlsHashtagsAndMentions(text)
        if (len(text) > 10):
            prediction = model.predict(text)
            if len(prediction) > 0:
                result[0] = prediction[0][0].replace("__label__","")
                result[1] = prediction[1][0]


    return result

tweets = pd.read_csv("../../../RawData/BitcoinTweets.csv", engine="c", nrows=1000)
print(tweets.head())
start = time.time()

language_and_proba = tweets["text"].apply(get_language)
tweets["language"] = [x[0] for x in language_and_proba]
tweets["language_proba"] = [x[1] for x in language_and_proba]

end = time.time()

print("Time elapsed: " + str(end - start) + " seconds")

tweets.to_csv("./BitcoinTweets_lang.csv")

print(tweets.head())

print("Finish!")