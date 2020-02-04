# Standard Library Imports
try:
	import os, datetime, subprocess, requests, configparser
except Exception as e:
	print(e)

# Third Party Imports

# Local Application Imports
import apis, helpers

def load_args(args):


	global USER, API_TOKEN, PAYLOAD, HOST
	USER, API_TOKEN, PAYLOAD, HOST = [helpers.get_arg_value(arg) for arg in args]

def main(args):
	load_args(args)
	if(not apis.supported_endpoint(HOST)):
		print("Error: web host passed in is not currently supported")
		return False
	repo_names_and_urls = helpers.get_repo_names_and_urls(HOST, 'fetch', USER, API_TOKEN, PAYLOAD) # key is repo name, value is repo url
	try:
		for repo_name in repo_names_and_urls:
			subprocess.run("git clone {0} {1}".format(repo_names_and_urls[repo_name], repo_name), shell=True)
		print('\nand finished...!')
		input()
	except Exception as e:
		print(e)
		input()