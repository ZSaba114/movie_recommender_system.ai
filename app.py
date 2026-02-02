import pickle
import streamlit as st
import requests
import base64

# ===== Page config =====
st.set_page_config(page_title="Movie Recommender", layout="wide")

# ===== Fonction pour convertir l'image locale en base64 =====
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ===== Convertir ton image locale bg.png =====
image_base64 = get_base64_of_bin_file("bg.jpg")  # bg.png au même niveau que app.py

# ===== CSS pour style coloré avec image de fond =====
st.markdown(f"""
<style>
/* Image de fond avec overlay semi-transparent pour textes lisibles */
[data-testid="stAppViewContainer"] {{
    background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("data:image/png;base64,{image_base64}");
    background-size: cover;
    background-attachment: fixed;
}}

/* Titre */
h1 {{
    text-align: center;
    color: white;
    text-shadow: 0 0 25px pink;
    font-size: 48px;
    margin-bottom: 40px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}

/* Bouton stylé */
.stButton>button {{
    background-color: #1f77b4;
    color: white;
    font-size: 18px;
    padding: 10px 25px;
    border-radius: 10px;
    font-weight: bold;
    border: none;
    transition: all 0.3s ease;
}}
.stButton>button:hover {{
    background-color: #ff7f0e;
    color: #fff;
}}

/* Cartes des films */
.movie-card {{
    text-align: center;
    padding: 10px;
    border-radius: 15px;
    background: rgba(0,0,0,0.6);
    box-shadow: 0 8px 20px pink;
    transition: transform 0.3s ease;
}}
.movie-card:hover {{
    transform: scale(1.05);
}}

/* Poster des films */
.movie-card img {{
    border-radius: 15px;
    width: 200px;
}}

/* Nom du film */
.movie-card p {{
    font-weight: bold;
    color: #333333;
    margin-top: 8px;
    font-size: 16px;
}}
</style>
""", unsafe_allow_html=True)

# ===== Charger les fichiers pickle =====
movies = pickle.load(open('model/movie_list.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))

# ===== Fonction pour récupérer les posters =====
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return full_path

# ===== Fonction de recommandation =====
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# ===== Interface Streamlit =====
st.title("🍿 Movie Recommender System")

# ===== Label agrandi pour le selectbox =====
st.markdown('<h2 style="text-align:center; font-size:26px; color:white; font-weight:bold;">Type or select a movie from the dropdown</h2>', unsafe_allow_html=True)

# ===== Selectbox sans label =====
selected_movie = st.selectbox("", movies['title'].values)

# ===== Afficher recommandations =====
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    cols = st.columns(5)
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.markdown(f"""
            <div class="movie-card">
                <img src="{poster}" alt="{name}">
                <p>{name}</p>
            </div>
            """, unsafe_allow_html=True)
