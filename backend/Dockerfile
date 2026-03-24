FROM public.ecr.aws/lambda/python:3.10

# Copy requirements file
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install PyTorch CPU first to save space, then other requirements
# Using the CPU-only package reduces the image size drastically, which is ideal for Lambda.
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

# Download NLTK vader_lexicon data into a globally readable location
ENV NLTK_DATA=/opt/nltk_data
RUN python -m nltk.downloader -d /opt/nltk_data vader_lexicon

# Download HuggingFace model during build to cache it in the container image
# This prevents downloading it during cold starts.
ENV HOME=/tmp
ENV HF_HOME=/tmp/huggingface
ENV TRANSFORMERS_CACHE=/tmp/huggingface
RUN mkdir -p /tmp/huggingface && chmod 777 /tmp/huggingface
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
    AutoTokenizer.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment-latest'); \
    AutoModelForSequenceClassification.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment-latest', use_safetensors=True)"

# Copy function code
COPY app/ ${LAMBDA_TASK_ROOT}/app/

# Set the CMD to the Mangum handler
CMD [ "app.main.handler" ]
