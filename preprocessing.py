import emoji
from json.decoder import JSONDecodeError
import re
from nltk.stem.snowball import SnowballStemmer, FrenchStemmer
from nltk.corpus import stopwords
from os import remove
import pandas as pd
import string
import nltk
from nltk import word_tokenize
from starlette.responses import JSONResponse
# nltk.download('punkt')
from tqdm.auto import tqdm
tqdm.pandas()
# nltk.download('stopwords')

df = pd.read_csv(
    '/home/dimitri/Documents/code/python/NLP_trustpilot/csv_test/trustpilot_reviews.csv', index_col=0)
print(df)

df = pd.DataFrame({'dates': date, 'review': reviews, 'rating': ratings})

df['rating'] = df['rating'].str.split(expand=True)[4]
df['rating'] = df['rating'].str.replace('alt="', '')
df[['day', 'month', 'year']] = df['date'].str.split(expand=True)[[5, 6, 7]]
df = df.drop(columns=['day', 'month', 'year'])




def remove_spaces(txt: str) -> str:
    txt = txt.replace('\n', '')
    txt = txt.replace('                ', '')
    txt = txt.replace('        ', '')
    txt = txt.strip().lower()
    return txt


def remove_punctuations_digits(txt: str) -> str:
    for punctuation in string.punctuation:
        txt = txt.replace(punctuation, ' ')
    for digit in string.digits:
        txt = txt.replace(digit, ' ')
    return txt


def remove_stop_words(txt: list) -> list:
    txt = [x for x in txt if x not in stop_words]
    return txt


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def lemmatize(tokens: list) -> list:
    tokens = [stemmer.stem(x) for x in tokens]
    return tokens


def preprocess(txt: str, show_progress: bool = False) -> list:
    if show_progress:
        print("Original text :")
        print(txt, '\n')


spaces_removed = remove_spaces(txt)
if show_progress:
    print("Cleaned text :")
    print(txt, '\n')

cleaned_txt = remove_punctuations_digits(spaces_removed)
if show_progress:
    print("Cleaned text :")
    print(cleaned_txt, '\n')

text_without_emoji = remove_emoji(cleaned_txt)
if show_progress:
    print("Cleaned text :")
    print(cleaned_txt, '\n')

tokens = word_tokenize(text_without_emoji)
if show_progress:
    print("Tokenized text :")
    print(tokens, '\n')

filtered_tokens = remove_stop_words(tokens)
if show_progress:
    print("Tokenized text :")
    print(tokens, '\n')

lemmas = lemmatize(filtered_tokens)
if show_progress:
    print("Lemmatized text :")
    print(lemmas, '\n')


df['review'] = df['review'].apply(remove_emojis)


df.to_csv('trustpilot_reviews_final.csv')