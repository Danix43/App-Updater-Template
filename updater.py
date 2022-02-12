import os
import dotenv
from github import Github
import requests
import shutil

dotenv.load_dotenv()

github_access = Github(os.environ['GITHUB_ACCESS_TOKEN'])
repo = github_access.get_repo(os.environ['REPO_NAME'])


def get_local_version():
    """ Check the local version of the program"""

    with open('app.cfg', 'r') as config:
        version = config.readline().strip()

        if version == '':
            raise Exception('No version found inside the config file')

        return version


def get_remote_version():
    """ Check the latest version of the program on the repository

    NOTE: change to something that doesn't need a github access token
    """
    version_file = repo.get_contents('remote_version.cfg')
    version = version_file.decoded_content.decode('utf-8')

    return version


def init_update_operation():
    """Should run only if a new version is found on the repository

        Updates all the local files and starts the main program
    """
    print('versions not matching, running update function')

    # get all the new files from the repository in a temp directory
    try:
        os.mkdir('temp')
    except FileExistsError:
        print('temp folder already exists')

    temp_folder_path = os.getcwd() + os.sep + 'temp'
    print('temp folder path: {}'.format(temp_folder_path))

    # get the download links from the repository
    files_links = list(
        file.download_url for file in repo.get_contents('update'))

    # download the files to the temp folder
    for link in files_links:
        download_file(link, temp_folder_path)

    # copy from temp to root


def start_main_program(file_path):
    pass


def download_file(url, destinationPath=''):
    """
        Found here: https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests

        Added destinationPath param to download the file to an another folder other than the root
    """

    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(destinationPath + os.sep + local_filename, 'wb') as f:
            # raw bytes fix
            r.raw.decode_content = True

            shutil.copyfileobj(r.raw, f)
    return local_filename


if __name__ == '__main__':
    local_version = get_local_version()
    remote_version = get_remote_version()

    print('checking the local and the remote versions if they match')
    print('local version: {} | remote version: {}'.format(
        local_version, remote_version))

    if local_version == remote_version:
        print('the same version runs on local and remote')
    else:
        init_update_operation()
