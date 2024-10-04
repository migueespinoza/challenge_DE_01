import pandas as pd
import emoji

def read_tweets_json_pandas(file_path = "farmers-protest-tweets-2021-2-4.json"):
    df_tweets_full = pd.read_json(file_path, lines = True)
    return df_tweets_full

def get_emojis_in_content(x):
    result =  [x['emoji'] for x in emoji.emoji_list(x)]
    return result if len(result) > 0 else None