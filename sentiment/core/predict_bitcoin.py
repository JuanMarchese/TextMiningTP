import csv
import json
import os
import sys
sys.path.append("..")
from fastText.python.fasttext_module.fasttext.FastText import load_model
#from fastText_2.fastText import load_mod

from utils.utils import apply_cleaner, reformat_pred

fname = '/tweets_en_rf.csv'
basedir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(basedir, 'data', 'bitcoin_data')

tweets_pred = open(data_path + '/tweets_en_pred.csv', 'w')
classifier = load_model("model_tweet_2_v2.bin")


with open(data_path + fname, mode='r', encoding = "ISO-8859-1" ) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\n')
    line = 0
    bad_line = 0
    for row in csv_reader:
        line = line + 1
        #
        # Clean the training data
        try:
            pred = classifier.predict(row)
            pred = reformat_pred(pred, row)
            pred = [*pred]
            # Split data into train and validation
            print(pred, file=tweets_pred)
        except:
            bad_line += 1
            pass

print(line)
print(bad_line)
