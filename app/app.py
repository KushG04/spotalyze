from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from sklearn.cluster import KMeans
import pandas as pd
import os
from dotenv import load_dotenv

# load variables
load_dotenv()

# set up Spotify API client
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = "user-top-read user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    analysis = None
    if request.method == "POST":
        track_id = request.form.get("track_id")
        track = sp.track(track_id)
        audio_features = sp.audio_features([track_id])[0]
        
        # prepare df for clustering
        df_audio_features = pd.DataFrame([audio_features])
        
        # check samples for clustering
        if len(df_audio_features) >= 5:
            kmeans = KMeans(n_clusters=5, random_state=42)
            features = df_audio_features[['danceability', 'energy', 'tempo']]
            df_audio_features['cluster'] = kmeans.fit_predict(features)
            cluster_label = df_audio_features['cluster'][0]
        else:
            cluster_label = 'Insufficient data for clustering'
        
        analysis = {
            "track_name": track["name"],
            "artists": ", ".join(artist["name"] for artist in track["artists"]),
            "tempo": audio_features["tempo"],
            "danceability": audio_features["danceability"],
            "energy": audio_features["energy"],
            "cluster": cluster_label
        }

    return render_template("index.html", analysis=analysis)

if __name__ == "__main__":
    app.run(debug=True)