## FastText

I try 2 models, modifying the cleaning of the cleaning of the dataset.

Predictions go from label 0 meaning negative to label 4 meaning positive

### Usage
My code is find in ./core
Web tutorial project is found in fastText_2

```
python generate_file.py
../fastText_2/fasttext supervised -input ./data/tweets.train -output model_tweet -epoch 30 -lr 0.1
../fastText_2/fasttext test model_tweet.bin ./data/tweets.valid
python predict.py
```
#### V1
It's save in core/model_tweets_2.bin

First model replicates the one found in: https://aboullaite.me/sentiment-analysis-fasttext/

wget https://github.com/facebookresearch/fastText/archive/v0.2.0.zip
(rename to fastText_2)

#### V2
It's save in core/model_tweets_2_v2.bin

Generate file was modify (stacking with 3 length words)

### Model  results
### V1
N       100000
P@1     0.75
R@1     0.75

Same results for same sentences on url, not good results for bitcoin sentences.

```
[('__label__4', 0.9407151341438293, 'Why you should not buy bitcoins'), 
('__label__4', 0.9407151341438293, 'Why you should buy bitcoins'), 
('__label__4', 0.7707151770591736, 'Best time ever to buy bitcoins'), 
('__label__4', 0.659260094165802, "Don't waste your time in bitcoins"), 
('__label__4', 0.8699657917022705, "I don't mind what you do with your money"), 
('__label__4', 0.8356685042381287, 'Bitcoin going up'), 
('__label__0', 0.590138852596283, 'Bitcoin going down'), 
('__label__0', 0.6384021043777466, 'Ugghhh... Not happy at all! sorry'), 
('__label__4', 0.9189409613609314, 'Happyyyyyyy'), 
('__label__4', 0.9994680285453796, 'OH yeah! lets rock.')]
```

### V2

Will try not removing less 3 word characters

N       100000
P@1     0.777
R@1     0.777


```
[('__label__0', 0.8188413977622986, 'why you should not buy bitcoins'), 
('__label__4', 0.6124006509780884, 'why you should buy bitcoins'), 
('__label__4', 0.9473025798797607, 'best time ever buy bitcoins'), 
('__label__0', 0.7407112121582031, 'don waste your time bitcoins'), 
('__label__4', 0.8100113272666931, ' don mind what you with your money'), 
('__label__4', 0.8562479019165039, 'bitcoin going'), 
('__label__0', 0.7147967219352722, 'bitcoin going down'), 
('__label__0', 0.840828001499176, 'ugghhh... not happy all! sorry'), 
('__label__4', 0.9479750394821167, 'happyyyyyyy'), 
('__label__4', 0.999893307685852, ' yeah! lets rock.')]
```

### Predicting bitcoin dataset

Dataset from was used.

Then we stay just with english data. Getting dataset of lines. Saved in ./core/data/bitcoin_data.




fastText folder wa created by pulling: 
git clone https://github.com/facebookresearch/fastText.git
https://fasttext.cc/docs/en/support.html

predicts testing are in predict_2.py

Other models weren't efficient, only use model_tweet_2.bin