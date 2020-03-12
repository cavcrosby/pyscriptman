# Standard Library Imports
import os

# Third Party Imports

# Local Application Imports

def get_dir_names():
    
    try:
        scripts_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(scripts_dir)
        nodes = os.listdir()
        is_a_dir = list()
        for node in nodes:
            if(os.path.isdir(node)):
                is_a_dir.append(node)
        return ','.join(is_a_dir)
    except Exception as e:
        print(e)

print(get_dir_names())