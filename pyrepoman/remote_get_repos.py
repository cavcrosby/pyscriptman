# Standard Library Imports
import os

# Third Party Imports

# Local Application Imports

def get_repo_names():
    
    try:
        repos = list()
        dirs = os.listdir(os.getcwd())
        dirs = [dir for dir in dirs if dir.find('.') == -1]
        for dir in dirs:
            os.chdir(dir)
            if('.git' in os.listdir()):
                repos.append(dir)
            os.chdir('..')
        return ','.join(repos)
    except Exception as e:
        print(e)

print(get_repo_names())