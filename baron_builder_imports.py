'''
    PURPOSE - Organize all of the globals and macros implemented for Baron Builder
'''



#################################################
#################### IMPORTS ####################
#################################################

import os


#################################################
#################### MACROS #####################
#################################################

# OPERATING SYSTEM
OS_UNKNOWS = 0  # Unknows OS
OS_LINUX = 1    # All *nix
OS_WINDOWS = 2  # All Windows
OS_APPLE = 3    # All OS/?
# USER TOLERANCE
MAX_ERRS = 3    # Maximum number of bad user answers tolerated before giving up
# DIRECTORY NAMES
TOP_DIR = "Baron_Builder"  # Store everything in there
ARCHIVE_DIR = "Archive"    # Move archived save files here
BACKUP_DIR = "Backup"      # Backup save files here
WORKING_DIR = "Working"    # Use this directory to unarchive and modify save games
# FILE EXTENSIONS
SAVE_GAME_EXT = ".zks"     # Pathfinder Kingmaker save game file extension
BACKUP_EXT = ".bbb"        # Backed up save game file extension
ARCHIVE_EXT = ".bba"       # Archived save game file extension
MISC_BACKUP_EXT = ".bak"   # File extension for non-save games being backed up


#################################################
#################### GLOBALS ####################
#################################################

# SUPPORTED OPERATING SYSTEMS
supportedOSGlobal = [ OS_LINUX, OS_WINDOWS, OS_APPLE ]
# PYTHON MINIMUM VERSION REQUIRED
minMajNum = 3  # Minimum Python version major number
minMinNum = 5  # Minimum Python version minor number
minMicNum = 2  # Minimum Python version micro number
# OPERATING SYSTEM SAVE GAME LOCATIONS
# Linux - /home/user/.config/unity3d/Owlcat Games/Pathfinder Kingmaker/Saved Games
nixSaveGamePath = os.path.join(".config", "unity3d", "Owlcat Games", "Pathfinder Kingmaker", "Saved Games")
# Windows - C:\Users\user\AppData\LocalLow\Owlcat Games\Pathfinder Kingmaker\Saved Games
winSaveGamePath = os.path.join("AppData", "LocalLow", "Owlcat Games", "Pathfinder Kingmaker", "Saved Games")
# Apple - /home/user/Library/Application\ Support/unity.Owlcat\ Games.Pathfinder\ Kingmaker/Saved\ Games 
macSaveGamePath = os.path.join("Library", "Application Support", "unity.Owlcat Games.Pathfinder Kingmaker", "Saved Games")
# File name of the json file storing the save game list
saveGameJson = "steam-saves-release.json"
