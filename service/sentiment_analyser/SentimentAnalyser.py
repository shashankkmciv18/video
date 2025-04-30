from service.Logger import CentralizedLogger
from textblob import TextBlob

# logger = CentralizedLogger.get_logger()


def do_sentiment_analysis(quote):
    # Check if the quote is positive
    sentiment = TextBlob(quote).sentiment
    return True
    # if sentiment.polarity > 0:
    #     return True
    # else:
    #     print("Quote rejected due to low sentiment polarity.")
    #     print("Quote: %s, Sentiment Polarity: %s", quote, sentiment.polarity)
    #     # logger.warning("Quote rejected due to low sentiment polarity.")
    #     # logger.error("Quote: %s, Sentiment Polarity: %s", quote, sentiment.polarity)
    #     return False
