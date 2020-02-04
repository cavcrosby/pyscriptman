#!/usr/bin/env python3
#######################################################################################
#
#       Author: Conner Crosby
#       Description:
#       The purpose of this script is to automate the mirroring (backing up) of Git
#       repos of a GitHub account, both full mirroring and bundling of the full mirror 
#       are done. All via the GitHub API.
#
#
#######################################################################################

# Standard Library Imports
import argparse, configparser

# Third Party Imports

# Local Application Imports
import update_repos as upr
import apis
import fetch_repos as fetchr
import backup 

def parse_args():

    DESC = """Description: This python application helps manage web-hosted Git repos with various actions."""
    parser = argparse.ArgumentParser(description=DESC, prog="pyrepoman.py")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--update", action="store_true", help="update all Git repos in your current directory from remote repos")
    group.add_argument("-f", "--fetch", action="store_true", help="fetch all Git repos through a web provider")
    group.add_argument("-a", "--archive", action="store_true", help="archive all Git repos, done by bundling repos")
    group.add_argument("-b", "--backup", action="store_true", help="backup all Git repos, done by mirroring repos fully")
    group.add_argument("-w", "--list-web-hosts", action="store_true", help="list currently supported web-hosts and api used")
    parser.add_argument("--where", metavar="PROVIDER", help="specifies for -a, -f, or -b what web hosted provider to target")
    args = parser.parse_args()

    if(args.fetch and args.where == None):
        parser.error("--fetch requires --where REPO-PROVIDER")
    if(args.archive and args.where == None):
        parser.error("--archive requires --where REPO-PROVIDER")
    if(args.backup and args.where == None):
        parser.error("--backup requires --where REPO-PROVIDER")
    if(args.list_web_hosts):
        list_supported_hosts()
        return False
    if(args.archive == False and args.backup == False and args.fetch == False and args.update == False and args.list_web_hosts == False):
        parser.print_help()
        return False

    args = vars(args) # converts the Namespace object to a dict
    args['task'] = [arg for arg in args if args[arg] == True][0]
    args['task_arg'] = [arg for arg in args if ((args[arg] != None) and (args[arg] != True) and (args[arg] != False))][0]

    return args

def list_supported_hosts():

    for host in apis.SUPPORTED_HOSTS:
        print(f"{host}{apis.get_hostname_desc(host)}")

def task_arguments(task_name):
    
    config_app = configparser.ConfigParser()
    config_app.read('pyrepoman/config.ini')
    script_configs = [item if item[1] != '' else -1 for item in config_app.items(task_name)]
    return script_configs

def grab_task_func(task_name):

    TASKS = {
        'update': upr.main,
        'fetch': fetchr.main,
        'backup': backup.main
    }

    return TASKS[task_name]

def run_task(task_obj, args):
    task_obj(args)

def main():
    runtime_args = parse_args()
    if(not runtime_args):
        return 1

    task_args = task_arguments(runtime_args['task'])
    task_args.append((runtime_args['task_arg'], runtime_args[runtime_args['task_arg']]))
    #print(task_args)

    if(-1 in task_args):
        print(f"Error: missing values in configuration file for {runtime_args['task']}")
        return 0

    task = grab_task_func(runtime_args['task'])
    run_task(task, task_args)

#TODO add function descriptions

if(__name__ == '__main__'):
    main()