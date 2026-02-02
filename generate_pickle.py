import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Créer le dossier 'model' s'il n'existe pas
if not os.path.exists('model'):
    os.makedirs('model')

# 1️⃣ Charger les CSV
movies = pd.read_csv('data/tmdb_5000_movies.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')

# 2️⃣ Fusionner les deux fichiers sur le titre
movies = movies.merge(credits, on='title')

# 3️⃣ Garder seulement les colonnes importantes
# 'id' est l'ID TMDB
movies = movies[['id','title','overview']]
movies.rename(columns={'id':'movie_id'}, inplace=True)

# 4️⃣ Remplir les valeurs manquantes
movies['overview'] = movies['overview'].fillna('')

# 5️⃣ Créer une matrice de similarité basée sur les descriptions
cv = CountVectorizer(stop_words='english')
count_matrix = cv.fit_transform(movies['overview'])
similarity = cosine_similarity(count_matrix)

# 6️⃣ Sauvegarder les fichiers pickle
with open('model/movie_list.pkl', 'wb') as f:
    pickle.dump(movies, f)

with open('model/similarity.pkl', 'wb') as f:
    pickle.dump(similarity, f)

print("✅ movie_list.pkl et similarity.pkl ont été créés dans le dossier 'model'.")
