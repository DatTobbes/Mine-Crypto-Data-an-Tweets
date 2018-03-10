from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer():

    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_tweet(self, tweet):
        return self.analyzer.polarity_scores(tweet)