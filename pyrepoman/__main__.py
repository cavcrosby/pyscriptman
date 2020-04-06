#!/usr/bin/env python3
# Standard Library Imports

# Third Party Imports

# Local Application Imports
from .generator import Generator
from subprocess import CalledProcessError

def main():

    try:
        configholder = Generator.generate_cli_args()
        action = Generator.generate_action(configholder)
        action.run()
    except SystemExit:
        pass
    except FileNotFoundError as e: 
        print(f"Error: a particular file can not be found, '{e.filename}'")
    except PermissionError as e:
        print(f"Error: a particular file/path was unaccessable, '{e.filename}'")
    except CalledProcessError as e:
        print(e.stderr)
    except Exception as e:
        print('Error: an unknown error occured, please report the following below:')
        print(e)

if(__name__ == '__main__'):
    main()
