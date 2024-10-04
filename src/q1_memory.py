from typing import List, Tuple
from datetime import datetime
import polars as pl
import json

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    dict_data = {}
    ids = []
    dates = []
    usernames = []
    with open(file_path) as json_file:
        for line in json_file.readlines():
            json_obj = json.loads(line)
            ids.append(json_obj['id'])
            dates.append(json_obj['date'])
            usernames.append(json_obj['user']['username'])

    dict_data['id'] = ids
    dict_data['username'] = usernames
    dict_data['date'] = dates
    pl_data = pl.DataFrame(dict_data)
    del dict_data, ids, usernames, dates

    pl_data = pl_data.with_columns(pl.col('date').str.to_date('%Y-%m-%dT%H:%M:%S%:z').dt.date().alias('date_only')).\
        drop('date')

    top_10_fechas_count = pl_data.group_by('date_only').\
        agg(pl.count('id').alias('count')).\
        sort(by='count', descending=True).\
        head(10)
    top_10_fechas = top_10_fechas_count.get_column('date_only').to_list()

    pl_tweets_top10 = pl_data.filter(pl.col('date_only').is_in(top_10_fechas))
    top_users_in_top10_dates = pl_tweets_top10.with_columns(pl.count('id').over(['date_only', 'username']).alias('count_tweets_per_user_by_date'),
        ).\
        with_columns(
            pl.max('count_tweets_per_user_by_date').over('date_only').alias('max_tweets_per_user_by_date'), 
            pl.count('id').over('date_only').alias('count_id_by_date'), 
        ).\
        filter(pl.col('count_tweets_per_user_by_date')==pl.col('max_tweets_per_user_by_date')).\
        select('date_only', 'username', 'count_id_by_date').\
        unique().\
        sort(by='count_id_by_date', descending=True).\
        drop('count_id_by_date')
    
    result = top_users_in_top10_dates.rows()

    return result

if __name__ == '__main__':
    file_path = "farmers-protest-tweets-2021-2-4.json"
    result = q1_memory(file_path)
    print(result)