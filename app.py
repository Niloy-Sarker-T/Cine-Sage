import pandas as pd
import streamlit as st
import pickle
import requests

st.title('Movie Recommender System ')


def fetch_poster(movie_id):
   response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=98d429f4a3373d037ad2321743a2db8c'.format(movie_id))
   data=response.json()
   return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
def recommend(movie):
    index = movie_list[movie_list['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    rec_mov=[]
    poster=[]
    for i in distances[1:6]:
        rec_mov.append((movie_list.iloc[i[0]].title))
        poster.append(fetch_poster(movie_list.iloc[i[0]].movie_id))
    return rec_mov,poster


movie_dict=pickle.load(open('movie_dict.pkl','rb'))
movie_list= pd.DataFrame(movie_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

selected_movie_name= st.selectbox(
    "Select your movies",
    movie_list['title'].values)


if st.button('Recommend'):
    names,poster=recommend(selected_movie_name)
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

