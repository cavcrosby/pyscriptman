# Standard Library Imports
import argparse, configparser, os

# Third Party Imports

# Local Application Imports
import apis

def main(args):

    for host in apis.SUPPORTED_HOSTS:
        print(f"{host}{apis.get_hostname_desc(host)}")