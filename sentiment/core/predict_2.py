import sys
import numpy as np
sys.path.append("..")
from pprint import pprint
from fastText.python.fasttext_module.fasttext.FastText import load_model
#from fastText_2.fastText import load_mod

from utils.utils import apply_cleaner, reformat_pred

classifier = load_model("model_tweet_2_v2.bin")

texts =["Why you should not buy bitcoins",
         "Why you should buy bitcoins",
         "Best time ever to buy bitcoins",
         "Don't waste your time in bitcoins",
         "I don't mind what you do with your money",
         "Bitcoin going up",
         "Bitcoin going down",
         "Right time for buying bitcoins",
         "Happyyyyyyy",
         "I lost all my money on bitcoins"]

texts = [apply_cleaner(text) for text in texts]

pred = classifier.predict(texts)

ref = reformat_pred(pred, texts)

print([*ref])

"""
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
"""

# Works as url sample, but not good for other sentences (just applying cleaner)

"""
[('__label__4', 0.9407151341438293, 'why you should not buy bitcoins'),
 ('__label__4', 0.9407151341438293, 'why you should buy bitcoins'), 
 ('__label__4', 0.9325990080833435, 'best time ever buy bitcoins'), 
 ('__label__4', 0.659260094165802, 'don waste your time bitcoins'), 
 ('__label__4', 0.8699657917022705, ' don mind what you with your money'), 
 ('__label__4', 0.8356685042381287, 'bitcoin going'), 
 ('__label__0', 0.590138852596283, 'bitcoin going down'), 
 ('__label__0', 0.7686778903007507, 'ugghhh... not happy all! sorry'), 
 ('__label__4', 0.9189409613609314, 'happyyyyyyy'), 
 ('__label__4', 0.9994680285453796, ' yeah! lets rock.')]
"""

# Works better!!!! (just applying cleaner and v2 model)

"""
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
"""