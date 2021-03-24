import torch

from transformers import CamembertModel, CamembertTokenizer, CamembertForSequenceClassification, pipeline, AdamW
from keras.preprocessing.sequence import pad_sequences
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler

from tqdm import tqdm, trange
import pandas as pd
import numpy as np

camembert = torch.hub.load('pytorch/fairseq', 'camembert')

camembert = CamembertForSequenceClassification.from_pretrained("camembert-base", num_labels=2)
tokenizer = CamembertTokenizer.from_pretrained("camembert-base")

model_path = "/home/terence/PycharmProjects/truspilot_api/camembert_sentiment_anal.pt"

camembert.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')), strict=False)
camembert.eval()

MAX_LEN = 128
batch_size = 16

def tokenize(txt:str):
    tokenized_reviews = [tokenizer.encode(txt, add_special_tokens=True, truncation=True, max_length=MAX_LEN)
                              for txt in txt]
    tokenized_reviews = pad_sequences(tokenized_reviews, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")
    return tokenized_reviews
