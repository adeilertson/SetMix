import time
import logging

import processing
import screens
import formatting
import callers

module_logger = logging.getLogger("primary.actions")


def setlist_search():
    """Setlist search process handler

    Returns:
        None
    """
    # Reset screen
    screens.print_header()

    # Get artist to search for
    artist = input("Enter artist name: ")
    
    # Get tour to search for
    tour = input("Enter tour name: ")

    # No search term check
    if artist.strip() == '' and tour.strip() == '':
        cont = input("No search terms entered. Press enter to return to menu. ")
        return None

    # Start collection timer
    start_time = time.time()

    # Search for tour
    tour_data = processing.get_tour_data(artist, tour)
    if tour_data is None:
        return None

    # Show collection timing and outcomes
    elapsed_time = formatting.seconds_to_time(time.time() - start_time)
    print(f"Collected data for {len(tour_data)} setlists in {elapsed_time}")
    module_logger.info(f"Collected {len(tour_data)} setlists in {elapsed_time}")

    # Confirm artist
    tour_data = processing.select_artist(tour_data)

    # Confirm tour
    tour_data = processing.select_tour(tour_data)

    # Get tour setslists
    tour_avg_setlist = processing.get_tour_songs(tour_data)

    # Set artist display name
    artist_display = tour_data[0]['artist']['name']

    # Set tour display name
    tour_display = tour_data[0]['tour']['name']
    if tour_display == 'none':
        tour_display = ''

    # Show average setlists
    screens.print_header()
    screens.print_avg_setlist(tour_avg_setlist, artist_display, tour_display)

    # Spotify prompt
    cont = input("\nCreate spotify playlist from average setlist? (y/n): ").lower()

    if cont == 'y':
        create_setlist_playlist(tour_avg_setlist, artist_display)

    cont = input("\n\n Press enter to return to menu. ")
    return None


def create_setlist_playlist(songs, artist):
    sp_session = callers.spotify_auth()

    playlist_name = input('Enter playlist name: ')
    
    track_ids = []

    # Search for each song in night 2 setlist and get spotify track IDs
    for song in songs:
        song_query = f"track:{song['name']} artist:{artist}"
        result = sp_session.search(song_query, type='track')
        module_logger.info(f"spotify - Searched for {song_query} for user {sp_session.me()['id']}")
        if len(result['tracks']['items']) > 0:
            track_ids.append(result['tracks']['items'][0]['id'])
        else:
            print(f"Unable to find track for {song['name']} by {artist}")

    try:
        playlist = callers.create_playlist(sp_session, playlist_name)
        snapshot = sp_session.playlist_add_items(playlist['id'], track_ids)
        module_logger.info(f"spotify - Added {len(track_ids)} songs to playlist {playlist['id']} for user {sp_session.me()['id']}")
    except Exception as e:
        module_logger.error(f"spotify - Error creating playlist for user {sp_session.me()['id']} - {e}")
        module_logger.exception("Crash error")
        print(f"Unable to create playlist {playlist_name} due to error - {e}")
        cont = 'Press enter to return to menu. '
        return None

    print(f"Playlist {playlist_name} created. \n\nLink:\n{playlist['external_urls']['spotify']}")
    cont = 'Press enter to return to menu. '

    return None
