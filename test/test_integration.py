# Standard Library Imports
import subprocess as sp
import os, sys

# Third Party Imports

# Local Application Imports

# TODO, iS RELATIVE PATH OK FOR CONFIG FILE?

def git_add_commit_push(msg):
    sp.run(['git', 'add', '.'])
    sp.run(['git', 'commit', '-m', f"{msg}"])
    sp.run(['git', 'push', 'origin', 'master'])

# def test_success_update_linux():
    
#     UPDATE_TARGET = 'tmp1'
#     MODEL_TARGET = 'tmp2'
#     TESTING_FILE1 = 'testing.txt'
#     INCLUDED_FILE1 = 'init.txt' # this should already exist on the local git server

#     def success_update_setup():

#         local_test_repo = 'git@192.168.254.234:~/dev/test_main_tmp'
#         sp.run(['git', 'clone', local_test_repo, UPDATE_TARGET])
#         sp.run(['git', 'clone', local_test_repo, MODEL_TARGET])
#         os.chdir(MODEL_TARGET)
#         sp.run([f"echo 'testing update by adding file' > {TESTING_FILE1}"], shell=True)
#         sp.run([f"echo 'testing update by appending file...' >> {INCLUDED_FILE1}"], shell=True)
#         git_add_commit_push('testing commit...')
#         os.chdir('..')

#     def success_update_teardown():
#         os.chdir(MODEL_TARGET)
#         sp.run(['rm', TESTING_FILE1])
#         git_add_commit_push('test done, now deleting any additional files added...')
#         os.chdir('..')
#         sp.run(['rm', '-rf', UPDATE_TARGET])
#         sp.run(['rm', '-rf', MODEL_TARGET])
#         sp.run(['rm', '-rf', '__pycache__'])

#     success_update_setup()
#     sp.run(['python3', '../pyrepoman/__main__.py', 'update'])
#     results = sp.run(['diff', '-r', '--exclude=.git', UPDATE_TARGET, MODEL_TARGET], stdout=sp.PIPE, encoding='utf-8')
#     success_update_teardown()
#     assert results.stdout == ''

# def test_success_fetch_linux():

#     FETCH_TARGET = 'tmp1'
#     MODEL_TARGET = 'tmp2'

#     def success_fetch_setup():

#         host = 'git@192.168.254.234'
#         repos_location = '~/dev/'
#         sp.run(['mkdir', FETCH_TARGET])
#         sp.run(['mkdir', MODEL_TARGET])
#         os.chdir(MODEL_TARGET)
#         results = sp.run(['ssh', host, f"ls {repos_location}"], stdout=sp.PIPE, encoding='utf-8')
#         dirs = results.stdout.split('\n')
#         dirs = dirs[:len(dirs)-1]
#         for dir in dirs:
#             sp.run(['git', 'clone', f"{host}:{repos_location}/{dir}"])
#         os.chdir('..')

#     def success_fetch_teardown():

#         sp.run(['rm', '-rf', FETCH_TARGET])
#         sp.run(['rm', '-rf', MODEL_TARGET])
#         sp.run(['rm', '-rf', '__pycache__'])

#     success_fetch_setup()
#     os.chdir(FETCH_TARGET)
#     sp.run(['python3', '../pyrepoman/__main__.py', 'fetch', 'git@192.168.254.234'])
#     results = sp.run(['diff', '-r', '--exclude=.git', FETCH_TARGET, MODEL_TARGET], stdout=sp.PIPE, encoding='utf-8')
#     os.chdir('..')
#     success_fetch_teardown()
#     assert results.stdout == ''

def test_success_backup_linux():

    BACKUP_TARGET = 'testb'
    MODEL_TARGET = 'tmp2'

    def success_backup_setup():

        host = 'git@192.168.254.234'
        repos_location = '~/dev/'
        sp.run(['mkdir', MODEL_TARGET])
        os.chdir(MODEL_TARGET)
        results = sp.run(['ssh', host, f"ls {repos_location}"], stdout=sp.PIPE, encoding='utf-8')
        dirs = results.stdout.split('\n')
        dirs = dirs[:len(dirs)-1]
        for dir in dirs:
            sp.run(["git", "clone", "--mirror", f"{host}:{repos_location}{dir}", dir])
        os.chdir('..')

    def success_backup_teardown():

        sp.run(['rm', '-rf', BACKUP_TARGET])
        sp.run(['rm', '-rf', MODEL_TARGET])
        sp.run(['rm', '-rf', '__pycache__'])

    success_backup_setup()
    sp.run(['python3', '../pyrepoman/__main__.py', 'backup', 'git@192.168.254.234', BACKUP_TARGET, '--host-path ~/dev/'])
    results = sp.run(['diff', '-r', '--exclude=.git', BACKUP_TARGET, MODEL_TARGET], stdout=sp.PIPE, encoding='utf-8')
    success_backup_teardown()
    assert results.stdout == ''

def test_success_archive_linux():

    ARCHIVE_TARGET = 'testa'
    MODEL_TARGET = 'tmp2'

    def success_archive_setup():

        host = 'git@192.168.254.234'
        repos_location = '~/dev/'
        sp.run(['mkdir', MODEL_TARGET])
        os.chdir(MODEL_TARGET)
        results = sp.run(['ssh', host, f"ls {repos_location}"], stdout=sp.PIPE, encoding='utf-8')
        dirs = results.stdout.split('\n')
        dirs = dirs[:len(dirs)-1]
        for dir in dirs:
            sp.run(["git", "clone", "--mirror", f"{host}:{repos_location}{dir}", dir])
            sp.run(["git", "--git-dir", dir, "bundle", "create", f"{dir}.bundle", "--all"])
            sp.run(["rm", "-rf", dir])
        os.chdir('..')

    def success_backup_teardown():

        sp.run(['rm', '-rf', ARCHIVE_TARGET])
        sp.run(['rm', '-rf', MODEL_TARGET])
        sp.run(['rm', '-rf', '__pycache__'])

    #success_archive_setup()
    sp.run(['python3', '../pyrepoman/__main__.py', 'archive', 'git@192.168.254.234', ARCHIVE_TARGET, '--host-path ~/dev/'])
    results = sp.run(['diff', '-r', '--exclude=.git', ARCHIVE_TARGET, MODEL_TARGET], stdout=sp.PIPE, encoding='utf-8')
    #success_backup_teardown()
    assert results.stdout == ''