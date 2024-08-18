import pandas as pd
import streamlit as st
import pickle
import requests
import os

# Set API key from environment variable
API_KEY = os.getenv('TMDB_API_KEY')

st.title('Movie Recommender System')

def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}')
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except requests.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"

def recommend(movie):
    index = movie_list[movie_list['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    rec_mov = []
    poster = []
    for i in distances[1:6]:
        rec_mov.append(movie_list.iloc[i[0]].title)
        poster.append(fetch_poster(movie_list.iloc[i[0]].movie_id))
    return rec_mov, poster

# Load data
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movie_list = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie selection
selected_movie_name = st.selectbox("Select your movies", movie_list['title'].values)

if st.button('Recommend'):
    names, poster = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])
    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])
