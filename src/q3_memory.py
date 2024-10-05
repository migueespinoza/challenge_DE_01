from typing import List, Tuple
import json
import re
from itertools import chain
from collections import Counter

def find_mentioned_users(text):
    result = re.findall('@(\w+)', text)
    return result if len(result) > 0 else None

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    
    dict_data = {}
    content_list = []
    with open(file_path) as json_file:
        for line in json_file:
            json_obj = json.loads(line)
            content_list.append(json_obj['content'])

    dict_data['content'] = content_list
    mentioned_users = list(map(find_mentioned_users, dict_data['content']))
    mentioned_users_filtered = filter(lambda x: x is not None, mentioned_users)
    mentioned_users_full = chain.from_iterable(mentioned_users_filtered)
    users_counter = Counter(mentioned_users_full)
    top_10_user_mentioned = sorted(users_counter.items(), key=lambda x: x[1], reverse=True)[:10]
    return top_10_user_mentioned