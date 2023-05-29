# import libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# load the data
data = pd.read_csv(r"D:\security\tmdb_movies_data.csv", skipinitialspace=True)

# preprocess the data
data['overview'] = data['overview'].fillna('')
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['overview'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# define function to get movie recommendations
def get_recommendations(user_input, indices, cosine_sim, data):
    idx = indices[user_input]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return data['original_title'].iloc[movie_indices]

# get user input from terminal
user_input = input('What movie are you in the mood for? ')

# find closest match to user input
matches = data['original_title'].apply(lambda x: x.lower()).str.contains(user_input.lower())
if matches.sum() == 0:
    print('Sorry, no matches found.')
else:
   # get index of closest match
    idx = matches.idxmax()
    
    # get recommendations based on closest match
    indices = pd.Series(data.index, index=data['original_title'])
    recommendations = get_recommendations(idx, indices, cosine_sim, data)
    print(recommendations)