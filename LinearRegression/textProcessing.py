from utils import Timer
from collections import defaultdict, OrderedDict
import re
from nltk.corpus import stopwords

print('importing text processing...')


class TweetFuncs(object):

    @classmethod
    def countTweets( cls, df, keyCol='text', coutnCol='count'):
        with Timer('Counting repeated tweets'):
            keycolData = df[[keyCol]]
            keycolData[coutnCol] = 1
            grouped = keycolData.groupby(keyCol).sum().reset_index()
            countedTweets = df.merge( grouped, left_on=keyCol, right_on=keyCol, how='left' )

        return countedTweets


class AutoToken(object):


    def __init__(self, trackTokens=False):
        from nltk.tokenize import TweetTokenizer
        self.tweetTokenizer = TweetTokenizer(reduce_len=True)
        self._reMention = re.compile('@\w+')
        self._numbers = frozenset('1,2,3,4,5,6,7,8,9,0'.split(','))
        self.stopWords = self._calculateStopwords()

        self.tokenTracker = defaultdict(set) if trackTokens else None

        self.tokenTransformers = OrderedDict([
            ('<URL>', self._isUrl),
            ('<BTC>', self._isBitcoin),
            ('<ALTCOIN>', self._isAltCoint),
            ('<INT_NUMBER>', self._isIntNumber),
            ('<FLOAT_NUMBER>', self._isFloatNumber),
            ('<MENTION>', self._isMention),
        ])


    def _calculateStopwords(self):
        engStopWords = set( stopwords.words('english') )
        engStopWords.update( ', . : ( ) " | [ ] \' *'.split(' ') )
        return engStopWords

    def __call__(self, tweet):

        for token in self.tweetTokenizer.tokenize(tweet):

            if token in self.stopWords:
                continue

            normlizedToken = self._normalizeToken( token )
            yield normlizedToken


    def _normalizeToken(self, token):

        for tokenType, normalizer in self.tokenTransformers.items():
            if normalizer( token ):

                if self.tokenTracker is not None:
                    self.tokenTracker[tokenType].add( token )

                return tokenType

        return token

    def _isUrl(self, token):
        return token.startswith('http') or token.startswith('www') or '.com' in token

    def _isBitcoin(self, token):
        return token.replace('#', '') in frozenset('btc,bitcoin'.split(','))

    def _isMention(self, token):
        return  self._reMention.match(token)

    def _isAltCoint(self, token):
        return token.replace('#', '') in frozenset('eth,ltc,ethereum,litecoin,altcoin'.split(','))

    def _preProcessNumber(self, token):
        token = token.replace(',', '').replace('#', '')
        if token and token[-1] in {'-', '+'} and token[0] in self._numbers:
            token = token[-1] + token[:-1]

        return token


    def _isFloatNumber(self, token):
        token = self._preProcessNumber(token)
        try:
            _ = float(token)
            return True

        except ValueError:
            pass

        return False

    def _isIntNumber(self, token):
        token = self._preProcessNumber(token)

        try:
            _ = int(token)
            return True

        except ValueError:
            pass

        return False


class SuperCounter(object):

    def __init__(self):
        self.counter = defaultdict(lambda:0)
        self._countToWords=None


    def count(self, token):
        self.counter[token] += 1


    def countToWords(self):
        self._countToWords = defaultdict(set)

        for token,occurance in self.counter.items():
            self._countToWords[occurance].add(token)

        return self._countToWords


    def mostUsed(self, lowFilter=0):
        countToWords = self.countToWords()
        for useCount in sorted( countToWords, reverse=True ):

            if useCount >= lowFilter:

                for token in countToWords[useCount]:
                    yield useCount, token

