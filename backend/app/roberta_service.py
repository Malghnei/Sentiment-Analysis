from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

# Global initialization so it is cached in the warm Lambda execution environment
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_safetensors=True)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, use_safetensors=True)

# Ensure the model is in eval mode for inference
model.eval()

def analyze_roberta(text: str) -> dict:
    """
    Returns sentiment analysis from RoBERTa.
    Outputs usually map to: 0 -> Negative, 1 -> Neutral, 2 -> Positive
    """
    # Truncate to max length for RoBERTa (512 tokens)
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    scores = F.softmax(outputs.logits, dim=1).numpy()[0]
    
    # labels for cardiffnlp/twitter-roberta-base-sentiment-latest:
    # 0 -> negative, 1 -> neutral, 2 -> positive
    labels = ["NEGATIVE", "NEUTRAL", "POSITIVE"]
    
    ranking = torch.argsort(outputs.logits, dim=1, descending=True).numpy()[0]
    
    best_idx = ranking[0]
    best_label = labels[best_idx]
    
    all_scores = {labels[i]: float(scores[i]) for i in range(len(labels))}
    
    # Calculate a pseudo-compound score between -1 and 1 for easy comparison with VADER
    # pos mapping to 1, neg to -1, neutral to 0
    compound = all_scores["POSITIVE"] - all_scores["NEGATIVE"]
    
    return {
        "label": best_label,
        "score": compound, # Scaled ~ [-1, 1]
        "raw_scores": all_scores
    }

def analyze_roberta_batch(texts: list[str]) -> list[dict]:
    """
    Analyzes multiple texts in a single model pass.
    """
    start_time = time.time()
    logger.info(f"Analyzing batch of {len(texts)} texts with RoBERTa")
    
    # Tokenize all texts in the batch
    inputs = tokenizer(texts, padding=True, truncation=True, max_length=512, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    scores_batch = F.softmax(outputs.logits, dim=1).numpy()
    
    labels = ["NEGATIVE", "NEUTRAL", "POSITIVE"]
    results = []
    
    for i in range(len(texts)):
        scores = scores_batch[i]
        best_idx = scores.argmax()
        best_label = labels[best_idx]
        
        all_scores = {labels[j]: float(scores[j]) for j in range(len(labels))}
        compound = all_scores["POSITIVE"] - all_scores["NEGATIVE"]
        
        results.append({
            "label": best_label,
            "score": compound,
            "raw_scores": all_scores
        })
        
    end_time = time.time()
    logger.info(f"Batch analysis took {end_time - start_time:.2f} seconds")
    return results
