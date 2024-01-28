import time
import logging

import processing
import screens
import formatting

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

    cont = input("\n\n Press enter to return to menu. ")
    return None