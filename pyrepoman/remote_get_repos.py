# Standard Library Imports
import os

# Third Party Imports

# Local Application Imports

def get_repo_names():
    
    try:
        scripts_dir = os.path.dirname(os.path.realpath(__file__))
        dirs = os.listdir(scripts_dir)
        is_a_dir = list()
        for dir in dirs:
            if(os.path.isdir(f"{scripts_dir}/{dir}")):
                is_a_dir.append(dir)
        return ','.join(is_a_dir)
    except Exception as e:
        print(e)

print(get_repo_names())