# Naturally we need to import necessary libraries. You'll need to install pandas if you haven't already.

import os
import re
import sqlite3
import pandas as pd

# Settings are always nice

sonarr_db = "sonarr.db"  # You direct the script to your Sonarr database here, make sure it isn't running at the time.
sonarr_root_directory_to_replace = "/your/current/root"
sonarr_root_directory_to_replace_with = "/your/new/root"

radarr_db = "nzbdrone.db"  # You direct the script to your Radarr database here, make sure it isn't running at the time.
radarr_root_directory_to_replace = "/your/current/root"
radarr_root_directory_to_replace_with = "/your/new/root"

# Define functions here


def change_root_directories(your_database, replace_this, with_this):
    # Incomplete function
    if os.path.exists(your_database):
        current_string = ""
        new_string = re.sub(replace_this, with_this, current_string)
    return


# Main Script

# Apply to sonarr
change_root_directories(sonarr_db, sonarr_root_directory_to_replace, sonarr_root_directory_to_replace_with)

# Apply to radarr
change_root_directories(radarr_db, radarr_root_directory_to_replace, radarr_root_directory_to_replace_with)
