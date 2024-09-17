import pandas as pd
from sklearn.cluster import KMeans

# get audio features from top tracks
def fetch_audio_features(sp, track_ids):
    audio_features = sp.audio_features(track_ids)
    return audio_features

# cluster audio features
def cluster_audio_features(audio_features, num_clusters=5):
    df = pd.DataFrame(audio_features)
    if len(df) >= num_clusters:
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        selected_features = df[['danceability', 'energy', 'tempo']]
        df['cluster'] = kmeans.fit_predict(selected_features)
        return df
    else:
        raise ValueError("Not enough data to perform clustering.")

# save data to csv
def save_data_to_csv(data, filename='data/top_tracks_audio_features.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")