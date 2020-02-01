#######################################################################################
#
#       Author: Conner Crosby
#       Description:
#       The purpose of this script is to automate cloning all repos (public and private)
#       to a user's computer. Currently, this script works for pulling repos from GitHub
#		with the GitHub API.
#		TODO WORK ON DESCRIPTION
#
#######################################################################################

# Standard Library Imports
try:
	import os, datetime, subprocess, requests, configparser
except Exception as e:
	print(e)

# Third Party Imports

# Local Application Imports

import apis

def get_arg_value(field):
	
	return field[1]

def supported_endpoint():

	if(API not in apis.SUPPORTED_APIS):
		return False

	return True

def load_args(args):


	global USER, API_TOKEN, PAYLOAD, API
	USER, API_TOKEN, PAYLOAD, API = [get_arg_value(arg) for arg in args]

def get_repo_names_and_urls():
	
	return apis.get_endpoint_module_func(API, 'fetch')(API, USER, API_TOKEN, PAYLOAD)

def main(args):
	load_args(args)
	if(not supported_endpoint()):
		print("Error: api endpoint passed in is not currently supported")
		return False
	repo_names_and_urls = get_repo_names_and_urls() # key is repo name, value is repo url
	try:
		for repo_name in repo_names_and_urls:
			subprocess.run("git clone {0} {1}".format(repo_names_and_urls[repo_name], repo_name), shell=True)
		print('\nand finished...!')
		input()
	except Exception as e:
		print(e)
		input()