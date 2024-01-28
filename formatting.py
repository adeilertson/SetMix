def seconds_to_time(total_seconds):
    """Converts seconds to formatted time string (36h 10m 6s)

    Args:
        total_seconds (float): Seconds to be converted to a time

    Returns:
        str: Formatted string for display
    """
    seconds = int(total_seconds%60)
    minutes = int((total_seconds/(60))%60)
    hours = int(total_seconds/3600)
    if hours > 0:
        req_time = f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        req_time = f"{minutes}m {seconds}s"
    else:
        req_time = f"{seconds}s"

    return req_time


def format_tour_name(tour):
    """Formats tour name to use in a API query url

    Args:
        tour (str): Raw tour name to format

    Returns:
        str: Formatted tour name
    """
    tour = tour.strip().replace(' ', '%20')
    return tour


def format_artist_name(artist):
    """Formats artist name to use in a API query url

    Args:
        artist (str): Raw artist name to format

    Returns:
        str: Formatted artist name
    """
    artist = artist.strip().replace(' ', '%20')
    return artist