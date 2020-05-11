import csv
import re
import os

fname = '/training.1600000.processed.noemoticon.csv'
basedir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(basedir, 'data')

train = open(data_path + '/tweets.train', 'w')
test = open(data_path + '/tweets.valid', 'w')


def apply_cleaner(text):
    # First we lower case the text
    text = row["text"].lower()
    # remove links
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', text)
    # Remove usernames
    text = re.sub('@[^\s]+', '', text)
    # replace hashtags by just words
    text = re.sub(r'#([^\s]+)', r'\1', text)
    # correct all multiple white spaces to a single white space
    text = re.sub('[\s]+', ' ', text)
    # Additional clean up : removing words less than 3 chars, and remove space at the beginning and teh end
    text = re.sub(r'\W*\b\w{1,3}\b', '', text)
    return text

with open(data_path + fname, mode='r', encoding = "ISO-8859-1") as csv_file:
    csv_reader = csv.DictReader(csv_file, fieldnames=['target', 'id', 'date', 'flag', 'user', 'text'])
    line = 0
    for row in csv_reader:
        # Clean the training data
        text = apply_cleaner(row)
        text = text.strip()
        line = line + 1
        # Split data into train and validation
        if line%16 == 0:
            print(f'__label__{row["target"]} {text}', file=test)
        else:
            print(f'__label__{row["target"]} {text}', file=train)
