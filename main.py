# main.py
from spotify_client import get_spotify_client
from data_collection import get_last_7_days_tracks, tracks_to_dataframe
from audio_features import get_audio_features, features_to_dataframe
from recommendations import get_seed_tracks, compute_average_features, get_recommendations
from playlist_manager import get_or_create_playlist, update_playlist

def main():
    # Step 1: Authenticate and create Spotify client
    sp = get_spotify_client()
    user = sp.current_user()
    user_id = user.get('id')
    
    # Step 2: Get your recently played tracks from the last 7 days
    tracks = get_last_7_days_tracks(sp)
    if not tracks:
        print("No tracks found in the last 7 days.")
        return
    df_tracks = tracks_to_dataframe(tracks)
    print("Fetched listening history:")
    print(df_tracks.head())

    # Step 3: Retrieve audio features for these tracks
    track_ids = df_tracks['track_id'].tolist()
    features = get_audio_features(sp, track_ids)
    if not features:
        print("Could not retrieve audio features.")
        return
    df_audio = features_to_dataframe(features)
    
    # Step 4: Compute your listening profile and select seed tracks
    avg_features = compute_average_features(df_audio)
    seed_tracks = get_seed_tracks(df_tracks)
    if not seed_tracks:
        print("Not enough seed tracks for recommendation.")
        return

    # Step 5: Get recommendations based on your listening profile
    rec_tracks, rec_track_ids = get_recommendations(sp, seed_tracks, avg_features)
    print("Recommended Tracks:")
    for track in rec_tracks:
        print(f"{track.get('name')} by {', '.join([artist['name'] for artist in track.get('artists', [])])}")

    # Step 6: Update (or create) your dedicated recommendation playlist
    playlist_id = get_or_create_playlist(sp, user_id)
    update_playlist(sp, playlist_id, rec_track_ids)
    print(f"Playlist (ID: {playlist_id}) updated with {len(rec_track_ids)} recommended tracks.")

if __name__ == "__main__":
    main()
