# Standard Library Imports
import os, datetime, subprocess, requests, configparser

# Third Party Imports

# Local Application Imports
import apis, helpers

def load_args(args):

	global USER, API_TOKEN, PAYLOAD, HOST
	USER, API_TOKEN, PAYLOAD, HOST = [helpers.get_arg_value(arg) for arg in args]

def main(args):
	
	load_args(args)
	repo_names_and_urls = helpers.get_repo_names_and_urls(HOST, 'fetch', USER, API_TOKEN, PAYLOAD) # key is repo name, value is repo url
	try:
		for repo_name in repo_names_and_urls:
			subprocess.run("git clone {0} {1}".format(repo_names_and_urls[repo_name], repo_name), shell=True)
		print('\nand finished...!\n')
		return 1
	except Exception as e:
		print(e)
		return -1