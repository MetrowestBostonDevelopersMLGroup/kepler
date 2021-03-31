import pandas as pd
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_data():
    movie_data = pd.read_csv('dataset/movie_data.csv.zip')
    movie_data['original_title'] = movie_data['original_title'].str.lower()
    return movie_data

def combine_data(data):
    data_recommend = data.drop(columns=['movie_id','original_title']) #,'plot'])
    data_recommend = data_recommend[['genres', 'cast', 'title', 'overview']]
    data_recommend['combine'] = data_recommend[data_recommend.columns[0:2]].apply(
                                                                         lambda x: ','.join(x.dropna().astype(str)),axis=1)
    data_recommend = data_recommend.drop(columns=[ 'cast','genres'])
    return data_recommend

def analyze(data_combine):

    # Count Vectorizer assigns a number to the frequency of the word within the corpus
    countVec = CountVectorizer(stop_words='english')
    wordCountMatrix = countVec.fit_transform(data_combine['combine'])
    
    # dump the vectorized list
    # pd.DataFrame(wordCountMatrix.toarray(), columns=countVec.get_feature_names())

    # Term Frequency Inverse Document Frequency gives a 'weight' value indicating the 'orginality' of the word
    tfidfVec = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidfVec.fit_transform(data_combine['overview'])

    # dump the vector list
    #term_vectors.todense()

    # Stack sparse matrices horizontally
    combine_sparse = sp.hstack([wordCountMatrix, tfidf_matrix], format='csr')
    
    # Cosine similarity is a metric used to determine how similar the documents are irrespective of their size.
    # It measures the cosine of the angle between two vectors projected in a multi-dimensional space.
    cosine_sim = cosine_similarity(combine_sparse, combine_sparse)
    
    return cosine_sim

def recommend(title, combine, transform):

    #indices = pd.Series(data.index, index = data['original_title'])
    indices = pd.Series(combine.index, index = combine['title'])
    index = indices[title]

    sim_scores = list(enumerate(transform[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    
    movie_indices = [i[0] for i in sim_scores]

    #combine.columns
    #Index(['genres', 'cast', 'title', 'overview', 'combine'], dtype='object')

    movie_id = combine['movie_id'].iloc[movie_indices]
    movie_title = combine['title'].iloc[movie_indices]
    movie_genres = combine['genres'].iloc[movie_indices]

    recommendation_data = pd.DataFrame(columns=['Movie_Id','Name','Genres'])

    recommendation_data['Movie_Id'] = movie_id
    recommendation_data['Name'] = movie_title
    recommendation_data['Genres'] = movie_genres

    return recommendation_data

def recommend2(movie_name, session):
    movie_name = movie_name.lower()
    
    find_movie = get_data()
    combine_result = combine_data(find_movie)
    transform_result = transform_data(combine_result,find_movie)
    
    if movie_name not in find_movie['original_title'].unique():
        return 'Movie not in Database'
    
    else:
        recommendations = recommend_movies(movie_name, find_movie, combine_result, transform_result)
        return recommendations.to_dict('records')

