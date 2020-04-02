# Standard Library Imports
import subprocess as sp
import os, sys, filecmp, shutil, subprocess

# Third Party Imports

# Local Application Imports

LOCAL_GIT_SERVER = "git@192.168.254.234"
LOCAL_GIT_SERVER_PATH = "~/dev/"
LOCAL_GIT_SERVER_PATH_EXPANDED = subprocess.run(['ssh', LOCAL_GIT_SERVER, f'python3 -c "import os; print(os.path.expanduser(\\"{LOCAL_GIT_SERVER_PATH}\\"));"'], \
                        stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip()

TEST_SUCCESS_UPDATE_REPO_ON_SERVER = "py_automate_indeed"

def git_add_commit_push(msg):
    sp.run(['git', 'add', '.'])
    sp.run(['git', 'commit', '-m', f"{msg}"])
    sp.run(['git', 'push', 'origin', 'master'])

def diff(dcmp):

    if dcmp.diff_files or dcmp.left_only or dcmp.right_only:
        print("Shared Files Differences: " + str(dcmp.diff_files))
        print(f"{dcmp.left} Has Exclusively: " + str(dcmp.left_only))
        print(f"{dcmp.right} Has Exclusively: " + str(dcmp.right_only))
        return True
    for sub_dcmp in dcmp.subdirs: # key ==> common_dir string, value ==> filecmp object
        if(sub_dcmp == '.git'):
            continue
        return diff(dcmp.subdirs[sub_dcmp])
    return False

def delete_folder_and_contents(dir):
    
    os.chdir(dir)
    nodes = os.scandir()
    dir_entry = nodes.__next__()
    try:
        while(dir_entry):
            if(dir_entry.is_dir()):
                shutil.rmtree(dir_entry)
                dir_entry = nodes.__next__()
            else:
                os.remove(dir_entry)
                dir_entry = nodes.__next__()
    except StopIteration as e:
        pass
        #print(e)
    finally:
        os.chdir('..')
        os.rmdir(dir)

def test_success_update():
    
    UPDATE_TARGET = 'tmp1'
    MODEL_TARGET = 'tmp2'
    TESTING_FILE1 = 'testing.txt'

    def success_update_setup():

        local_test_repo = f"{LOCAL_GIT_SERVER}:{LOCAL_GIT_SERVER_PATH_EXPANDED}{TEST_SUCCESS_UPDATE_REPO_ON_SERVER}"
        sp.run(['git', 'clone', local_test_repo, UPDATE_TARGET])
        sp.run(['git', 'clone', local_test_repo, MODEL_TARGET])
        os.chdir(MODEL_TARGET)
        sp.run([f"echo 'testing update by adding file' > {TESTING_FILE1}"], shell=True)
        git_add_commit_push('testing commit...')
        os.chdir('..')

    def success_update_teardown():
        os.chdir(MODEL_TARGET)
        os.remove(TESTING_FILE1)
        git_add_commit_push('test done, now deleting any additional files added...')
        os.chdir('..')
        delete_folder_and_contents(UPDATE_TARGET)
        delete_folder_and_contents(MODEL_TARGET)

    success_update_setup()
    sp.run(['python3', '../pyrepoman/__main__.py', 'update'])
    dcmp = filecmp.dircmp(UPDATE_TARGET, MODEL_TARGET)
    different = diff(dcmp)
    success_update_teardown()
    assert different == False

def test_success_fetch():

    FETCH_TARGET = 'tmp1'
    MODEL_TARGET = 'tmp2'

    def success_fetch_setup():

        os.mkdir(FETCH_TARGET)
        os.mkdir(MODEL_TARGET)
        os.chdir(MODEL_TARGET)
        results = sp.run(['ssh', LOCAL_GIT_SERVER, f"ls {LOCAL_GIT_SERVER_PATH_EXPANDED}"], stdout=sp.PIPE, encoding='utf-8')
        dirs = results.stdout.split('\n')
        dirs = dirs[:len(dirs)-1]
        for dir in dirs:
            sp.run(['git', 'clone', f"{LOCAL_GIT_SERVER}:{LOCAL_GIT_SERVER_PATH_EXPANDED}/{dir}"])
        os.chdir('..')

    def success_fetch_teardown():

        delete_folder_and_contents(FETCH_TARGET)
        delete_folder_and_contents(MODEL_TARGET)

    success_fetch_setup()
    os.chdir(FETCH_TARGET)
    sp.run(['python3', '../../pyrepoman/__main__.py', 'fetch', LOCAL_GIT_SERVER, '--host-path', LOCAL_GIT_SERVER_PATH_EXPANDED])
    os.chdir('..')
    dcmp = filecmp.dircmp(FETCH_TARGET, MODEL_TARGET)
    different = diff(dcmp)
    success_fetch_teardown()
    assert different == False

def test_success_backup():

    BACKUP_TARGET = 'testbackup'
    MODEL_TARGET = 'tmp2'

    def success_backup_setup():

        os.mkdir(MODEL_TARGET)
        os.chdir(MODEL_TARGET)
        results = sp.run(['ssh', LOCAL_GIT_SERVER, f"ls {LOCAL_GIT_SERVER_PATH_EXPANDED}"], stdout=sp.PIPE, encoding='utf-8')
        dirs = results.stdout.split('\n')
        dirs = dirs[:len(dirs)-1]
        for dir in dirs:
            sp.run(["git", "clone", "--mirror", f"{LOCAL_GIT_SERVER}:{LOCAL_GIT_SERVER_PATH_EXPANDED}{dir}", dir])
        os.chdir('..')

    def success_backup_teardown():

        delete_folder_and_contents(BACKUP_TARGET)
        delete_folder_and_contents(MODEL_TARGET)

    success_backup_setup()
    sp.run(['python3', '../pyrepoman/__main__.py', 'backup', LOCAL_GIT_SERVER, BACKUP_TARGET, '--host-path', LOCAL_GIT_SERVER_PATH_EXPANDED])
    dcmp = filecmp.dircmp(BACKUP_TARGET, MODEL_TARGET)
    different = diff(dcmp)
    success_backup_teardown()
    assert different == False

def test_success_archive():

    ARCHIVE_TARGET = 'testarchive'
    MODEL_TARGET = 'tmp2'

    def success_archive_setup():

        os.mkdir(MODEL_TARGET)
        os.chdir(MODEL_TARGET)
        results = sp.run(['ssh', LOCAL_GIT_SERVER, f"ls {LOCAL_GIT_SERVER_PATH_EXPANDED}"], stdout=sp.PIPE, encoding='utf-8')
        dirs = results.stdout.split('\n')
        dirs = dirs[:len(dirs)-1]
        for dir in dirs:
            sp.run(["git", "clone", "--mirror", f"{LOCAL_GIT_SERVER}:{LOCAL_GIT_SERVER_PATH_EXPANDED}{dir}", dir])
            sp.run(["git", "--git-dir", dir, "bundle", "create", f"{dir}.bundle", "--all"])
            delete_folder_and_contents(dir)
        os.chdir('..')

    def success_archive_teardown():

        delete_folder_and_contents(ARCHIVE_TARGET)
        delete_folder_and_contents(MODEL_TARGET)

    success_archive_setup()
    sp.run(['python3', '../pyrepoman/__main__.py', 'archive', LOCAL_GIT_SERVER, ARCHIVE_TARGET, '--host-path', LOCAL_GIT_SERVER_PATH_EXPANDED])
    dcmp = filecmp.dircmp(ARCHIVE_TARGET, MODEL_TARGET)
    different = diff(dcmp)
    success_archive_teardown()
    assert different == False
