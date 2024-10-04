from typing import List, Tuple
from aux_functions import read_tweets_json_pandas, get_emojis_in_content

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    df_tweets = read_tweets_json_pandas(file_path)
    content = df_tweets['content']

    emojis = content.apply(get_emojis_in_content)
    emojis_clean = emojis.explode().dropna().reset_index(drop=True)

    top10_emojis = emojis_clean.value_counts().head(10)
    result = [(x, y) for x, y in zip(top10_emojis.index, top10_emojis.values)]
    
    return result