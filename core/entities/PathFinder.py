class PathFinder:

    # App paths:
    central_dir: str
    """
    directory address where app stored (home directory)
    """

    current_dir: str
    """
    pointer to current working directory of the application
    """

    path_to_books_dir: str
    """
    path where your books stored
    """

    book_read_file: str
    """
    Alias name for path where stored file with books history
    """

    FULL_PATH_TO_READ_FILE: str
    """
    Alias variable name for central dir + file name with read books
    """
