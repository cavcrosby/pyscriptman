# Standard Library Imports

# Third Party Imports

# Local Application Imports
import apis

def get_arg_value(field):

	return field[1]

def get_repo_names_and_urls(HOST, action, USER, API_TOKEN, PAYLOAD):
	
	api = apis.get_hostname_module_func_api(HOST, action)
	return apis.get_hostname_module_func(HOST, action)(api, USER, API_TOKEN, PAYLOAD)