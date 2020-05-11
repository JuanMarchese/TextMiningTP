import csv
import os

from utils.utils import apply_cleaner

fname = '/tweets_en.csv'
basedir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(basedir, 'data', 'bitcoin_data')

tweets_rf = open(data_path + '/tweets_en_rf.csv', 'w')

with open(data_path + fname, mode='r', encoding = "ISO-8859-1") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line = 0
    for row in csv_reader:
        # Clean the training data
        text = row['text']
        text = apply_cleaner(text)
        text = text.strip()
        line = line + 1
        # Split data into train and validation
        print(text, file=tweets_rf)
