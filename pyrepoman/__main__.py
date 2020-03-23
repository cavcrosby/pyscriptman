#!/usr/bin/env python3
# Standard Library Imports

# Third Party Imports

# Local Application Imports
from .cmd import Cmd
from .generator import Generator

def main():

    try:
        CONFIGHOLDER = Cmd.retrieve_args()
        action = Generator.generate_action(CONFIGHOLDER)
        action.run()
    except SystemExit:
        pass
    except:
        print("OH NO")

if(__name__ == '__main__'):
    main()
