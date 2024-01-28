import time
import math
import logging

import references
import formatting
import callers

module_logger = logging.getLogger("primary.processing")


def select_tour(setlists):
    """Prompt user to select tour from setlist data

    Args:
        setlists (list): List of dicts containing setlist data

    Returns:
        list: List of dicts with setlist data for selected tour
    """
    options = references.get_options()
    # Set dict for tour counts with placeholder for setlists with no tour data
    tours = {'none': 0}
    for setlist in setlists:
        # If no tour data, add to placeholder and set tour name to placeholder
        if 'tour' not in setlist.keys():
            setlist['tour'] = {'name': 'none'}
            tours['none'] += 1
        # If tour already added to dict, update count
        elif setlist['tour']['name'] in tours.keys():
            tours[setlist['tour']['name']] += 1
        # Otherwise create tour entry in dict
        else:
            tours[setlist['tour']['name']] = 1

    # Check if only one tour
    if len(tours) == 2 and tours['none'] == 0:
        return setlists

    # Print tours with setlists counts
    print(f"No.  Tour  Setlist count")
    for idx, (tour, count) in enumerate(tours.items(), start=1):
        print(f"{idx}. {tour} - {count}")

    # Selection loop
    sel_loop = True
    while sel_loop is True:
        tour_sel = input("\nEnter number of tour to use or 0 to use all: ").lower().strip()
        if tour_sel in options['exit']:
            return None
        try:
            tour_sel = int(tour_sel)
        except ValueError:
            continue
        if len(tours) >= tour_sel >= 0:
            sel_loop = False
            break

    # Return all setlists
    if tour_sel == 0:
        return setlists
    # Identify tour selected
    else:
        # Iterate to get to tour name with matching index to selected tour
        for idx, tour in enumerate(tours.keys(), start=1):
            if idx == tour_sel:
                # Return only tours that match selected name
                return [setlist for setlist in setlists if setlist['tour']['name'] == tour]
            

def select_artist(setlists):
    """Prompt user to select artist from setlist data

    Args:
        setlists (list): List of dicts containing setlist data

    Returns:
        list: List of dicts with setlist data for selected artist
    """
    options = references.get_options()
    # Set dict for artist counts
    artists = {}
    for setlist in setlists:
        # If artist in dict, update count
        if setlist['artist']['name'] in artists.keys():
            artists[setlist['artist']['name']] += 1
        # Otherwise, create artists dict entry
        else:
            artists[setlist['artist']['name']] = 1

    # Check if only one artist
    if len(artists) == 1:
        return setlists
    
    # Print artists with setlists counts
    print(f"No.  Artist  Setlist count")
    for idx, (artist, count) in enumerate(artists.items(), start=1):
        print(f"{idx}. {artist} - {count}")

    # Selection loop
    sel_loop = True
    while sel_loop is True:
        artist_sel = input("\nEnter number of artist to use: ").lower().strip()
        if artist_sel in options['exit']:
            return None
        try:
            artist_sel = int(artist_sel)
        except ValueError:
            continue
        if len(artists) >= artist_sel >= 0:
            sel_loop = False
            break
    # Identify tour selected
    else:
        # Iterate to get to tour name with matching index to selected tour
        for idx, artist in enumerate(artists.keys(), start=1):
            if idx == artist_sel:
                # Return only tours that match selected name
                return [setlist for setlist in setlists if setlist['artist']['name'] == artist]


def get_tour_songs(setlist_data):
    """Return song data with average position and frequency from setlist data

    Args:
        setlist_data (list): List of dicts containing setlist data

    Returns:
        list: List of dicts of songs with average position and frequency performed
    """
    # Empty dict for song data
    tour_songs = {}
    print("Getting songs from setlists")

    for setlist in setlist_data:
        # Skip setlists with no set data
        if len(setlist['sets']['set']) == 0:
            continue
        # Cycle through song data to update tour song dict
        for pos, song in enumerate(setlist['sets']['set'][0]['song'], start=1):
            if song['name'] in tour_songs.keys():
                # If song in dict keys, add position and update count
                tour_songs[song['name']]['set_pos'].append(pos)
                tour_songs[song['name']]['times_played'] += 1
            else:
                # If song not in dict keys, create entry
                tour_songs[song['name']] = {}
                tour_songs[song['name']]['name'] = song['name']
                tour_songs[song['name']]['set_pos'] = [pos]
                tour_songs[song['name']]['times_played'] = 1

    # For each song, determine average position performed and frequency played
    for song in tour_songs.values():
        song['avg_pos'] = sum(song['set_pos'])/len(song['set_pos'])
        song['frequency'] = len(song['set_pos'])/len(setlist_data)

    # Create sorted list of dicts based on the average position performed
    sorted_songs = sorted(tour_songs.values(), key=lambda x: x['avg_pos'], reverse=False)

    return sorted_songs


def get_tour_data(artist, tour=''):
    """Builds API query and handles collection process

    Args:
        artist (str): Artist name to search for
        tour (str, optional): Tou name to search for. Defaults to ''.

    Returns:
        list: List of dicts containing setlist data
    """
    print("Getting tour data")
    
    # Format provided artist name
    artist = formatting.format_artist_name(artist)
    # Format provided tour name
    tour = formatting.format_tour_name(tour)

    # Build query
    page = 1
    if tour == '':
        query = f"&artistName={artist}"
    elif artist == '':
        query = f"&tourName={tour}"
    else:
        query = f"&artistName={artist}&tourName={tour}"
    module_logger.info(f"Starting query {query}")

    # Set query URL for API call
    url = f"https://api.setlist.fm/rest/1.0/search/setlists?p={page}{query}"

    # Call setlist.fm API
    data = callers.setlist_call(url)
    if data == None:
        return None
    # Select setlist data
    setlist_data = data['setlist']

    # Confirm additional requests
    pages_to_collect = math.ceil(data['total'] / data['itemsPerPage'])
    if pages_to_collect > 1:
        complete_time = formatting.seconds_to_time(pages_to_collect)
        print(f"Completing request will require collecting {pages_to_collect} more pages (est. {complete_time})")
        cont = input("Continue? (y/n): ").lower()
        if cont != 'y':
            return None
        
    # Print amount collected
    print(f"\nCollected {len(setlist_data)} of {data['total']} setlists.")

    # Collect additional data
    while data['total'] > len(setlist_data):
        # Inter-Call Pause
        time.sleep(1)
        # Increment page to collect
        page += 1
        # Update url with page number
        url = f"https://api.setlist.fm/rest/1.0/search/setlists?p={page}{query}"
        # Call setlist.fm API
        data = callers.setlist_call(url)
        # If no data returned, failure during collection, abort process and return to menu
        if data == None:
            return None
        # Add new setlist data to existing list
        setlist_data.extend(data['setlist'])
        # Show progress update
        print(f"Collected {len(setlist_data)} of {data['total']} setlists.")

    return setlist_data