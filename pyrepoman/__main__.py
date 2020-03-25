#!/usr/bin/env python3
# Standard Library Imports

# Third Party Imports

# Local Application Imports
from .cmd import Cmd
from .generator import Generator

#TODO, ABSTRACT PAYLOAD AWAY SEE TOML FILE
#TODO, OR MAKE GITHUB A SUBCOMMAND TO EACH ACTION? (E.G. FETCH GITHUB --public, BACKUP GITHUB --private)

def main():

    try:
        CONFIGHOLDER = Cmd.retrieve_args()
        CONFIGHOLDER.load_toml()
        action = Generator.generate_action(CONFIGHOLDER)
        action.run()
    except SystemExit:
        pass
    except Exception as e:
        print(e)

if(__name__ == '__main__'):
    main()
