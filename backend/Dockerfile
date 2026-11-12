# API image: CPU-only PyTorch, models baked in, served on 7860
FROM python:3.12-slim

# Run as an unprivileged user
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

COPY --chown=user requirements.txt .
# CPU-only torch first: much smaller than the default CUDA build
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r requirements.txt

# Bake models into the image so startup doesn't download them (~/nltk_data and ~/.cache/huggingface)
RUN python -m nltk.downloader vader_lexicon \
 && python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification as M; \
n='cardiffnlp/twitter-roberta-base-sentiment-latest'; AutoTokenizer.from_pretrained(n); M.from_pretrained(n, use_safetensors=True)"

COPY --chown=user app/ app/

EXPOSE 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
