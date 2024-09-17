from spotify_api import setup_spotify_client, get_user_top_tracks
from processing import fetch_audio_features, save_data_to_csv

# main
def main():
    sp_client = setup_spotify_client()
    track_ids = get_user_top_tracks(sp_client)
    audio_features = fetch_audio_features(sp_client, track_ids)
    save_data_to_csv(audio_features)

if __name__ == "__main__":
    main()