# Baron_Builder

A save game editor for [Pathfinder Kingmaker](https://en.wikipedia.org/wiki/Pathfinder:_Kingmaker) by [Owlcat Games](https://owlcatgames.com/) that is written in Python 3 and supports Linux, Windows, and Apple installations.

## Description

I like the game Pathfinder Kingmaker but it has a lot of bugs, issues, and oversights.  Game-ending events happen without much fanfare, save games are deleted, plot-completing item drops are lost, etc.  Hours are being lost in what is becoming a poorly documented and unforgiving experience.  I want to continue but I don't want to waste my time on multiple restarts just to hit the same mysterious roadblock.  So here we are...

## Purpose

My end goal is to create a save game editor that works on all operating systems supported by [Pathfinder Kingmaker](https://en.wikipedia.org/wiki/Pathfinder:_Kingmaker).  I want this save game editor to resolve many of the issues my friends and I have been encountering.  I won't support _everything_ but I will support fixes to the annoying, poorly documented, game-ending problems that have been cropping up during our playthroughs.

## To Do

### Basic Functionality

| Task | Linux | Windows | Apple |
| :--- | :---: | :-----: | :---: |
| Verify Python version | ✓ | ✓ | ✓ |
| Check OS | ✓ | ✓ | ✓ |
| Locate save games dir | ✓ | ✓ | ? |
| Parse save games | ✓ | ✓ | ? |
| Print file open menu | ✓ | ✓ | ? |
| Print user selection menu | ✓ | ✓ | ? |
| Write json-parsing class | ✓ | ✓ | ? |
| Write save-file-parsing class | ✓ | ✓ | ? |
| Store compression_type for each file in .zks for ZksFile.update_zks() | ✓ | ✓ | ? |
| Release wheel | | | |
| Write wiki | / | / | / |
| Python command not required to run | | | |
| Search _all_ home dirs for save games(?) | | | |
| Implement pylint | | | |
| Implement continuous integration | | | |
| Implement doxygen | | | |
| Organize test code, class modules, and production code | | | |

### Editor Features 

| Feature # | Category          | Task | Linux | Windows | Apple |
| :-------: | :---------------: | :--- | :---: | :-----: | :---: |
| F01       | Game Play         | Add BPs | ✓ | ? | ? |
| F02       | Game Play         | Change Kingdom Stability | ✓ | ? | ? |
| F03       | File Management   | Backup save games | ✓ | ✓ | ? |
| F04       | File Management   | Restore backed up save game | ✓ | ? | ? |
| F05       | File Management   | Archive (AKA backup/delete) old saves | ✓ | ✓ | ? |
| F06       | Game Play         | Change gold | ✓ | ✓ | ? |
| F07       | File Management   | Clean up 'Working' directory | ✓ | ✓ | ? |
| F08       | File Management   | 'Working' directory tallies up storage size | | | |
| F09       | Utility           | Baron Builder system log | | | |
| F10       | File Management   | 'Working' directory is automatically cleaned up | | | |
| F11       | Game Optimization | 'Repair' steam-saves-release.json (remove dead entries) | | | |
| F12       | File Management   | Restore archived save games | / | / | / |
| F13       | Game Play         | Restock camping supplies for vendors | | | |
| F14       | Game Optimization | Fix a 'busted' save game list json | | | |
| F15       | File Management   | Prompt to overwrite a backup save game | | | |
| F16       | File Management   | Backup multiple save games at once | | | |
| F17       | File Management   | Archive multiple save games at once | | | |
| F18       | Utility           | Baron Builder user log | | | |

### BUGS

| Resolved | BUG # | File | Function | Details |
| :------: | :---: | :--- | :------- | :------ |
| ✓ | B01 | baron_builder_features | bbf06_GOLD_sub_menu | Menu allows default gold to exceed max macro |
|   | B02 | baron_builder_* | * | Refactor * to raise Exception for failure/error and capture/silence/interpret in baron_builder.py |
|   | B03 | baron_builder_file_mgmt | *menu() | Refactor top level menus to validate input once, at the highest appropriate level |
| ✓ | B04 | baron_builder_file_mgmt | add_save_game_to_list() | "Add save games" doesn't check for prior existence (fixed in F04) |

### Legend

| Symbol | Meaning |
| :----: | :------ |
| | Not yet begun |
| / | Work has begun |
| ? | Implemented but not tested |
| ✓ | Implemented and tested |

### Design

* Sub-directories created in save game directory
	* "Baron_Builder" (Encapsulating directory for all work done)
		* "Archive" (Move old save game files here)
		* "Backup" (Back up save game files here)
		* "Working" (Working directory to unarchive save files into)
	* Implement JsonFile and ZksFile classes to be directory-independent
		* AKA Don't 'hard code' directories
		* Make Baron_Builder pass in the necessary directories (e.g., Archive, Backup, Working)
		* This design will facilitate easy relocation of files in the future

### Branching

* Branch names should be based off BUG number, Feature number, or 'basic functionality' short title
* Branches verified on one operating system can be merged into development
* Avoid merging development into master until all implemented features have been tested on two operating systems