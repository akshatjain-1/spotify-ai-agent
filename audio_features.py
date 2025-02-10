# audio_features.py
import pandas as pd

def get_audio_features(sp, track_ids):
    """
    Retrieve audio features for a list of track IDs.
    Remove duplicates before making API calls.
    """
    unique_ids = list(set(track_ids))
    features = sp.audio_features(unique_ids)
    # Filter out any None responses
    features = [f for f in features if f is not None]
    return features

def features_to_dataframe(features):
    """
    Convert the audio features list into a Pandas DataFrame.
    Retain only key columns.
    """
    df = pd.DataFrame(features)
    # Select relevant columns for recommendation computations
    columns = ['id', 'danceability', 'energy', 'valence', 'tempo']
    df = df[columns]
    return df
