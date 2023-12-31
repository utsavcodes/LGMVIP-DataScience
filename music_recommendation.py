# -*- coding: utf-8 -*-
"""Copy of Music_Recommendation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HnhMkoMYh1CDh4HCNY5O2CX9TNAxVhYp
"""

import pandas as pd
import numpy as np

import pandas as pd

# Read the dataset into a pandas DataFrame
df = pd.read_json('/content/sample_data/amazon_metadata_MuMu.json', lines=True)

# Print the first few rows of the DataFrame
print(df.head())

import pandas as pd

# Define the chunk size (in number of lines)
chunk_size = 10000

# Initialize an empty list to hold the chunks
chunks = []

# Open the file and read it in chunks
with open('/content/amazon_metadata_MuMu.json') as f:
    for chunk in pd.read_json(f, lines=True, chunksize=chunk_size):
        chunks.append(chunk)

# Concatenate the chunks into a single DataFrame
df = pd.concat(chunks, ignore_index=True)

# Print the first few rows of the DataFrame
print(df.head())

import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load dataset
with open('/content/amazon_metadata_MuMu.json') as f:
    data = [json.loads(line) for line in f]
songs_df = pd.DataFrame(data)

# Preprocess data
songs_df['tags'] = songs_df['tags'].fillna('')
songs_df['search_history'] = songs_df['search_history'].fillna('')
songs_df['text'] = songs_df['tags'] + ' ' + songs_df['search_history']

# Vectorize the text data
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(songs_df['text'])

# Compute the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Define the function to recommend songs
def recommend_songs(tags, search_history, cosine_sim=cosine_sim, df=songs_df):
    # Create a dataframe with relevant songs
    relevant_songs = df[(df['tags'].str.contains(tags)) & (df['search_history'].str.contains(search_history))]

    # Get the indices of relevant songs
    indices = pd.Series(relevant_songs.index)

    # Compute the similarity scores
    sim_scores = list(enumerate(cosine_sim[indices]))

    # Sort the songs based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices of the top 10 songs
    song_indices = [i[0] for i in sim_scores[:10]]

    # Return the top 10 songs
    return df.iloc[song_indices]['title']

# Test the function
recommendations = recommend_songs('pop', 'Ariana Grande')
print(recommendations)

# Commented out IPython magic to ensure Python compatibility.
import os
import numpy as np
import pandas as pd

import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
# %matplotlib inline

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.metrics import euclidean_distances
from scipy.spatial.distance import cdist
from collections import defaultdict
import difflib

import warnings
warnings.filterwarnings("ignore")

! gdown --id 1RlP8YUaYVaVDyWC1XNw0xhpGt1I7MdjS
! gdown --id 1QTact3Y2tGnpJqTWLDdEWZgG6nVVwL0y
! gdown --id 1BBrCInmMABIpwH1ksQo_a9TnqyStMQpT
! gdown --id 1YG8oeoheZNoud0d1SpyDH19WXmKMeU2N
! gdown --id 1KpZAraMRZDXrl0RrZSo6_MulKbvDxfyq

data = pd.read_csv("/content/data.csv")
genre_data = pd.read_csv('/content/data_by_genres.csv')
year_data = pd.read_csv('/content/data_by_year.csv')
artist_data = pd.read_csv('/content/data_by_artist.csv')

data.head(10)

data['decade'] = data['year'].apply(lambda year : f'{(year//10)*10}s')

sns.countplot(data['decade'],)

sound_features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'valence']
fig = px.line(year_data, x='year', y=sound_features,title='Trend of various sound features over decades')
fig.show()

fig = px.line(year_data, x='year', y='loudness',title='Trend of loudness over decades')
fig.show()

top10_genres = genre_data.nlargest(10, 'popularity')

fig = px.bar(top10_genres, x='genres', y=['valence', 'energy', 'danceability', 'acousticness'], barmode='group',
            title='Trend of various sound features over top 10 genres')
fig.show()

genre_list = genre_data['genres'].tolist()
genre_string = ', '.join(genre_list)

print("Genres: ")
print(genre_string)

artist_list = artist_data['artists'].tolist()
artist_string = ', '.join(artist_list)

print("Artists: ")
print(artist_string)

top10_popular_artists = artist_data.nlargest(10, 'popularity')
top10_most_song_produced_artists = artist_data.nlargest(10, 'count')

print('Top 10 Artists that produced most songs:')
top10_most_song_produced_artists[['count','artists']].sort_values('count',ascending=False)

# **clustering **

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

cluster_pipeline = Pipeline([('scaler', StandardScaler()), ('kmeans', KMeans(n_clusters=12))])
X = genre_data.select_dtypes(np.number)
cluster_pipeline.fit(X)
genre_data['cluster'] = cluster_pipeline.predict(X)

''' Visualizing the Clusters with t-SNE
 is an unsupervised Machine Learning algorithm.
 It has become widely used in bioinformatics and more generally in data science to visualise the structure of
 high dimensional data in 2 or 3 dimensions.
 While t-SNE is a dimensionality reduction technique, it is mostly used for visualization and not data pre-processing
 (like you might with PCA). For this reason, you almost always reduce the dimensionality down to 2 with t-SNE,
 so that you can then plot the data in two dimensions.
'''
from sklearn.manifold import TSNE

tsne_pipeline = Pipeline([('scaler', StandardScaler()), ('tsne', TSNE(n_components=2, verbose=1))])
genre_embedding = tsne_pipeline.fit_transform(X) # returns np-array of coordinates(x,y) for each record after TSNE.
projection = pd.DataFrame(columns=['x', 'y'], data=genre_embedding)
projection['genres'] = genre_data['genres']
projection['cluster'] = genre_data['cluster']

fig = px.scatter(
    projection, x='x', y='y', color='cluster', hover_data=['x', 'y', 'genres'],title='Clusters of genres')
fig.show()

song_cluster_pipeline = Pipeline([('scaler', StandardScaler()),
                                  ('kmeans', KMeans(n_clusters=25,
                                   verbose=False))
                                 ], verbose=False)

X = data.select_dtypes(np.number)
song_cluster_pipeline.fit(X)
song_cluster_labels = song_cluster_pipeline.predict(X)
data['cluster_label'] = song_cluster_labels

'''
# Visualizing the Clusters with PCA
Principal Component Analysis is an unsupervised learning algorithm that is used for the dimensionality reduction in machine learning.
One of the most major differences between PCA and t-SNE is it preserves only local similarities whereas PA preserves
large pairwise distance maximize variance. It takes a set of points in high dimensional data and converts it into low dimensional data.
'''
from sklearn.decomposition import PCA

pca_pipeline = Pipeline([('scaler', StandardScaler()), ('PCA', PCA(n_components=2))])
song_embedding = pca_pipeline.fit_transform(X)
projection = pd.DataFrame(columns=['x', 'y'], data=song_embedding)
projection['title'] = data['name']
projection['cluster'] = data['cluster_label']

fig = px.scatter(
    projection, x='x', y='y', color='cluster', hover_data=['x', 'y', 'title'],title='Clusters of songs')
fig.show()

!pip install spotipy

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Replace CLIENT_ID and CLIENT_SECRET with your own credentials
CLIENT_ID = 'ff28528ba5ac427c93000eb1278c0b9a'
CLIENT_SECRET = '1653b1684cd54ef5a3b155caf7978ae6'

# Authenticate and authorize the Spotipy client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Test the Spotipy client by getting the details of a track
track = sp.track('3n3Ppam7vgaVa1iaRUc9Lp')
print(track['name'])

#skipping sporify loging part

'''
Finds song details from spotify dataset. If song is unavailable in dataset, it returns none.
'''
def find_song(name, year):
    song_data = defaultdict()
    results = sp.search(q= 'track: {} year: {}'.format(name,year), limit=1)
    if results['tracks']['items'] == []:
        return None

    results = results['tracks']['items'][0]
    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]

    song_data['name'] = [name]
    song_data['year'] = [year]
    song_data['explicit'] = [int(results['explicit'])]
    song_data['duration_ms'] = [results['duration_ms']]
    song_data['popularity'] = [results['popularity']]

    for key, value in audio_features.items():
        song_data[key] = value

    return pd.DataFrame(song_data)

#Finds song details from spotify dataset. If song is unavailable in dataset, it returns none.
def find_song (name, year):
    song_data = defaultdict ()
    results = sp.search(q= 'track: () year: ()'.format (name, year), limit=1)
    if results['tracks']['items'] == []:
        return None
    results = results[ 'tracks' ]['items' ][0]
    track_id = results[ 'id']
    audio_features = sp.audio_features (track_id) [0]
    song_data ['name'] = [name]
    song_data['year'] = [year]
    song_data['explicit'] = [int(results ['explicit' ])]
    song_data['duration_ms'] = [results['duration_ms' ]]
    song_data['popularity'] = [results ['popularity' ]]
    for key, value in audio_features.items ():
        song_data[key] = value
    return pd. DataFrame (song_data)

number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit',
 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']

'''
Fetches song details from dataset. If info is unavailable in dataset, it will search details from the spotify dataset.
'''
def get_song_data(song, spotify_data):
    try:
        song_data = spotify_data[(spotify_data['name'] == song['name'])
                                & (spotify_data['year'] == song['year'])].iloc[0]
        print('Fetching song information from local dataset')
        return song_data

    except IndexError:
        print('Fetching song information from spotify dataset')
        return find_song(song['name'], song['year'])

'''
Fetches song info from dataset and does the mean of all numerical features of the song-data.
'''
def get_mean_vector(song_list, spotify_data):
    song_vectors = []
    for song in song_list:
        song_data = get_song_data(song, spotify_data)
        if song_data is None:
            print('Warning: {} does not exist in Spotify or in database'.format(song['name']))
            continue
        song_vector = song_data[number_cols].values
        song_vectors.append(song_vector)

    song_matrix = np.array(list(song_vectors))#nd-array where n is number of songs in list. It contains all numerical vals of songs in sep list.
    #print(f'song_matrix {song_matrix}')
    return np.mean(song_matrix, axis=0) # mean of each ele in list, returns 1-d array

'''
Flattenning the dictionary by grouping the key and forming a list of values for respective key.
'''
def flatten_dict_list(dict_list):
    flattened_dict = defaultdict()
    for key in dict_list[0].keys():
        flattened_dict[key] = [] # 'name', 'year'
    for dic in dict_list:
        for key,value in dic.items():
            flattened_dict[key].append(value) # creating list of values
    return flattened_dict

'''
Gets song list as input.
Get mean vectors of numerical features of the input.
Scale the mean-input as well as dataset numerical features.
calculate eculidean distance b/w mean-input and dataset.
Fetch the top 10 songs with maximum similarity.
'''
def recommend_songs( song_list, spotify_data, n_songs=10):

    metadata_cols = ['name', 'year', 'artists']
    song_dict = flatten_dict_list(song_list)

    song_center = get_mean_vector(song_list, spotify_data)
    #print(f'song_center {song_center}')
    scaler = song_cluster_pipeline.steps[0][1] # StandardScalar()
    scaled_data = scaler.transform(spotify_data[number_cols])
    scaled_song_center = scaler.transform(song_center.reshape(1, -1))
    distances = cdist(scaled_song_center, scaled_data, 'cosine')
    #print(f'distances {distances}')
    index = list(np.argsort(distances)[:, :n_songs][0])

    rec_songs = spotify_data.iloc[index]
    rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
    return rec_songs[metadata_cols].to_dict(orient='records')

from tkinter import *
root = Tk()

root.title("Music Recommendation System")

label = Label(root,text="Welcome to one-stop music recommendation system!!!")
label.pack(pady=10)
label = Label(root,text="Enter you favorite song:")
label.pack()
entry = Entry(root)
entry.pack()
def get_text():
    text = entry.get()
    label = Label(root,text=recommend_songs([{'name': text, 'year': 2019}],  data))
    label.pack()


button = Button(root, text="Submit",command = get_text)
button.pack()

mainloop()

recommend_songs([{'name': 'Blinding Lights', 'year': 2019}],  data)