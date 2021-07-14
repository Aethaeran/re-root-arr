import os
import re
import sqlite3

# Here is where you customize settings.

# You direct the script to your Sonarr database here, make sure it isn't running at the time.
sonarr_db = "sonarr.db"
sonarr_root_directory_to_replace = "/your/current/root"
sonarr_root_directory_replacement = "/your/new/root"

# You direct the script to your Radarr database here, make sure it isn't running at the time.
radarr_db = "radarr.db"
radarr_root_directory_to_replace = "/your/current/root"
radarr_root_directory_replacement = "/your/new/root"

sonarr = ""
while str.lower(sonarr) != "yes" and str.lower(sonarr) != "no":
    sonarr = input("Do you want to re-root Sonarr?"+"\n")
    if str.lower(sonarr) != "yes" and str.lower(sonarr) != "no":
        print("You must answer 'yes' or 'no'.")
if str.lower(sonarr) == ("yes"):
    print("Ensure Sonarr is not running until the script is complete.")
    print("The script needs to know where your sonarr.db is located.")
    value = input("Please enter the absolute path:\n")
    print("The script needs to know which root path it is replacing.")
    sonarr_root_directory_to_replace = input('Please enter the entire root path ie. "/your/current/root":\n')
    print("The script needs to know which path to replace it with.")
    sonarr_root_directory_replacement = input('Please enter the entire root path ie. "/your/new/root":\n')
elif str.lower(sonarr) == ("no"):
    print("We won't re-root Sonarr then.")


radarr = ""
while str.lower(radarr) != "yes" and str.lower(radarr) != "no":
    radarr = input("Do you want to re-root Radarr?"+"\n")
    if str.lower(radarr) != "yes" and str.lower(radarr) != "no":
        print("You must answer 'yes' or 'no'.")
if str.lower(radarr) == ("yes"):
    print("Ensure Radarr is not running until the script is complete.")
    print("The script needs to know where your radarr.db is located.")
    value = input("Please enter the absolute path:\n")
    print("The script needs to know which root path it is replacing.")
    radarr_root_directory_to_replace = input('Please enter the entire root path ie. "/your/current/root":\n')
    print("The script needs to know which path to replace it with.")
    radarr_root_directory_replacement = input('Please enter the entire root path ie. "/your/new/root":\n')
elif str.lower(radarr) == ("no"):
    print("We won't re-root Radarr then.")

def sonarr_change_root_directories(your_database, replace_this, with_this):

    if os.path.exists(your_database):
        conn = sqlite3.connect(your_database)
        c = conn.cursor()

        # Sonarr DB tables that need updating
        print("Updating sonarr 'RootFolders' table...")
        # RootFolders, Path column
        root_folders_to_change = []
        for row in c.execute('SELECT * FROM RootFolders WHERE Path Like "' + str(replace_this) + '%"'):
            root_folders_to_change.append(row[1])  # Append Path column to list

        for item in root_folders_to_change:
            new_path = re.sub(replace_this, with_this, item)
            print(item+" --> "+new_path)
            c.execute('UPDATE RootFolders SET Path="' + new_path + '" WHERE Path like "' + item + '%"')

        print("Updating sonarr 'Series' table...")
        series_to_change = []
        for row in c.execute('SELECT * FROM Series WHERE Path Like "' + str(replace_this) + '%"'):
            series_to_change.append(row[11])  # Append Path column to list

        for item in series_to_change:
            new_path = re.sub(replace_this, with_this, item)
            print(item+" --> "+new_path)
            c.execute('UPDATE Series SET Path="' + new_path + '" WHERE Path like "' + item + '%"')

        # You'd want to change these too if you were making the change between Windows and Linux

        # MetadataFiles, RelativePath
        # SubtitleFiles, RelativePath
        # ExtraFiles, RelativePath
        # EpisodeFiles, RelativePath

        # Save (commit) the changes
        conn.commit()
        conn.close()


def radarr_change_root_directories(your_database, replace_this, with_this):

    if os.path.exists(your_database):
        conn = sqlite3.connect(your_database)
        c = conn.cursor()

        # Radarr DB tables that need updating
        # RootFolders, Path column
        root_folders_to_change = []
        for row in c.execute('SELECT * FROM RootFolders WHERE Path Like "' + str(replace_this) + '%"'):
            root_folders_to_change.append(row[1])  # Append Path column to list

        for item in root_folders_to_change:
            new_path = re.sub(replace_this, with_this, item)
            print(item+" --> "+new_path)
            c.execute('UPDATE RootFolders SET Path="' + new_path + '" WHERE Path like "' + item + '%"')

        # Movies, Path column
        movies_to_change = []
        for row in c.execute('SELECT * FROM Movies WHERE Path Like "' + str(replace_this) + '%"'):
            movies_to_change.append(row[9])  # Append Path column to list

        for item in movies_to_change:
            new_path = re.sub(replace_this, with_this, item)
            print(item+" --> "+new_path)
            c.execute('UPDATE Movies SET Path="' + new_path + '" WHERE Path like "' + item + '%"')

        # ImportLists, RootFolderPath column
        net_import_to_change = []
        # If you uncomment the following line, and comment the one following that,
        # and do that in the following block as well,
        # then you can use these two blocks to set the RootFolderPath on all ImportListss simultaneously
        # for row in c.execute('SELECT * FROM ImportLists WHERE RootFolderPath Like "%"'):
        for row in c.execute('SELECT * FROM ImportLists WHERE RootFolderPath Like "' + str(replace_this) + '%"'):
            net_import_to_change.append(row[7])  # Append RootFolderPath column to list

        for item in net_import_to_change:
            new_path = re.sub(replace_this, with_this, item)
            print(item+" --> "+new_path)
            # c.execute('UPDATE ImportLists SET RootFolderPath="' + with_this + '" WHERE RootFolderPath like "%"')
            c.execute('UPDATE ImportLists SET RootFolderPath="'+new_path+'" WHERE RootFolderPath like "'+item+'%"')

        # You'd want to change these too if you were making the change between Windows and Linux

        # SubtitleFiles, RelativePath
        # MovieFiles, RelativePath column # Probably unnecessary. I don't think Radarr supports sub-folders.

        # Save (commit) the changes
        conn.commit()
        conn.close()


# Apply changes to sonarr
if str.lower(sonarr) == ("yes"):
    sonarr_change_root_directories(sonarr_db, sonarr_root_directory_to_replace, sonarr_root_directory_replacement)

# Apply changes to radarr
if str.lower(radarr) == ("yes"):
    radarr_change_root_directories(radarr_db, radarr_root_directory_to_replace, radarr_root_directory_replacement)
