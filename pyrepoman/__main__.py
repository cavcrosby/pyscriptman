#!/usr/bin/env python3
# Standard Library Imports
import argparse, configparser, os

# Third Party Imports

# Local Application Imports
import actions, apis

def parse_args():

    """ APPLICATION DESC AT THE PROMPT INCLUDING HELPFUL DOCUMENTATION """

    global EXCLUDE 
    EXCLUDE = ['update', 'list_web_hosts'] # to denote no need for --where arg

    # def good_arg_values():
    #     exclude = ['update', 'list_web_hosts']
    #     if(not args[exclude[0]] and not args[exclude[1]]):
    #         for arg in args:
    #             if(args[arg] and args['where'] == None and arg not in exclude):
    #                 parser.error(f"--{arg} requires --where REPO-PROVIDER")
    #                 return False
    #     if(args['update'] and args['where']):
    #         parser.error("-u, --update does not need --where")
    #         return False
    #     if(True not in args.values()): # no action was selected, even if help was selected
    #         parser.print_help()
    #         return False
    #     return True

    DESC = """Description: This python application helps manage web-hosted Git repos with various actions."""
    parser = argparse.ArgumentParser(description=DESC, prog="pyrepoman.py")
    subparsers = parser.add_subparsers(title="available commands", metavar="command [options ...]")

    parser_update = subparsers.add_parser('update', help='update all Git repos in your current directory from remote repos')
    parser_update.set_defaults(func='update')

    parser_list_web_hosts = subparsers.add_parser('list-web-hosts', help='list currently supported web-hosts and api used')
    parser_list_web_hosts.set_defaults(func='list_web_hosts')

    parser_fetch = subparsers.add_parser('fetch', help='fetch all Git repos through a web provider')
    parser_fetch.add_argument('host', help='specifies what host to target')
    parser_fetch.add_argument('--path', metavar="path", default="", help='specifies what directory on the host to target for repos')
    parser_fetch.set_defaults(func='fetch')
    
    parser_archive = subparsers.add_parser('archive', help='archive all Git repos, done by bundling repos')
    parser_archive.add_argument('host', help='specifies what host to target')
    parser_archive.add_argument('--path', metavar="path", default="", help='specifies what directory on the host to target for repos')
    parser_archive.set_defaults(func='archive')

    parser_backup = subparsers.add_parser('backup', help='backup all Git repos, done by mirroring repos fully')
    parser_backup.add_argument('host', help='specifies what host to target')
    parser_backup.add_argument('--path', metavar="path", default="", help='specifies what directory on the host to target for repos')
    parser_backup.set_defaults(func='backup')

    args = vars(parser.parse_args()) # converts the Namespace object to a dict

    return args

def task_arguments(task_name, host):

    """ TASKS ARGUMENTS ARE BASED IN THE CONFIG.INI FILE """
    if(task_name in EXCLUDE): # EXCLUDE action passes in none, default is placed in for host (e.g. github)
        host = 'github'
    config_app = configparser.ConfigParser()
    config_app.read(f"config_{host}.ini")
    script_configs = [item if item[1] != '' else -1 for item in config_app.items(task_name)]
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

def run_task(task_obj, args):

    task_obj(args)

def main():

    runtime_args = parse_args()
    if(not runtime_args):
        return -1

    if(runtime_args['func'] in EXCLUDE):
        task_args = list()
        pass
    elif(not apis.supported_host(runtime_args['host'].lower())):
        task_args = [(runtime_args['func'], runtime_args['host'], runtime_args['path'])]
    else:
        task_args = task_arguments(runtime_args['func'], str(runtime_args['host']).lower()) # casting as string incase of None
        task_args.append(('host', runtime_args['host'].lower()))
        task_args.append(('path', runtime_args['path']))
    #print(task_args)

    if(-1 in task_args):
        print(f"Error: missing values in configuration file for {runtime_args['func']}")
        return -1
    
    task = grab_task_func(runtime_args['func'])
    run_task(task, task_args)
    return 1

if(__name__ == '__main__'):
    main()