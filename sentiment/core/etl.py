import csv
import os
import sys
from functions import functions


class TwitterETL:

    FNAME = "training.1600000.processed.noemoticon.csv"
    INPUT_ENCODING = "ISO-8859-1"
    OUTPUT_ENCODING = "utf8"
    FIELDNAMES = ['target', 'id', 'date', 'flag', 'user', 'text']
    TEST_P = 0.10
    TRAIN_FNAME = "train"
    VALID_FNAME = "validation"

    def __init__(self, basedir: str):
        self.basedir = basedir

    def get_data(self):
        f = open(os.path.join(self.basedir,
                              self.FNAME),
                  mode='r',
                  encoding=self.INPUT_ENCODING)
        csv_reader = csv.DictReader(f, fieldnames=self.FIELDNAMES)
        return csv_reader

    @staticmethod
    def preprocess_etl(line: str) -> str:
        target, text = line["target"], line["text"]
        text = functions.preprocess_barbi(text)
        # Fast Text expected format
        text = "__label__{} {}".format(eval(target), text)
        return text

    def outputs(self, n_line: int, train_file, valid_file) -> str:
        # Decides if line will be stored in train or validation set
        if n_line % (self.TEST_P*100) == 0:
            return valid_file
        return train_file

    def write_file(self, file, content):
        # For use inside the loop
        content = content + '\n'
        file.write(content)

    def open_file(self, fname: str):
        fpath = os.path.join(self.basedir, fname)
        file = open(fpath + '.csv', 'w+', encoding=self.OUTPUT_ENCODING)
        return file

    def run(self):
        lines = self.get_data()
        train_file = self.open_file(self.TRAIN_FNAME)
        valid_file = self.open_file(self.VALID_FNAME)

        print('Creating ETL Train and Valid Files')

        for i, line in enumerate(lines):
            if i % 100000 == 0:
                print(i)
            parsed_text = self.preprocess_etl(line)
            file = self.outputs(i, train_file, valid_file)
            self.write_file(file, parsed_text)

        train_file.close()
        valid_file.close()
        
        print(f'Files {self.TRAIN_FNAME}, {self.VALID_FNAME} in {self.basedir}')
