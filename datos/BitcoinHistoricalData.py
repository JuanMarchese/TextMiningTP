import pandas as pd
import datetime
import os.path


class BitcoinHistoricalDataReader:

    SOURCE = r'https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20150419&end=20200519'

    FILENAME = 'Bitcoin Historical Data - Investing.com.csv'

    @classmethod
    def stringDateToDate( cls, strDate ):
        return datetime.datetime.strptime( strDate, "%b %d, %Y")#.date()

    @classmethod
    def strToValues( cls, numAsStr ):
        if numAsStr.endswith('M'): return float( numAsStr[:-1] ) * 1000000
        if numAsStr.endswith('K'): return float( numAsStr[:-1] ) * 1000
        return float( numAsStr )

    @classmethod
    def strToPercentages( cls, precentageStr ):
        return float( precentageStr[:-1] )/100

    @classmethod
    def read( cls, path=r"." ):

        full_path = os.path.join( path, cls.FILENAME )

        df = pd.read_csv(full_path,
                         sep=',',
                         thousands=',',
                         dtype={"Date": str, "Price": float, "Open": float, "High": float, "Low": float, "Vol.": str,
                                "Change %": str})

        df['Date'] = df['Date'].apply( cls.stringDateToDate )
        df['Vol.'] = df['Vol.'].apply( cls.strToValues )
        df['Change %'] = df['Change %'].apply( cls.strToPercentages )

        return df

df = BitcoinHistoricalDataReader.read()

print(df.head())
print(df.dtypes)