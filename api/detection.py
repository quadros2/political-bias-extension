import torch
import torch.nn as nn
import torch.nn.functional as F

from transformers import AutoTokenizer, AutoModelForSequenceClassification

def get_tokenizer(model_name):
    return AutoTokenizer.from_pretrained(model_name)

def get_model(model_name, device="cuda"):
    if "cuda" in device: assert torch.cuda.is_available() 
    return AutoModelForSequenceClassification.from_pretrained(model_name).to(device)

def detect_bias(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)

    return F.softmax(outputs.logits, dim=0).detach().tolist()