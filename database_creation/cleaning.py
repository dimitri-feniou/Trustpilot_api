import pandas as pd
import string
import nltk
from nltk import word_tokenize
#nltk.download('punkt')
from tqdm.auto import tqdm
tqdm.pandas()
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer, FrenchStemmer
import re

df = pd.read_csv('trustpilot_reviews_tech.csv', index_col=0)
print(df)

df['rating'] = df['rating'].str.split(expand=True)[4]
df['rating'] = df['rating'].str.replace('alt="', '')
df['rating'] = df['rating'].astype('int')
# df['sentiment'] = df['rating'].map({1: 0, 2: 0, 4: 1, 5: 1})
df[['day', 'month', 'year']] = df['date'].str.split(expand=True)[[5, 6, 7]]
df = df.drop(columns='date')
# df = df.dropna(subset=['sentiment'])

# df.to_csv('trustpilot_reviews.csv', index=False)


stop_words = stopwords.words('french')
stemmer = SnowballStemmer('french')


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

def remove_emoji(txt:str) -> str:
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', txt)

# preprocess light
df['review'] = df['review'].progress_apply(remove_spaces) # a effacer
df['review'] = df['review'].progress_apply(remove_emoji) # a effacer
#df = df.drop(columns='Unnamed: 0')
# df = df[['review', 'sentiment']]
# df = df.reset_index(drop=True)
# # df['positif'] = df['sentiment'].map({1: 1, 0: 0})
# # df['negatif'] = df['sentiment'].map({1: 0, 0: 1})
df.to_csv('trustpilot_to_predict.csv', index=False)


def remove_stop_words(txt: list) -> list:
    txt = [x for x in txt if x not in stop_words]
    return txt

def lemmatize(tokens: list) -> list:
    tokens = [stemmer.stem(x) for x in tokens]
    return tokens

def preprocess(txt: str, show_progress: bool=False) -> list:
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
    return lemmas

#df['review'] = df['review'].progress_apply(preprocess)

# preprocess complet
#df.to_csv('trustpilot_fatal.csv')
