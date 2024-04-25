from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import json


app = FastAPI()

class model_input(BaseModel):
    name : str

# loading the saved model
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    for i in distances[1:6]:
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names

# recommendation api
@app.post('/recommended')
def diabetes_predd(input_parameters : model_input):
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)
    name = input_dictionary['name']
    recommendatedSystem = recommend(name)
    print(recommendatedSystem)
    return(recommendatedSystem)

# movies name api
@app.get('/movies/name')
def moviesNames():
    movie_list = movies['title'].values
    final_df = movies.reindex(['title'], axis=1)
    return final_df.title

# run using 
# uvicorn RecommendationSystemAPI:app
# https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata