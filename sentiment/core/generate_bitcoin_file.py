import os

import fasttext
import pandas as pd

MODEL_FILE = "lid.176.ftz"
model = fasttext.load_model(MODEL_FILE)

basedir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(basedir, 'data', 'bitcoin_data')
fname = '/tweets.csv'

parse_dates = ["timestamp"]

dtypes = {"id": str,
          "user": str,
          "fullname": str,
          "url": str,
          "timestamp": str,
          "replies": pd.Int64Dtype(),
          "retweets": pd.Int64Dtype(),
          "text": str}

data = pd.read_csv(data_path + fname, sep=";", quotechar='"', dtype=dtypes, parse_dates = parse_dates, nrows = 1000000)
data["text"] = data["text"].str.replace("\n", " ")

def get_language(text):
    result = ["-", 0.0]

    if (type(text) == str):
        if (len(text) > 10):
            prediction = model.predict(text)
            if len(prediction) > 0:
                result[0] = prediction[0][0].replace("__label__","")
                result[1] = prediction[1][0]
    return result

language_and_proba = data["text"].apply(get_language)
data["language"] = [x[0] for x in language_and_proba]
data["language_proba"] = [x[1] for x in language_and_proba]
print('Original len data: ', len(data))
data = data[data["language"] == 'en']
print('English len data: ', len(data))

data.to_csv(data_path + "/tweets_en.csv", index=False)
print(data_path + "/tweets_en.csv")
