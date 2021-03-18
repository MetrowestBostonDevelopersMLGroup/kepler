
import pandas as pd
import os
#import matplotlib.pyplot as plt
#import seaborn as sns
import json

def load_data():
    
    print(os.getcwd())
    data_movies = pd.read_csv('./dataset/tmdb_5000_movies.csv',na_filter=False)
    data_credits = pd.read_csv('./dataset/tmdb_5000_credits.csv')

    data_credits = data_credits[['movie_id','title','cast','crew']]
    data_movies = data_movies.rename(columns = {'id':'movie_id'})
    data_movies = data_movies.merge(data_credits,on='movie_id')

    
    data_movies = data_movies.drop(columns=['tagline', 'status', 'homepage', 
                                        'keywords','crew','vote_count', 'vote_average',
                                       'tagline', 'spoken_languages', 'runtime',
                                       'popularity', 'production_companies', 'budget',
                                       'production_countries', 'release_date', 'revenue',
                                        'title_y', 'original_language'])
    data_movies = data_movies.rename(columns = {'title_x':'title'})

    data_movies['cast'] = data_movies['cast'].apply(get_list)
    data_movies['genres'] = data_movies['genres'].apply(get_list)

    data_recommend = data_movies.drop(columns=['movie_id','original_title']) #,'plot'])
    data_recommend = data_recommend[['genres', 'cast', 'title', 'overview']]

    #data_recommend = data_movies.drop(columns=['movie_id', 'original_title','plot'])
    data_recommend['combine'] = data_recommend[data_recommend.columns[0:2]].apply(lambda x: ','.join(x.dropna().astype(str)),axis=1)
    data_recommend = data_recommend.drop(columns=[ 'cast','genres'])

    return data_recommend

def get_list(meta_data):
    
    try:
        if isinstance(meta_data, str):        
            parsed_json = json.loads(meta_data)
            parsed_json = parsed_json[:3]
            result = []
            for item in parsed_json:
                result.append(item['name'])
            return result
    except Exception:
        return []
    return []

def describe_data():
    return "done!"