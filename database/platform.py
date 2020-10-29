from datetime import datetime
from enum import Enum

DIRECT_DOWNLOAD = "https://drive.google.com/uc?id={}&export=download"

class Platform(Enum):
    """An enumerated class that contains the Platforms
    in the Database for projects
    """
    MAC_OS = "Mac OS"
    WINDOWS = "Windows"

    ANDROID = "Android"

def get_datetime() -> str:
    """Returns the current day as a human readable date in
    the format of {month} {day}, {year}
    """

    dt = datetime.now()

    month = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ][dt.month - 1]

    date_superscript = {
        "st": [1, 21, 31],
        "nd": [2, 22],
        "rd": [3, 23],
        "th": [
            4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16,
            17, 18, 19, 20, 24, 25, 26,
            27, 28, 29, 30
        ]
    }
    for superscript in date_superscript:
        if dt.day in date_superscript[superscript]:
            break

    return f"{month} {dt.day}{superscript}, {dt.year}"