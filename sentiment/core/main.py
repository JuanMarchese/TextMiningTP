from etl import TwitterETL
import os 
from pathlib import Path

dir_path = os.path.dirname(os.path.realpath(__file__))

data_path = os.path.join(dir_path, "data")
fasttext_path = os.path.join(Path(dir_path).parent, "fastText/fasttext")
model_path = os.path.join(dir_path, "model_tweet_barbi")
parameters = '-epoch 30 -lr 0.1'

if __name__ == "__main__":
    """
    Filters text with functions.normalizeForTokenization. 
    Generates train and validation files, found in ./data
    Trains fasttext model. 
    """
    my_etl = TwitterETL(basedir=data_path)
    my_etl.run()
    print(f'Training Model for {parameters}')
    os.system(f'{fasttext_path} supervised -input {os.path.join(data_path, "train.csv")} -output {model_path} {parameters}')
    print(f'model_tweet saved in {model_path}')
