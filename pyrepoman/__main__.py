#!/usr/bin/env python3
# Standard Library Imports

# Third Party Imports
import toml

# Local Application Imports
from .exceptions.hostgeneratorerror import HostGeneratorError
from .exceptions.actiongeneratorerror import ActionGeneratorError
from .cmd import Cmd
from .generator import Generator

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
    except ActionGeneratorError as e:
        print(e)
    except HostGeneratorError as e:
        print(e)
    except toml.decoder.TomlDecodeError as e: # thrown in: load_toml() if configuration file has bad syntax error
        print('Error: the configuration file contains syntax error(s), more details below')
        print(e)
    except Exception as e:
        print('Error: an unknown error occured, please report the following below:\n')
        print(e)

if(__name__ == '__main__'):
    main()
