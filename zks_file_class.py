from json_file_class import JsonFile
import os
import zipfile


class ZksFile():
    '''
        PURPOSE - Open, modify, save, and close json files contained in Pathfinder Kingmaker
            save game files.
        USAGE
            1. saveGame = ZksFile("save_game_42.zks")
            2. saveGame.unpack_file(os.path.join("Baron_Builder", "Working"))
            3. saveGame.load_data()
            4. [modify save game contents]
            5. jsonSave.update_zks()
            6. jsonSave.close_zks()
        NOTES
            ### SETUP ###
            [X] saveGame = ZksFile("save_game_42.zks")  # Instantiates a ZksFile object
            [X] saveGame.check_dir(verDir)              # Check for the existence of a directory
            [X] saveGame.make_dirs(newDir)              # Make a new directory(s)
            [X] saveGame.unpack_file(workDir)           # Unarchives the save file into a working directory
            [X] saveGame.load_data()                    # Loads all of the supported json files into JsonFile objects
            [X] saveGame.load_json_file(jsonName)       # Instantiates a specific json object
            [X] saveGame.load_json_files()              # Instantiates all supported json objects
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
            New json files to be supported must be added to the following locations:
                - ZksFile.self.zSupportedJson
                - ZksFile.self.save_json_files()
    '''


    def __init__(self, filename):
        '''
            PURPOSE - Class ctor
            INPUT
                filename - String representation of a relative or absolute filename
            OUTPUT - None
            NOTES
                New class attributes must be zeroed in close_zks()
        '''
        # CLASS ATTRIBUTES
        self.zPath = None         # Path to the filename
        self.zName = None         # Filename
        self.origFileName = None  # Raw filename originally passed in
        self.zModDir = None       # Save game-specific working directory name
        self.fullWorkPath = None  # Full directory to the unpacked file's directory in the working dir
        self.zSuccess = False     # Set this to False if anything fails
        self.zChanged = False     # Set this to True if any json contents are modified
        # JSON Files Supported by the ZksFile class
        self.zSupportedJson = [ "header.json", "party.json", "player.json", "statistic.json" ]
        # Save Game File Extensions supported by ZksFile class
        self.zSaveGameExts = [ ".zks" ]  # Consider adding the backup file extension as well
        self.zHeadFile = None     # header.json JsonFile object
        self.zPartFile = None     # party.json JsonFile object
        self.zPlayFile = None     # player.json JsonFile object
        self.zStatFile = None     # statistic.json JsonFile object

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
                self.origFileName = filename
                self.zPath = os.path.dirname(self.origFileName)
                self.zName = os.path.basename(self.origFileName)
                self.zModDir = os.path.splitext(self.zName)[0]
            except Exception as err:
                self.zPath = None
                self.zName = None
                self.zModDir = None
                print("\n{}".format(repr(err)))
            else:
                # Verify the file extension
                zNameSplit = os.path.splitext(self.zName)
                if len(zNameSplit) > 0:
                    if zNameSplit[len(zNameSplit) - 1] not in self.zSaveGameExts:
                        self.zPath = None
                        self.zName = None
                        self.zModDir = None
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
                On bad input, None
        '''
        # LOCAL VARIABLES
        retVal = None

        # INPUT VALIDATION
        if not self.zSuccess:
            retVal = self.zSuccess
        elif not isinstance(verDir, str):
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
                On bad input, None
            NOTES
                This method will succeed if the directory already exists
                This method can handle multiple directories at once
        '''
        # LOCAL VARIABLES
        retVal = None

        # INPUT VALIDATION
        if not self.zSuccess:
            retVal = self.zSuccess
        elif not isinstance(newDir, str):
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
                    self.zSuccess = False
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
                On bad input, None
        '''
        # LOCAL VARIABLES
        retVal = None

        # INPUT VALIDATION
        if not self.zSuccess:
            retVal = self.zSuccess
        elif not isinstance(workDir, str):
            pass
        elif 0 >= len(workDir):
            pass
        else:
            # UNPACK THE FILE
            # 1. Setup Directories
            self.fullWorkPath = os.path.join(workDir, self.zModDir)
            # print("Full Work Path:\t{}".format(self.fullWorkPath))  # DEBUGGING
            retVal = self.make_dirs(self.fullWorkPath)

            # 2. Unpack File
            if retVal is True:
                try:
                    # print("Original File Name:\t{}".format(self.origFileName))  # DEBUGGING
                    with zipfile.ZipFile(self.origFileName, "r") as inZipFile:
                        inZipFile.extractall(self.fullWorkPath)
                except Exception as err:
                    print("\n{}".format(repr(err)))
                    retVal = False
                    self.zSuccess = False
            else:
                self.zSuccess = False

        # DONE
        return retVal


    def load_data(self):
        '''
            PURPOSE - Finalize any preparation before the user starts modifying save game content
            INPUT - None
            OUTPUT
                On success, True
                On failure, False
                On bad input, None
            NOTES
                Currently, this method just calls self.load_json_files().  In the future, it may
                    need to do more.
        '''
        # LOCAL VARIABLES
        retVal = None

        # INPUT VALIDATION
        if not self.zSuccess:
            retVal = self.zSuccess
        else:
            retVal = self.load_json_files()

        # DONE
        return retVal


    def load_json_file(self, jsonName):
        '''
            PURPOSE - Instantiate a JsonFile object for a given json filename
            INPUT
                jsonName - Full or relative path to a supported json file
            OUTPUT
                On success, True
                On failure, False
                On bad input, None
            NOTE:
                see self.zSupportedJson for a list of supported json files
        '''
        # LOCAL VARIABLES
        retVal = None
        baseJsonName = None  # Store os.path.basename(jsonName)

        # INPUT VALIDATION
        if not self.zSuccess:
            # print("ZksFile.load_json_file():\tEncountered previous failure")  # DEBUGGING
            retVal = self.zSuccess
        elif not isinstance(jsonName, str):
            # print("ZksFile.load_json_file():\tJson file name was not a string")  # DEBUGGING
            pass
        elif 0 >= len(jsonName):
            # print("ZksFile.load_json_file():\tJson file name was empty")  # DEBUGGING
            pass
        elif not os.path.exists(jsonName):
            # print("ZksFile.load_json_file():\tJson file {} does not exist".format(jsonName))  # DEBUGGING
            retVal = False
        elif not os.path.isfile(jsonName):
            # print("ZksFile.load_json_file():\tJson file {} is not a file".format(jsonName))  # DEBUGGING
            retVal = False
        else:
            try:
                baseJsonName = os.path.basename(jsonName)
                # print("Base Json File Name:\t{}".format(baseJsonName))  # DEBUGGING
            except Exception as err:
                print("\n{}".format(repr(err)))
                retVal = False
            else:
                if baseJsonName not in self.zSupportedJson:
                    print("ZksFile.load_json_file():\tJson file {} is not supported".format(jsonName))  # DEBUGGING
                    retVal = False
                else:
                    if "header.json" == baseJsonName:
                        self.zHeadFile = JsonFile(os.path.join(self.fullWorkPath, baseJsonName))
                        retVal = self.zHeadFile.jSuccess
                        self.zSuccess = retVal
                    elif "party.json" == baseJsonName:
                        self.zPartFile = JsonFile(os.path.join(self.fullWorkPath, baseJsonName))
                        retVal = self.zPartFile.jSuccess
                        self.zSuccess = retVal
                    elif "player.json" == baseJsonName:
                        self.zPlayFile = JsonFile(os.path.join(self.fullWorkPath, baseJsonName))
                        retVal = self.zPlayFile.jSuccess
                        self.zSuccess = retVal
                    elif "statistic.json" == baseJsonName:
                        self.zStatFile = JsonFile(os.path.join(self.fullWorkPath, baseJsonName))
                        retVal = self.zStatFile.jSuccess
                        self.zSuccess = retVal
                    else:
                        raise RuntimeError("load_json_file() appears to be missing an implementation for a supported json file")  # DEBUGGING
                        retVal = False

        # DONE
        if retVal is False:
            print("Failed to load json file:\t{}".format(jsonName))  # DEBUGGING
        return retVal


    def load_json_files(self):
        '''
            PURPOSE - Instantiate JsonFile objects for all support json filename
            INPUT - None
            OUTPUT
                On success, True
                On failure, False
                On bad input, None
            NOTES
                Iterates self.zSupportedJson to retreive the json filenames to open
                The JsonFile class doesn't actually parse any of the json files until it is needed
        '''
        # LOCAL VARIABLES
        retVal = None

        # INPUT VALIDATION
        if not self.zSuccess:
            retVal = self.zSuccess
        elif not os.path.isdir(self.fullWorkPath):
            print("\nThe save game does not appear to have been unpacked.")
            retVal = False
        else:
            for jsonFileName in self.zSupportedJson:
                retVal = self.load_json_file(os.path.join(self.fullWorkPath, jsonFileName))
                if retVal is not True:
                    break

        # DONE
        return retVal


'''
    player.json
        CompanionStories
        VisitedAreasData
        PartyCharacters
        InspectUnitsManager
        m_MainCharacter
        Chapter
        m_CameraPos
        m_Camping
        GameTime
        m_Dialog
        Difficulty
        SharedVendorTables
        m_CurrentFormationIndex
        CrossSceneState
        Money
        UISettings
        m_UnlockableFlags
        UpgradeActions
        m_AreaAmbienceData
        DetachedPartyCharacters
        Stalker
        ExCompanions
        RealTime
        RemoteCompanions
        SelectedFormation
        Achievements
        SharedStash
        SteamPremiumRewards
        REManager
        CustomFormations
        Weather
        $id
        m_QuestBook
        Kingdom
        m_GlobalMap
        GogPremiumRewards
        CurrentArea
        Encumbrance
'''