from typing import List, Tuple
from aux_functions import read_tweets_json_pandas
import pandas as pd
import json

def q3_time(file_path: str) -> List[Tuple[str, int]]:

    content_list = []
    with open(file_path) as json_file:
        for line in json_file:
            json_obj = json.loads(line)
            content_list.append(json_obj['content'])

    content = pd.Series(content_list, name='content')
    mentioned_users = content.str.findall(('@(\w+)'))
    mentioned_users = mentioned_users.explode().dropna().reset_index(drop=True)
    top10_mentioned_users = mentioned_users.value_counts().head(10)
    
    result = [(x, y) for x, y in zip(top10_mentioned_users.index, top10_mentioned_users.values)]

    return result
