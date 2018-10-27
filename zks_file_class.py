

class ZksFile():
    '''
        PURPOSE - Open, modify, save, and close json files contained in Pathfinder Kingmaker
            save game files.
        USAGE

        NOTES
            ### SETUP ###
            [ ] saveGame = ZksFile("save_game_42.zks")  # Instantiates a JsonFile object
            [ ] saveGame.unpack_file(workDir)  # Unarchives the save file into a working directory
            [ ] saveGame.load_json_file(jsonName)  # Instantiates a specific json object
            [ ] saveGame.load_json_files()  # Instantiates all supported json objects
            [ ] saveGame.save_json_file(jsonName)  # Saves a specific json object
            [ ] saveGame.save_json_files()  # Saves all supported json objects
            [ ] saveGame.close_json_file(jsonName)  # Closes a specific json object
            [ ] saveGame.close_json_files()  # Closes all supported json objects
            ### FEATURES ###



            ### TEAR DOWN ###
            [ ] saveGame.update_zks()  # Updates .zks file with modified json files
            [ ] saveGame.close_zks()  # Closes the .zks file
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
            OUTPUT - None
            NOTES
                New class attributes must be zeroed in close_zks()
        '''
        # CLASS ATTRIBUTES
        self.zPath = None      # Path to the filename
        self.zName = None      # Filename
        self.zSuccess = False  # Set this to False if anything fails
        self.zChanged = False  # Set this to True if any json contents are modified
        # JSON Files Supported by the ZksFile class
        self.zSupportedJson = [ "header.json", "party.json", "player.json", "statistic.json" ]
        self.zHeadFile = None  # header.json JsonFile object
        self.zPartFile = None  # party.json JsonFile object
        self.zPlayFile = None  # player.json JsonFile object
        self.zStatFile = None  # statistic.json JsonFile object

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
            try:
                self.zPath = os.path.dirname(filename)
                self.zName = os.path.basename(filename)
            except Exception as err:
                print("\n{}".format(repr(err)))
                self.zSuccess = False
            else:
                self.zSuccess = True


# NOTE:  Enforce .zks file extension?  Maybe add a list of permitted file extensions?
#   Then I can add any back up file extension to the list.

