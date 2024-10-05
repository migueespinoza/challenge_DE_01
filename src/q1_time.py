from typing import List, Tuple
from datetime import datetime
import pandas as pd
import json

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:

    dict_data = {}
    ids = []
    dates = []
    usernames = []
    with open(file_path) as json_file:
        for line in json_file:
            json_obj = json.loads(line)
            ids.append(json_obj['id'])
            dates.append(json_obj['date'])
            usernames.append(json_obj['user']['username'])

    dict_data['id'] = ids
    dict_data['username'] = usernames
    dict_data['date'] = dates
    df_tweets_full = pd.DataFrame(dict_data)
    df_tweets_full['date_only'] = pd.to_datetime(df_tweets_full['date'], format='%Y-%m-%dT%H:%M:%S%z').dt.date

    cantidad_id_por_fecha = df_tweets_full.groupby('date_only')['id'].count().reset_index()
    top10_fechas = cantidad_id_por_fecha.rename(columns={'id':'count'}).sort_values(by='count', ascending=False).head(10)
    top_fechas = top10_fechas['date_only'].to_list()

    df_tweets_top_fechas = df_tweets_full[df_tweets_full['date_only'].isin(top_fechas)]

    cantidad_tweets_por_fecha_y_user = df_tweets_top_fechas.groupby(by=['date_only', 'username'], sort=False)['id'].count().reset_index().\
        rename(columns={'id': 'count'})
    
    mayor_cantidad_tweets_de_un_usuario_por_fecha = cantidad_tweets_por_fecha_y_user.\
        groupby(by=['date_only'], sort=False)['count'].agg(['max', 'sum']).reset_index()
    
    join_dfs = cantidad_tweets_por_fecha_y_user.merge(mayor_cantidad_tweets_de_un_usuario_por_fecha, on='date_only', how='inner')
    usuario_max_tweets_por_fecha = join_dfs[join_dfs['count'] == join_dfs['max']].reset_index(drop=True).sort_values(by='sum', ascending=False)

    lista_usuario_max_tweets_por_fecha = [(x, y) for x, y in usuario_max_tweets_por_fecha[['date_only', 'username']].values]
    return lista_usuario_max_tweets_por_fecha


if __name__ == '__main__':
    file_path = "farmers-protest-tweets-2021-2-4.json"
    result = q1_time(file_path)
    print(result)