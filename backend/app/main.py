from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel
from typing import List, Union

from app.vader_service import analyze_vader
from app.roberta_service import analyze_roberta_batch, analyze_roberta
import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI(title="Sentiment Analysis API")

# Allowed origins for local development and potential production
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextItem(BaseModel):
    text: str

class TextBatch(BaseModel):
    texts: List[str]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sentiment Analysis API"}

@app.post("/analyze")
def analyze_sentiment(item: Union[TextItem, TextBatch]):
    start_time = time.time()
    # Normalize input to always be a list
    texts = item.texts if isinstance(item, TextBatch) else [item.text]
    logger.info(f"Received request to analyze {len(texts)} texts")
    
    # Filter empty texts
    valid_texts = [t for t in texts if t and t.strip()]
    
    if not valid_texts:
        return {"results": []}

    # Analyze with VADER (lightweight, keep loop)
    vader_results = [analyze_vader(t) for t in valid_texts]
    
    # Analyze with RoBERTa (heavy, use batch function)
    roberta_results = analyze_roberta_batch(valid_texts)
    
    # Collate results
    final_results = []
    for i in range(len(valid_texts)):
        final_results.append({
            "text": valid_texts[i],
            "vader": vader_results[i],
            "roberta": roberta_results[i]
        })
        
    end_time = time.time()
    logger.info(f"Full request processed in {end_time - start_time:.2f} seconds")
    return {"results": final_results}

# Wraps the FastAPI app for execution inside AWS Lambda
handler = Mangum(app)
