# recommendation.py
from collections import Counter

def get_seed_tracks(df_tracks, num_seeds=3):
    """
    Select seed tracks based on frequency in the past 7 days.
    Returns a list of up to num_seeds track IDs.
    """
    if df_tracks.empty:
        return []
    # Count occurrences of each track and select the most played ones.
    top_tracks = df_tracks['track_id'].value_counts().head(num_seeds).index.tolist()
    return top_tracks

def compute_average_features(df_audio):
    """
    Compute the average audio features (danceability, energy, valence, tempo)
    from the DataFrame of audio features.
    """
    avg_features = {}
    for feature in ['danceability', 'energy', 'valence', 'tempo']:
        avg_features[feature] = df_audio[feature].mean()
    return avg_features

def get_recommendations(sp, seed_tracks, avg_features, limit=20):
    """
    Use Spotify's Recommendations API to generate song recommendations.
    The average features are passed as target values.
    """
    recommendations = sp.recommendations(
        seed_tracks=seed_tracks,
        limit=limit,
        target_danceability=avg_features.get('danceability'),
        target_energy=avg_features.get('energy'),
        target_valence=avg_features.get('valence'),
        target_tempo=avg_features.get('tempo')
    )
    rec_tracks = recommendations.get('tracks', [])
    rec_track_ids = [track.get('id') for track in rec_tracks if track.get('id')]
    return rec_tracks, rec_track_ids
