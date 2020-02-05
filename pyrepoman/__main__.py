#!/usr/bin/env python3
# Standard Library Imports
import argparse, configparser

# Third Party Imports

# Local Application Imports
import update_repos as upr
import apis, backup, archive
import fetch_repos as fetchr

def parse_args():

    """ APPLICATION DESC AT THE PROMPT INCLUDING HELPFUL DOCUMENTATION """

    def good_arg_values():
        exclude = ['update', 'list_web_hosts']
        if(not args[exclude[0]] and not args[exclude[1]]):
            for arg in args:
                if(args[arg] and args['where'] == None and arg not in exclude):
                    parser.error(f"--{arg} requires --where REPO-PROVIDER")
                    return False
        if(args['update'] and args['where']):
            parser.error("-u, --update does not need --where")
            return False
        if(True not in args.values()): # no action was selected, even if help was selected
            parser.print_help()
            return False
        return True

    DESC = """Description: This python application helps manage web-hosted Git repos with various actions."""
    parser = argparse.ArgumentParser(description=DESC, prog="pyrepoman.py")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--update", action="store_true", help="update all Git repos in your current directory from remote repos")
    group.add_argument("-f", "--fetch", action="store_true", help="fetch all Git repos through a web provider")
    group.add_argument("-a", "--archive", action="store_true", help="archive all Git repos, done by bundling repos")
    group.add_argument("-b", "--backup", action="store_true", help="backup all Git repos, done by mirroring repos fully")
    group.add_argument("-w", "--list-web-hosts", action="store_true", help="list currently supported web-hosts and api used")
    parser.add_argument("--where", metavar="PROVIDER", help="specifies for -a, -f, or -b what web hosted provider to target")
    args = vars(parser.parse_args()) # converts the Namespace object to a dict
    
    if(not good_arg_values()):
        return False

    args['task'] = [arg for arg in args if args[arg] == True][0]
    args['task_arg'] = [arg for arg in args if ((args[arg] != None) and (args[arg] != True) and (args[arg] != False))][0]

    return args

def get_task_arg_value(runtime_args):
    return runtime_args[runtime_args['task_arg']]

def list_supported_hosts(args):

    """ THIS IS DRIVEN BY THE -w SWITCH, ONLY TASK NOT IN A MODULE """

    for host in apis.SUPPORTED_HOSTS:
        print(f"{host}{apis.get_hostname_desc(host)}")

def task_arguments(task_name):

    """ TASKS ARGUMENTS ARE BASED IN THE CONFIG.INI FILE """
    
    config_app = configparser.ConfigParser()
    config_app.read('pyrepoman/config.ini')
    script_configs = [item if item[1] != '' else -1 for item in config_app.items(task_name)]
    return script_configs

def grab_task_func(task_name):

    """ BASED ON THE TASK, ITS ENTRY POINT IS RETURNED """

    TASKS = {
        'update': upr.main,
        'fetch': fetchr.main,
        'backup': backup.main,
        'archive': archive.main,
        'list_web_hosts': list_supported_hosts
    }

    return TASKS[task_name]

def run_task(task_obj, args):
    task_obj(args)

def main():
    runtime_args = parse_args()
    if(not runtime_args):
        return -1

    task_args = task_arguments(runtime_args['task'])
    task_args.append((runtime_args['task_arg'], get_task_arg_value(runtime_args)))
    #print(task_args)

    if(-1 in task_args):
        print(f"Error: missing values in configuration file for {runtime_args['task']}")
        return -1
    
    task = grab_task_func(runtime_args['task'])
    run_task(task, task_args)
    return 1

if(__name__ == '__main__'):
    main()