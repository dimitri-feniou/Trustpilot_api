import torch

from transformers import CamembertModel, CamembertTokenizer, CamembertForSequenceClassification, pipeline, AdamW
from keras.preprocessing.sequence import pad_sequences
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler

from tqdm import tqdm, trange
import pandas as pd
import numpy as np

camembert = torch.hub.load('pytorch/fairseq', 'camembert')

camembert = CamembertForSequenceClassification.from_pretrained(
    "camembert-base", num_labels=2)
tokenizer = CamembertTokenizer.from_pretrained("camembert-base")

model_path = "/home/dimitri/Documents/code/python/NLP_trustpilot/fastapi/camembert_sentiment_anal.pt"

camembert.load_state_dict(torch.load(
    model_path, map_location=torch.device('cpu')), strict=False)
camembert.eval()

MAX_LEN = 128
batch_size = 16


def tokenize(txt: str):
    tokenized_reviews = [tokenizer.encode(txt, add_special_tokens=True, truncation=True, max_length=MAX_LEN)
                         for txt in txt]
    tokenized_reviews = pad_sequences(
        tokenized_reviews, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")

    attention_masks = []
    for seq in tokenized_reviews:
        seq_mask = [float(i > 0) for i in seq]
        attention_masks.append(seq_mask)
    prediction_inputs = torch.tensor(tokenized_reviews)
    prediction_masks = torch.tensor(attention_masks)


# Apply the finetuned model (Camembert)
flat_pred = []
with torch.no_grad():
    # Forward pass, calculate logit predictions
    outputs = camembert(prediction_inputs.to(
        device), token_type_ids=None, attention_mask=prediction_masks.to(device))
    logits = outputs[0]
    logits = logits.detach().cpu().numpy()
    flat_pred.extend(np.argmax(logits, axis=1).flatten())
