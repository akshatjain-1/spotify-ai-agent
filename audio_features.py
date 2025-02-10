# audio_features.py
import pandas as pd

def get_audio_features(sp, track_ids, batch_size=5):
    """
    Retrieve audio features for a list of track IDs.
    Remove duplicates before making API calls.
    """
    unique_ids = list(set(track_ids))
    features = []
    
    # Process in batches to avoid long query strings
    for i in range(0, len(unique_ids), batch_size):
        batch_ids = unique_ids[i:i+batch_size]
        try:
            batch_features = sp.audio_features(batch_ids)
            # Append only valid responses (non-None)
            features.extend([f for f in batch_features if f is not None])
        except Exception as e:
            print(f"Error fetching audio features for batch {batch_ids}: {e}")
            continue
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
