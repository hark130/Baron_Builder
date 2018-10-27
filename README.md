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
| Locate save games dir | ✓ | ? | ? |
| Parse save games | ✓ | ? | ? |
| Print file open menu | ✓ | ? | ? |
| Print user selection menu | ✓ | ? | ? |
| Write json-parsing class | ✓ | ? | ? |
| Write save-file-parsing class | / | / | / |
| Release wheel | | | |
| Write wiki | | | |
| Python command not required to run | | | |
| Search _all_ home dirs for save games(?) | | | |

### Editor Features 

| Feature # | Task | Linux | Windows | Apple |
| :-------- | :--- | :---: | :-----: | :---: |
| F01 | Add BPs | | | |
| F02 | Change Kingdom Stability | | | |
| F03 | Backup save games | | | |
| F04 | Restore backed up save game | | | |
| F05 | Archive (AKA backup/delete) old saves (speed up loads/saves?) | | | |

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

