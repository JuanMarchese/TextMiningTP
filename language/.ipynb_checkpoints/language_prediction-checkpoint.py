import pandas as pd
import numpy as np
import time
from datetime import timedelta


import fasttext

#Source: https://github.com/indix/whatthelang
MODEL_FILE = "lid.176.ftz"

model = fasttext.load_model(MODEL_FILE)

def get_language(text):
    result = ["-",0.0]

    if (type(text) == str):
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