#!/usr/bin/env python3
# Standard Library Imports

# Third Party Imports

# Local Application Imports
from .cmd import Cmd
from .generator import Generator
from subprocess import CalledProcessError

def main():

    try:
        configholder = Cmd.retrieve_args()
        action = Generator.generate_action(configholder)
        action.run()
    except SystemExit: # thrown in: Cmd (entire class) if error occurs
        pass
    except FileNotFoundError as e: # thrown in: load_toml() if configuration file does not exist
        print(f"Error: a particular file can not be found, '{e.filename}'")
    except PermissionError as e: # thrown in: load_toml() if configuration file cannot be read, also thrown if pathlib cannot access file (e.g. someone else's directory), also thrown in update.py for getting dirs in current directory
        print(f"Error: a particular file/path was unaccessable, '{e.filename}'")
    except CalledProcessError as e:
        print(e.stderr)
    except Exception as e:
        print('Error: an unknown error occured, please report the following below:\n')
        print(e)

if(__name__ == '__main__'):
    main()
