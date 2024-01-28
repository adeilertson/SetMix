import os

def print_avg_setlist(tour_songs, artist, tour):
    """Print average setlist from list of sorted songs

    Args:
        tour_songs (list): Sorted list of dicts with song data
        artist (str): Artist for song data
        tour (str): Tour for song data
    """
    max_song_len = 0
    for pos, song in enumerate(tour_songs, start=1):
        if len(song['name']) > max_song_len:
            max_song_len = len(song['name'])
    max_song_len += 2

    print(f" {artist} {tour}\n")
    print(f" Avg Pos   {'Song':<{max_song_len-2}}   Frequency performed")
    for pos, song in enumerate(tour_songs, start=1):
        print(f" {pos:<9} {song['name']:<{max_song_len}} {song['frequency']:.2%}")


def print_header():
    """
    Clears terminal screen and shows sylized header text
    Stylized text source (slant) - https://coolgenerator.com/ascii-text-generator
    """
    os.system('cls')
    print("""
   _____      __     __  ____     
  / ___/___  / /_   /  |/  (_)  __
  \__ \/ _ \/ __/  / /|_/ / / |/_/
 ___/ /  __/ /_   / /  / / />  <  
/____/\___/\__/  /_/  /_/_/_/|_|  
""")


def print_main_menu():
    """
    Prints main menu options
    """
    print("""
    1. Search by tour and artist name
        """)