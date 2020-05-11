from textblob import TextBlob

texts =["why you should not buy bitcoins",
        "why you should buy bitcoins",
        "best time ever buy bitcoins",
        "don waste your time bitcoins",
        "don mind what you with your money",
        "bitcoin going down",
        "right time for buying bitcoins",
        "happyyyyyyy",
        "lost all money bitcoins"]

for text in texts:
    blob = TextBlob(text)
    print(text, blob.sentiment, blob.sentiment.polarity)