import sys
import os
import subprocess
import time

repository_url = ""
local_directory = ""

def timeout(iterations_attempted: int):
    """
    """

    # arbitrary timeout lengths 
    timeout_durations = [0.2, 0.3, 1, 2, 5]

    if iterations_attempted < len(timeout_durations): 
        duration_of_sleep = timeout_durations[iterations_attempted]
        print("Waiting " + str(duration_of_sleep) + " before next run...")
        time.sleep(duration_of_sleep)
    else:
        print("Error, timeout on operation")
        sys.exit()


def is_avahi_running():
    """Checks if an avahi server instance is running on the server
    """
    try:
        subprocess.run(["systemctl", "is-active", "avahi-daemon"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        print("Error checking avahi run status")
        return False

def initialize_avahi_server():
    """Runs any initial commands which setup the piserver environment
    """
    try:
        subprocess.run("sudo apt-get install avahi-daemon", check=True)
        subprocess.run("sudo systemctl enable avahi-daemon", check=True)
        return True
    except subprocess.CalledProcessError:
        print("Error in initialization of avahi server")
        return False

def git_pull(repository_url, local_directory):
    try:
        subprocess.run(["git", "pull", repository_url], cwd=local_directory, check=True)
        print("Git pull successful.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during git pull: {e}")
        return False


def run_server():
    """
    """
    pass


def main():
    """
    Starts a new s

    """
    print("Checking if avahi server is intialized and running...")
    if not is_avahi_running():
        print("Avahi server not running, starting server...")
        while not is_avahi_running() and initialize_avahi_server():
            print("Attempting to initialize")


    if "--pull-git-changes" in sys.argv:
        print("Pulling any changes from github...")
        git_pull(repository_url, local_directory)

    print("Starting server...")


    






if __name__ == "__main__":
    main()