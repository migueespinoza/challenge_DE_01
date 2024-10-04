from typing import List, Tuple
from aux_functions import read_tweets_json_pandas

def q3_time(file_path: str) -> List[Tuple[str, int]]:

    df_tweets = read_tweets_json_pandas(file_path)
    content = df_tweets['content']
    mentioned_users = content.str.findall(('@(\w+)'))
    mentioned_users = mentioned_users.explode().dropna().reset_index(drop=True)
    top10_mentioned_users = mentioned_users.value_counts().head(10)
    
    result = [(x, y) for x, y in zip(top10_mentioned_users.index, top10_mentioned_users.values)]

    return result
