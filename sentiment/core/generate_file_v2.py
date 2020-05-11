import csv
import os

from utils.utils import apply_cleaner

fname = '/training.1600000.processed.noemoticon.csv'
basedir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(basedir, 'data')

train = open(data_path + '/tweets.train_2', 'w')
test = open(data_path + '/tweets.valid_2', 'w')

with open(data_path + fname, mode='r', encoding = "ISO-8859-1") as csv_file:
    csv_reader = csv.DictReader(csv_file, fieldnames=['target', 'id', 'date', 'flag', 'user', 'text'])
    line = 0
    for row in csv_reader:
        # Clean the training data
        text = row["text"]
        text = apply_cleaner(row)
        text = text.strip()
        line = line + 1
        # Split data into train and validation
        if line%16 == 0:
            print(f'__label__{row["target"]} {text}', file=test)
        else:
            print(f'__label__{row["target"]} {text}', file=train)