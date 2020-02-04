# Standard Library Imports
try:
	import os, datetime, subprocess, requests, smtplib, configparser, collections
except Exception as e:
	print(e)
    # TODO how to deal with libraries not present when the script is running?

# Third Party Imports

# Local Application Imports

config_app = configparser.ConfigParser()
config_app.read('git_backup.ini')
script_configs = config_app['git_backup']

def get_repo_names_and_urls(github_api_url):
	try:
		repos = requests.get(github_api_url, auth=(user, api_token), params=payload)
		return {(repo['name']):repo['svn_url'] for repo in repos.json()}
	except Exception as e:
		send_email("Failure In Script", "Exception occured when using GitHub's API\n\n{0}".format(e), email, recip_email)

def send_email(subj, msg, source, to):
    smtpObj = smtplib.SMTP(smtp_server, 587) # TLS encryption is assumed
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(email, password)
    smtpObj.sendmail(source, to, "Subject: git_backup.py {0}\n\n{1}\n\nboop-boop, git_backup.py".format(subj, msg))
    smtpObj.quit()
    # TODO if this fails, send to log file?

def dir_exist(dir_name):
    dir_contents = os.listdir()
    return dir_name in dir_contents

def create_dir(dir_name):
    subprocess.run(["mkdir", dir_name])

def create_mirror(url, loc):
    subprocess.run(["git", "clone", "--mirror", url, loc])

def update_mirror(loc):
    subprocess.run(["git", "--git-dir", loc, "remote", "update"])

def clear_old_bundles(loc):
    subprocess.run(["rm", "-rf", "{0}/*".format(loc)])

def clear_old_repos():
    collections.deque(
        map(lambda repo: subprocess.run(["rm", "-rf", "{0}/{1}".format(repobfull, repo)]), to_delete),
        maxlen=0
    )
    # collections.deque is used to prevent overhead when executing the map iterator (that is, no output should be recorded/saved).

def create_bundle(m_repo, file_loc):
    subprocess.run(["git", "--git-dir", m_repo, "bundle", "create", "{0}.bundle".format(file_loc), "--all"])

def remove_from_to_delete(repo_name):
    to_delete.remove(repo_name)
	
user = script_configs["user"]
api_token = script_configs["api_token"]
payload = script_configs["payload"]
github_api_url = script_configs["github_api_url"]
email = script_configs["email"]
recip_email = script_configs["recip_email"]
password = script_configs["password"]
smtp_server = script_configs["smtp_server"]
repobfull = script_configs["repobfull"]
repobbundle = script_configs["repobbundle"]

if(not dir_exist(repobfull)):
    create_dir(repobfull)

if(not dir_exist(repobbundle)):
    create_dir(repobbundle)

repo_names_and_urls = get_repo_names_and_urls(github_api_url) # key is repo name, value is repo url
try:
    to_delete = os.listdir(repobfull)
    clear_old_bundles(repobbundle)
    for repo_name in repo_names_and_urls:
        bfull_content = os.listdir("{0}".format(repobfull))
        bbundle_content = os.listdir("{0}".format(repobbundle))
        bfull_location = "{0}/{1}".format(repobfull, repo_name)
        bbundle_location = "{0}/{1}".format(repobbundle, repo_name)
        if(not repo_name in bfull_content):
            create_mirror(repo_names_and_urls[repo_name], bfull_location)
            create_bundle(bfull_location, bbundle_location)
        else:
            update_mirror(bfull_location)
            create_bundle(bfull_location, bbundle_location)
            remove_from_to_delete(repo_name)
    clear_old_repos() # from repobfull
except Exception as e:
	send_email("Failure In Script", "Exception occured when going through repos, executing git commmands\n\n{0}".format(e), email, email)