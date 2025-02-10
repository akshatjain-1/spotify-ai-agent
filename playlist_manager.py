# playlist_manager.py
def get_or_create_playlist(sp, user_id, playlist_name="AI Weekly Recommendations"):
    """
    Check if a playlist with the given name exists.
    If not, create one and return its ID.
    """
    playlists = sp.current_user_playlists(limit=50)
    for playlist in playlists.get('items', []):
        if playlist.get('name') == playlist_name:
            return playlist.get('id')
    # If not found, create the playlist (set public to False by default)
    playlist = sp.user_playlist_create(
        user=user_id, 
        name=playlist_name, 
        public=False, 
        description="Weekly AI song recommendations generated from your listening habits."
    )
    return playlist.get('id')

def update_playlist(sp, playlist_id, track_ids):
    """
    Replace the current items in the playlist with the new recommendations.
    """
    sp.playlist_replace_items(playlist_id, track_ids)
