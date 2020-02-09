# Standard Library Imports

# Third Party Imports

# Local Application Imports
import apis

def get_arg_value(field):

	return field[1]

def get_repo_names_and_urls(host, action, user = '', api_token = '', payload = ''):
	
	endpoint = apis.get_hostname_func_endpoint(host, action)
	return apis.get_hostname_func_obj(host, action)(endpoint, user, api_token, payload)

def not_supported_host(host):
	
	if(not apis.supported_endpoint(host)):
		print("Error: web host passed in is not currently supported")
		return True