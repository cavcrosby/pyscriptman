# Standard Library Imports
import os, datetime, subprocess

# Third Party Imports

# Local Application Imports

def get_repo_names():
	try:
		repos = os.listdir(os.getcwd())
		return [repo for repo in repos if repo.find('.') == -1]
	except Exception as e:
		print(e)

def main(args):
	repo_names = get_repo_names()
	try:
		for repo_name in repo_names:
			os.chdir(repo_name)
			subprocess.call(["git",  "pull"])
			os.chdir("..")
		print('\nand finished...!\n')
		return 1
	except Exception as e:
		print(e)
		return -1