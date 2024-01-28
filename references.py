def get_options():
    """Returns menu options

    Returns:
        dict: Dict with option name keys and list of accepted variations as values
    """
    options = {
        'search': ['1', 'search'],
        'exit': ['0', 'e', 'q', 'exit', 'quit']
    }
    return options