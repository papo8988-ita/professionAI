from transformers import AutoTokenizer
from src.train import preprocess_function
import pytest

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

def test_tokenize_sample():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    sample = {"text": ["Hello world!"]}
    out = preprocess_function(sample, tokenizer)
    assert "input_ids" in out