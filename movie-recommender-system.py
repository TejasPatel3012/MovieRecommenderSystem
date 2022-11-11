import numpy as np
import pandas as pd
import ast

movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')


movies = movies.merge(credits,on='title')

#movies['original_language'].value_counts()

#features
#genres,id or movie_id,keywords,title,overview,cast,crew

movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.head()

movies.isnull().sum()

movies.dropna(inplace=True)

movies.duplicated().sum()

#movies.iloc[0].genres
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])

    return L



#'[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]'

def convert3(obj):
    L = []
    count = 0
    for i in ast.literal_eval(obj):
        if count != 3:
            L.append(i['name'])
            count+=1
        else:
            break
    return L

movies['cast'] = movies['cast'].apply(convert3)

def fetch_director(obj):
    L = []
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

#preprocess fields
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x:x.split())

#remove space from col values
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

#create tags column
movies['tags'] = movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

#create new dataframe
new_df = movies[['movie_id','title','tags']]

#join all tags with space
new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))

#set all tags to lower
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())
