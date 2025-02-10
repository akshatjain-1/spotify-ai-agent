# data_collection.py
import datetime
import pandas as pd

def get_last_7_days_tracks(sp):
    """
    Retrieve recently played tracks from the last 7 days.
    Note: Spotify’s endpoint returns up to 50 tracks. If you need more data,
    you may have to adjust the logic.
    """
    # Calculate timestamp for 7 days ago (in milliseconds)
    now = datetime.datetime.now(datetime.timezone.utc)
    seven_days_ago = now - datetime.timedelta(days=7)
    after_timestamp = int(seven_days_ago.timestamp() * 1000)

    results = sp.current_user_recently_played(limit=50, after=after_timestamp)
    tracks = results.get('items', [])
    return tracks

def tracks_to_dataframe(tracks):
    """
    Convert the list of track items into a Pandas DataFrame.
    """
    data = []
    for item in tracks:
        track = item.get('track', {})
        data.append({
            'played_at': item.get('played_at'),
            'track_id': track.get('id'),
            'track_name': track.get('name'),
            'artist': track['artists'][0]['name'] if track.get('artists') else None,
            'popularity': track.get('popularity')
        })
    df = pd.DataFrame(data)
    if not df.empty:
        df['played_at'] = pd.to_datetime(df['played_at'])
    return df
