from DataSources import BitcoinHistoricalDataReader, AutoTweetReader
from utils import log, Timer, MultiDate
from textProcessing import SuperCounter, AutoToken, TweetFuncs


class AutoWorkflow(object):

    @classmethod
    def getTweets(cls, filesRead=3):
        with Timer('Reading files', log=log):
            allData = AutoTweetReader(maxFileCount=filesRead, convertDates=False).readAll()

        # filter english tweets only
        fullData = len(allData)
        allData = allData[(allData['language'] == 'en') & (allData['language_proba'] > 0.6)][['date', 'text']]
        engData = len(allData)
        log('englishTweeets : {0:.1%}'.format(engData / fullData))

        # filter repeated tweets
        allData = TweetFuncs.countTweets(allData)
        allData = allData[allData['count'] == 1][['date', 'text']]
        noDupes = len(allData)
        log('after removing dupes: {0:.1%}'.format(noDupes / engData))

        # converting to lower:
        with Timer('toLower'):
            allData['text'] = allData['text'].apply(lambda x: x.lower())

        return allData


def discretize(limit, value):
    if value < -limit: return -1
    if value < limit: return 0
    return 1


def enrichWithPrice(df, dateCol='date', offsets=(1, 2, 3)):
    bcd = BitcoinHistoricalDataReader.read()

    neededDatesData = {MultiDate(date).asDate() for date in set(df[dateCol])}

    datesDict = {date: [MultiDate(date).asDate(offset=offset) for offset in offsets] for date in neededDatesData}

    newCols = {}
    for date, otherDates in datesDict.items():
        priceToday = bcd[bcd['Date'] == date].iloc[0]['Price']
        priceOffsetValues = [(bcd[bcd['Date'] == otherDate].iloc[0]['Price'] / priceToday - 1) for otherDate in
                             otherDates]
        newCols[MultiDate(date).asStr()] = priceOffsetValues

    for i, offsetAmount in enumerate(offsets):
        colName = 'offset_col{}'.format(i)
        df[colName] = df[dateCol].apply(lambda x: newCols[x][i])

    return df

