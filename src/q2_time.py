from typing import List, Tuple
from aux_functions import read_tweets_json_pandas, get_emojis_in_content
import pandas as pd
import json

def q2_time(file_path: str) -> List[Tuple[str, int]]:

    content_list = []
    with open(file_path) as json_file:
        for line in json_file:
            json_obj = json.loads(line)
            content_list.append(json_obj['content'])
    
    content = pd.Series(content_list, name='content')
    emojis = content.apply(get_emojis_in_content)
    emojis_clean = emojis.explode().dropna().reset_index(drop=True)

    top10_emojis = emojis_clean.value_counts().head(10)
    result = [(x, y) for x, y in zip(top10_emojis.index, top10_emojis.values)]
    
    return result