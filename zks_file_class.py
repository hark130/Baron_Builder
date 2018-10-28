import os
import zipfile


class ZksFile():
    '''
        PURPOSE - Open, modify, save, and close json files contained in Pathfinder Kingmaker
            save game files.
        USAGE

        NOTES
            ### SETUP ###
            [X] saveGame = ZksFile("save_game_42.zks")  # Instantiates a ZksFile object
            [X] saveGame.check_dir(verDir)              # Check for the existence of a directory
            [X] saveGame.make_dirs(newDir)              # Make a new directory(s)
            [X] saveGame.unpack_file(workDir)           # Unarchives the save file into a working directory
            [ ] saveGame.load_json_file(jsonName)       # Instantiates a specific json object
            [ ] saveGame.load_json_files()              # Instantiates all supported json objects
            [ ] saveGame.save_json_file(jsonName)       # Saves a specific json object
            [ ] saveGame.save_json_files()              # Saves all supported json objects
            [ ] saveGame.close_json_file(jsonName)      # Closes a specific json object
            [ ] saveGame.close_json_files()             # Closes all supported json objects
            ### FEATURES ###



            ### TEAR DOWN ###
            [ ] saveGame.update_zks()                   # Updates .zks file with modified json files
            [ ] saveGame.close_zks()                    # Closes the .zks file
        JSON FILES SUPPORTED
            - header.json
            - party.json
            - player.json
            - statistic.json
    '''


    def __init__(self, filename):
        '''
            PURPOSE - Class ctor
            INPUT
                filename - String representation of a relative or absolute filename
                topDir - Top level directory to organize all of the unpacked and modified files
            OUTPUT - None
            NOTES
                New class attributes must be zeroed in close_zks()
        '''
        # CLASS ATTRIBUTES
        self.zPath = None      # Path to the filename
        self.zName = None      # Filename
        self.zModPath = None   # Save game-specific working directory name
        self.zSuccess = False  # Set this to False if anything fails
        self.zChanged = False  # Set this to True if any json contents are modified
        # JSON Files Supported by the ZksFile class
        self.zSupportedJson = [ "header.json", "party.json", "player.json", "statistic.json" ]
        # Save Game File Extensions supported by ZksFile class
        self.zSaveGameExts = [ ".zks" ]  # Consider adding the backup file extension as well
        self.zHeadFile = None  # header.json JsonFile object
        self.zPartFile = None  # party.json JsonFile object
        self.zPlayFile = None  # player.json JsonFile object
        self.zStatFile = None  # statistic.json JsonFile object

        # LOCAL VARIABLES
        zNameSplit = []  # Store the result of os.path.splitext(self.zName) here

        # INPUT VALIDATION
        if not isinstance(filename, str):
            # print("ZksFile ctor:\tfilename is not a string")  # DEBUGGING
            pass
        elif len(filename) <= 0:
            # print("ZksFile ctor:\tfilename is empty")  # DEBUGGING
            pass
        elif not os.path.exists(filename):
            # print("ZksFile ctor:\t{} does not exist".format(filename))  # DEBUGGING
            pass
        elif not os.path.isfile(filename):
            # print("ZksFile ctor:\t{} is not a file".format(filename))  # DEBUGGING
            pass
        else:
            # Split filename into parts
            try:
                self.zPath = os.path.dirname(filename)
                self.zName = os.path.basename(filename)
                self.zModPath = os.path.splitext(self.zName)[0]
            except Exception as err:
                self.zPath = None
                self.zName = None
                self.zModPath = None
                print("\n{}".format(repr(err)))
            else:
                # Verify the file extension
                zNameSplit = os.path.splitext(self.zName)
                if len(zNameSplit) > 0:
                    if zNameSplit[len(zNameSplit) - 1] not in self.zSaveGameExts:
                        self.zPath = None
                        self.zName = None
                        self.zModPath = None
                    else:
                        self.zSuccess = True


    def check_dir(self, verDir):
        '''
            PURPOSE - Verify the existence of a directory
            INPUT
                verDir - Relative or absolute path to a directory
            OUTPUT
                True if found
                False if missing
                None on error
        '''
        # LOCAL VARIABLES
        retVal = None

        # INPUT VALIDATION
        if not isinstance(verDir, str):
            pass
        elif 0 >= len(verDir):
            pass
        else:
            if not os.path.exists(verDir):
                retVal = False
            elif not os.path.isdir(verDir):
                retVal = False
            else:
                retVal = True

        # DONE
        return retVal


    def make_dirs(self, newDir):
        '''
            PURPOSE - Create a new directory
            INPUT
                newDir - Relative or absolute path to a new directory
            OUTPUT
                On success, True
                On failure, False
                None on error
            NOTES
                This method will succeed if the directory already exists
                This method can handle multiple directories at once
        '''
        # LOCAL VARIABLES
        retVal = None

        # INPUT VALIDATION
        if not isinstance(newDir, str):
            pass
        elif 0 >= len(newDir):
            pass
        else:
            # MAKE THE DIRECTORY
            # Does it already exist?
            if self.check_dir(newDir) is True:
                retVal = True
            else:
                try:
                    # If not, make it
                    os.makedirs(newDir)
                except Exception as err:
                    print("\n{}".format(repr(err)))
                    retVal = False
                else:
                    retVal = True

        # DONE
        return retVal


    def unpack_file(self, workDir):
        '''
            PURPOSE - Unpack a save game file into its own directory within the working directory
            INPUT
                workDir - Absolute or relative path to make a new save-game-specific dir and
                    store the unpacked contents
            OUTPUT
                On success, True
                On failure, False
                On error, None
        '''
        # LOCAL VARIABLES
        retVal = None
        fullInPath = None  # Store the full input filename (self.zPath + self.zName) here
        fullModPath = None  # Store the full directory (workDir + self.zModPath) here

        # INPUT VALIDATION
        if not isinstance(workDir, str):
            pass
        elif 0 >= len(workDir):
            pass
        else:
            # UNPACK THE FILE
            # 1. Setup Directories
            fullInPath = os.path.join(self.zPath, self.zName)
            fullModPath = os.path.join(workDir, self.zModPath)
            retVal = self.make_dirs(fullModPath)

            # 2. Unpack File
            if retVal is True:
                try:
                    with zipfile.ZipFile(fullInPath, "r") as inZipFile:
                        inZipFile.extractall(fullModPath)
                except Exception as err:
                    print("\n{}".format(repr(err)))
                    retVal = False

        # DONE
        return retVal




# with zipfile.ZipFile("file.zip","r") as zip_ref:
#     zip_ref.extractall("targetdir")
