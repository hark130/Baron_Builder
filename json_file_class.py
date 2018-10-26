# from codecs import BOM_UTF8
import codecs
import json
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
            [X] saveGame.parse_json_contents()           # Translate the raw json-format a dictionary
            [X] value1 = saveGame.get_data(key1)         # Get the value of an existing key
            [X] saveGame.key_present(key1)               # Determine if a key exists
            [X] saveGame.mod_data(key1, value2)          # Modify the value of an existing key
            [X] saveGame.add_data(key1337, value1337)    # Add a key/value pair to the dictionary
            [X] saveGame.del_data(key2)                  # Delete a key from the dictionary
            [X] saveGame.write_json_file()               # Overwrites existing file with changes
            [X] saveGame.close_json_file()               # Zeroizes all data (file is technically already closed)
    '''
    
    
    def __init__(self, filename):
        '''
            PURPOSE - Class ctor
            INPUT
                filename - String representation of a relative or absolute filename
            OUTPUT - None
            NOTES
                New class attributes must be zeroed in close_json_file()
        '''
        # CLASS ATTRIBUTES
        self.fPath = None     # Path to the filename
        self.fName = None     # Filename
        self.fCont = None     # Raw contents of filename
        self.fDict = None     # Dictionary parsed from self.fCont
        self.success = False  # Set this to False if anything fails
        self.changed = False  # Set this to True contents are modified
           
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
            self.success = True
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
        
        # INPUT VALIDATION
        if self.success:
            # READ FILE CONTENTS
            # Is the file already open?
            if not self.fCont:
                # Is there a path and filename?
                if self.fPath and self.fName:
                    # Open the file and read the contents
                    try:
                        with codecs.open(os.path.join(self.fPath, self.fName), "r", "utf-8-sig") as inFile:
                        # with open(os.path.join(self.fPath, self.fName), "r") as inFile:
                            self.fCont = inFile.read()
                            # print("\n{}".format(self.fCont))  # DEBUGGING
                            # Strip off the UTF-8 header
                            # if self.fCont.startswith(str(BOM_UTF8)):
                            #     self.fCont = self.fCont[len(str(BOM_UTF8)):]
                            # print("\n{}".format(self.fCont))  # DEBUGGING
                    except Exception as err:
                        print(repr(err))  # DEBUGGING
                        self.success = False
                    else:
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
        
        # INPUT VALIDATION
        if self.success:
            # PARSE RAW FILE CONTENTS
            if self.fCont and len(self.fCont) > 0:
                try:
                    self.fDict = json.loads(self.fCont)
                    # data = json.load(codecs.decode(r.text, 'utf-8-sig'))
                    # self.fDict = json.loads(codecs.decode(self.fCont, "utf-8-sig"))
                    # self.fDict = json.loads(codecs.decode(self.fCont, "utf-8-sig", errors = "ignore"))

                except Exception as err:
                    print(repr(err))  # DEBUGGING
                    self.success = False
                else:
                    retVal = True
        
        # DONE
        return retVal


    def get_data(self, key):
        '''
            PURPOSE - Resolve a key to its data in the json dictionary
            INPUT
                key - string representation of a key
            OUTPUT
                On success, the key's value
                None if the key does not exist
                On error, None
        '''
        # LOCAL VARIABLES
        retVal = None

        # INPUT VALIDATION
        if isinstance(key, str) and len(key) > 0 and self.success:
            if self.fDict:
                try:
                    if key in self.fDict.keys():
                        try:
                            retVal = self.fDict[key]
                        except Exception as err:
                            print(repr(err))
                            print("key == {}".format(key))  # DEBUGGING
                            print("self.fDict == {}".format(self.fDict))  # DEBUGGING
                except Exception as err:
                    print(repr(err))
                    print("key == {}".format(key))  # DEBUGGING
                    print("self.fDict == {}".format(self.fDict))  # DEBUGGING

        # DONE
        return retVal


    def key_present(self, key):
        '''
            PURPOSE - Determine if a key exists in the json dictionary
            INPUT
                key - string representation of a key
            OUTPUT
                If key is present, True
                If key is missing, False
        '''
        # LOCAL VARIABLES
        retVal = False

        # INPUT VALIDATION
        if isinstance(key, str) and len(key) > 0 and self.success:
            if self.get_data(key) is not None:
                retVal = True

        # DONE
        return retVal


    def mod_data(self, key, newData):
        '''
            PURPOSE - Modify existing data in the json dictionary
            INPUT
                key - string representation of a key
                newData - Key's new data
            OUTPUT
                On succcess, True
                On failure, False
            NOTES
                This method will fail if the key does not exist
        '''
        # LOCAL VARIABLES
        retVal = False

        # INPUT VALIDATION
        if isinstance(key, str) and len(key) > 0 and self.success:
            # Does the key exist?
            if self.key_present(key):
                self.fDict[key] = newData
                self.changed = True
                retVal = True

        # DONE
        return retVal


    def add_data(self, newKey, newData):
        '''
            PURPOSE - Add a new key to the json dictionary
            INPUT
                newKey - string representation of a new key to add
                newData - newKey's new data
            OUTPUT
                On success, True
                On failure, False
            NOTES
                If the key already exists, this method will fail
                This method permits empty strings as data
        '''
        # LOCAL VARIABLES
        retVal = False

        # INPUT VALIDATION
        if isinstance(newKey, str) and len(newKey) > 0 and self.success:
            # Does the key exist?
            if not self.key_present(newKey):
                self.fDict[newKey] = newData
                self.changed = True
                retVal = True

        # DONE
        return retVal


    def del_data(self, oldKey):
        '''
            PURPOSE - Remove a key/data pair from the json dictionary
            INPUT
                oldKey - string representation of the key to remove
            OUTPUT
                On success, True
                On failure, False
            NOTES
                This method will fail if the key does not exist
        '''
        # LOCAL VARIABLES
        retVal = False
        tempVal = None  # Store the return value from pop here

        # INPUT VALIDATION
        if isinstance(oldKey, str) and len(oldKey) > 0 and self.success:
            tempVal = self.fDict.pop(oldKey, None)
            if tempVal is not None:
                self.changed = True
                retVal = True

        # DONE
        return retVal


    def write_json_file(self):
        '''
            PURPOSE - Write the json content to the file
            OUTPUT
                On success, True
                On failure, False
            NOTES
                No file I/O will take place unless data has been modified
        '''
        # LOCAL VARIABLES
        retVal = False
        
        # INPUT VALIDATION
        if self.success:
            # OVERWRITE FILE
            if self.changed:
                try:
                    ######## DO I NEED MORE ENCODING HERE?!?! ########
                    with open(os.path.join(self.fPath, self.fName), 'w') as outFile:
                        json.dump(self.fDict, outFile)
                except Exception as err:
                    print(repr(err))  # DEBUGGING
                    self.success = False
                else:
                    retVal = True
            else:
                retVal = True  # No change made but everything is good
                
        # DONE
        return retVal        

    
    def close_json_file(self):
        '''
            PURPOSE - Clear out all class attributes without saving
            OUTPUT
                On success, True
                On failure, False
        '''
        # LOCAL VARIABLES
        retVal = False
        
        # RESET
        try:
            self.fPath = None
            self.fName = None
            self.fCont = None
            self.fDict = None
            self.success = True
        except Exception as err:
            print(repr(err))  # DEBUGGING
            retVal = False
        else:
            retVal = True
            
        # DONE
        return retVal
