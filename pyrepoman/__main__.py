#!/usr/bin/env python3
# Standard Library Imports
import argparse, configparser, os

# Third Party Imports

# Local Application Imports
import actions, apis
from pyrepoman_configs import pyrepoman_configs_add, PYREPOMAN_CONFIGS, pyrepoman_configs_config_exist, pyrepoman_configs_merge

def parse_args():

    """ APPLICATION DESC AT THE PROMPT INCLUDING HELPFUL DOCUMENTATION """

    global EXCLUDE 
    EXCLUDE = ['update', 'list_web_hosts'] # to denote no need for --where arg

    DESC = """Description: This python application helps manage web-hosted/local Git repos with various actions."""
    parser = argparse.ArgumentParser(description=DESC, prog="pyrepoman.py")
    subparsers = parser.add_subparsers(title="available commands", metavar="command [options ...]")

    parser_update = subparsers.add_parser('update', help='update all Git repos in your current directory from remote repos')
    parser_update.set_defaults(func='update')

    parser_list_web_hosts = subparsers.add_parser('list-web-hosts', help='list currently supported web-hosts and api used')
    parser_list_web_hosts.set_defaults(func='list_web_hosts')

    parser_fetch = subparsers.add_parser('fetch', help='fetch all Git repos through a web provider')
    parser_fetch.add_argument('host', help='specifies what host to target')
    parser_fetch.add_argument('--host-path', metavar="path", default="", help='specifies what directory on the host to target for repos')
    parser_fetch.set_defaults(func='fetch')
    
    parser_archive = subparsers.add_parser('archive', help='archive all Git repos, done by bundling repos')
    parser_archive.add_argument('host', help='specifies what host to target')
    parser_archive.add_argument('archive_dir', help='what are you wanting to call the archive directory')
    parser_archive.add_argument('--host-path', metavar="path", default="", help='specifies what directory on the host to target for repos')
    parser_archive.set_defaults(func='archive')

    parser_backup = subparsers.add_parser('backup', help='backup all Git repos, done by mirroring repos fully')
    parser_backup.add_argument('host', help='specifies what host to target')
    parser_backup.add_argument('backup_dir', help='what are you wanting to call the backup directory')
    parser_backup.add_argument('--host-path', metavar="path", default="", help='specifies what directory on the host to target for repos')
    parser_backup.set_defaults(func='backup')

    args = vars(parser.parse_args()) # converts the Namespace object to a dict

    if('host' in args):
        args['host'] = args['host'].lower()

    return args

def task_arguments(task_name, host):

    """ TASKS ARGUMENTS ARE BASED IN THE CONFIG.INI FILE """
    if(task_name in EXCLUDE): # EXCLUDE action passes in none, default is placed in for host (e.g. github)
        host = 'github'
    config_app = configparser.ConfigParser()
    config_app.read(f"config_{host}.ini")
    script_configs = [item if item[1] != '' else -1 for item in config_app.items(task_name)]
    for pair in script_configs:
        pyrepoman_configs_merge(pair)
    return script_configs

def grab_task_func(task_name):

    """ BASED ON THE TASK, ITS ENTRY POINT IS RETURNED """

    TASKS = {
        'update': actions.update,
        'fetch': actions.fetch,
        'backup': actions.backup,
        'archive': actions.archive,
        'list_web_hosts': actions.list_web_hosts
    }

    return TASKS[task_name]

def add_runtime_to_pyrepoman_configs(runtime_args):

    for arg in runtime_args:
        pyrepoman_configs_add(arg, runtime_args[arg])

def main():

    runtime_args = parse_args()
    if(not runtime_args):
        return -1

    if(not apis.supported_host(runtime_args['host'].lower())):
        add_runtime_to_pyrepoman_configs(runtime_args)
    else:
        task_arguments(runtime_args['func'], str(runtime_args['host']).lower()) # casting as string incase of None
        add_runtime_to_pyrepoman_configs(runtime_args)

    if(pyrepoman_configs_config_exist(-1)):
        print(f"Error: missing values in configuration file for {runtime_args['func']}")
        return -1
    
    task = grab_task_func(runtime_args['func'])
    task()
    return 1

if(__name__ == '__main__'):
    main()