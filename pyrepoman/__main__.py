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
#import git_backup as gitbak

def parse_args():

    DESC = """Description: This python application helps manage web-hosted Git repos with various actions."""
    parser = argparse.ArgumentParser(description=DESC, prog="pyrepoman.py")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--update", action="store_true", help="update Git repos in your current directory from remote repos")
    group.add_argument("-f", "--fetch", action="store_true", help="fetch Git repos from a through an api")
    group.add_argument("-a", "--archive", action="store_true", help="archive Git repos, done by bundling repos")
    group.add_argument("-b", "--backup", action="store_true", help="backup Git repos, done by mirroring repos fully")
    group.add_argument("-l", "--list", action="store_true", help="list currently supported api endpoints")
    parser.add_argument("--api", metavar="ENDPOINT", help="specifies for -a, -f, or -b that a api endpoint will be targeted")
    args = parser.parse_args()

    if(args.fetch and args.api == None):
        parser.error("--fetch requires --api ENDPOINT")
    if(args.archive and args.api == None):
        parser.error("--archive requires --api ENDPOINT")
    if(args.backup and args.api == None):
        parser.error("--backup requires --api ENDPOINT")
    if(args.list):
        list_apis()
        return False
    if(args.archive == False and args.backup == False and args.fetch == False and args.update == False and args.list == False):
        parser.print_help()
        return False

    args = vars(args) # converts the Namespace object to a dict
    args['task'] = [arg for arg in args if args[arg] == True][0]
    args['task_arg'] = [arg for arg in args if ((args[arg] != None) and (args[arg] != True) and (args[arg] != False))][0]

    return args

def list_apis():

    for api in apis.SUPPORTED_APIS:
        print(f"{api}{apis.get_endpoint_desc(api)}")

def task_arguments(task_name):
    
    config_app = configparser.ConfigParser()
    config_app.read('config.ini')
    script_configs = [item if item[1] != '' else -1 for item in config_app.items(task_name)]
    # TODO No section for action, is this due to file permissions?
    return script_configs

def grab_task_func(task_name):

    TASKS = {
        'update': upr.main,
        'fetch': fetchr.main
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