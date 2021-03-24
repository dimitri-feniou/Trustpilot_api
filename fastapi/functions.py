import re

def remove_spaces(txt: str):
    txt = [item.replace('\n', '') for item in txt]
    txt = [item.replace('                ', '') for item in txt]
    txt = [item.replace('        ', '') for item in txt]
    txt = [item.strip().lower() for item in txt]
    return txt

def remove_emoji(txt:str):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    txt = [emoji_pattern.sub(r'', item) for item in txt]
    return txt