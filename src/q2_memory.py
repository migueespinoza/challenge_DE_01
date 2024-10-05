from typing import List, Tuple
import json
from collections import Counter
from itertools import chain
from aux_functions import get_emojis_in_content

def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    
    dict_data = {}
    content_list = []
    with open(file_path) as json_file:
        for line in json_file:
            json_obj = json.loads(line)
            content_list.append(json_obj['content'])

    dict_data['content'] = content_list

    emojis = map(get_emojis_in_content, dict_data['content'])
    emojis_filtered = filter(lambda x: x is not None, emojis)
    emojis_full = chain.from_iterable(emojis_filtered)
    emojis_counter = Counter(emojis_full)
    top_10_emojis = sorted(emojis_counter.items(), key=lambda x: x[1], reverse=True)[:10]

    return top_10_emojis