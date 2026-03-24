from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize analyzer once globally to cache it between Lambda invocations
sia = SentimentIntensityAnalyzer()

def analyze_vader(text: str) -> dict:
    """
    Returns polarity scores from VADER:
    {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}
    """
    scores = sia.polarity_scores(text)
    
    # Map to a simple label format for comparative frontend
    compound = scores['compound']
    if compound >= 0.05:
        label = "POSITIVE"
    elif compound <= -0.05:
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"
        
    return {
        "label": label,
        "score": compound,
        "raw_scores": scores
    }
