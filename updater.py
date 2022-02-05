import os
import dotenv
from github import Github


dotenv.load_dotenv()

github_access = Github(os.environ['GITHUB_ACCESS_TOKEN'])


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
    repo = github_access.get_repo(os.environ['REPO_NAME'])

    version_file = repo.get_contents('remote_version.cfg')
    version = version_file.decoded_content.decode('utf-8')

    return version


def init_update_operation():
    """Should run only if a new version is found on the repository

        Updates all the local files and starts the main program
    """
    print('versions not matching, running update function')

    # get all the new files from the repository in a temp directory


def start_main_program(location):
    pass


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
