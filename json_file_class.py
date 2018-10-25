import os

class JsonFile():
    '''
        PURPOSE - Open, modify, save, and close json files
        USAGE
            1. saveGame = JsonFile("save_game_42.zks")
            2. saveGame.read_json_file()
            3. saveGame.parse_json_contents()
            4. [modify json contents using mod, add, or del]
            5. saveGame.write_json_file()
            6. saveGame.close_json_file()
        NOTES
            [X] saveGame = JsonFile("save_game_42.zks")  # Instantiates a JsonFile object
            [X] saveGame.read_json_file()                # Read the raw file contents
            [/] saveGame.parse_json_contents()           # Translate the raw json-format a dictionary
            [ ] value1 = saveGame.get_data(key1)         # Get the value of an existing key
            [ ] saveGame.mod_data(key1, value2)          # Modify the value of an existing key
            [ ] saveGame.add_data(key1337, value1337)    # Add a key/value pair to the dictionary
            [ ] saveGame.del_data(key2)                  # Delete a key from the dictionary
            [ ] saveGame.write_json_file()               # Overwrites existing file with changes
            [ ] saveGame.close_json_file()               # Zeroizes all data (file is technically already closed)
    '''
    
    
    def __init__(self, filename):
        # CLASS ATTRIBUTES
            self.fPath = None  # Path to the filename
            self.fName = None  # Filename
            self.fCont = None  # Raw contents of filename
            self.fDict = None  # Dictionary parsed from self.fCont
           
        # INPUT VALIDATION
        if not isinstance(filename, str):
            # print("JsonFile ctor:\tfilename is not a string")  # DEBUGGING
            pass
        elif len(filename) <= 0:
            # print("JsonFile ctor:\tfilename is empty")  # DEBUGGING
            pass
        elif not os.path.exists(filename):
            # print("JsonFile ctor:\t{} does not exist".format(filename))  # DEBUGGING
            pass
        elif not os.path.isfile(filename):
            # print("JsonFile ctor:\t{} is not a file".format(filename))  # DEBUGGING
            pass
        else:            
            self.fPath = os.path.dirname(filename)
            self.fName = os.path.basename(filename)
        
        
    def read_json_file(self):
        '''
            PURPOSE - Open a file and read its raw contents
            OUTPUT
                On success, True
                On failure, False
            NOTES
                Validates the presence and type of file prior to opening it
                Attempts to silence any error-based exceptions
        '''
        # LOCAL VARIABLES
        retVal = False
        
        # READ FILE CONTENTS
        # Is the file already open?
        if not self.fCont:
            # Is there a path and filename?
            if self.fPath and self.fName:
                # Open the file and read the contents
                with open(os.path.join(self.fPath, self.fName), "r") as inFile:
                    self.fCont = inFile.read()
                
                # Verify the read
                if self.fCont:
                    retVal = True

        # DONE
        return retVal
        
        
    def parse_json_contents(self):
        '''
            PURPOSE - Parse the raw contents of a json file into a dictionary
            OUTPUT
                On success, True
                On failure, False
        '''
        # LOCAL VARIABLES
        retVal = False
        
        # PARSE RAW FILE CONTENTS
        if self.fCont and len(self.fCont) > 0:
            pass  # IMPLEMENT THIS LATER
        
        # DONE
        return retVal
                
        
