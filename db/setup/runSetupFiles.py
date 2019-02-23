import createDatabase
import createDBUser
import createTables
import grantDBUser

import json
import os
from pathlib import Path

def __run_setup_files(filedata):    

    """Runs the three setup scripts and feeds them data from the variable filedata

    Parameters
    ----------
    filedata: Is a dictionary with all the json data containing the keys connect and users
    """

    connection_dict = filedata["connection"]    # basic setup connection
    rw_user = filedata["user"]                  # user for read write access
    try:
        createDBUser.create_dbuser(connection_dict["host"], connection_dict["port"], 
                connection_dict["password"], rw_user["username"], rw_user["password"])
        
        createDatabase.create_database(connection_dict["host"], 
                connection_dict["port"], connection_dict["password"], 
                connection_dict["dbname"], rw_user["username"])
        
        createTables.create_tables(connection_dict["dbname"], connection_dict["user"], 
                connection_dict["host"], connection_dict["password"], connection_dict["port"])

        grantDBUser.grant_dbuser(connection_dict["dbname"], rw_user["username"],
                connection_dict["host"], connection_dict["port"], connection_dict["password"])
        
    except Exception as e:
        print("Exception while running setup scripts:", e)


def __load_json_file(filename):

    """Loads file and returns all the data

    Parameters
    ----------
    filename: Name of the json file that will be loaded
    
    Returns
    ----------
    A dictionary with all the data from the json file
    """
    try:
        dirname = os.path.dirname(__file__)
        if (dirname == ""): #If the script is run from the same folder we don't want to prepend "/" (as it would result in searching the root)
            filepath = filename
        else:
            filepath = dirname + "/" + filename
        with open(filepath) as f:
            filedata = json.load(f)
    except Exception as e:
        print("Exception while loading JSON file:", e)
        return
    return filedata 

def run():
    """Runs the script and it's functions
    """
    filename = 'data.json'

    filedata = __load_json_file(filename)
    __run_setup_files(filedata)

if __name__ == "__main__":
    run()