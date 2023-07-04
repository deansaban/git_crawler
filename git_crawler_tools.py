import subprocess
import requests


def get_latest_version_from_branch(repo_url, version):

    # Define the Git commands
    tag_git_command = ['git', 'ls-remote', '--tags', repo_url] # gets humble tag and its sha
    branch_git_command = ['git', 'ls-remote', repo_url, '--tags', version] # gets version tags and their sha

    # Run the Git commands
    tag_result = subprocess.run(tag_git_command, capture_output=True, text=True)
    branch_result = subprocess.run(branch_git_command, capture_output=True, text=True)

    # Check the return code and output of the Git commands:
    tag_response_dict = {}

    # Parse the lines from the tag command and store the data
    # in a {sha code: tag name} dict format
    if tag_result.returncode == 0:
        # print("Git command executed successfully.")
        lines = tag_result.stdout.splitlines()
        for line in lines:
            parts = line.split()
            if len(parts) == 2:
                sha = parts[0]
                tag = parts[1].replace('refs/tags/', '')
                tag_response_dict[sha] = tag

        # print the dictionary
        # print("Response Dictionary:")
        # for sha, tag in tag_response_dict.items():
        #     print(f"Tag: {tag}, SHA: {sha}")
    else:
        print("Git command failed.")
        print("Error:", tag_result.stderr)


    # get sha code of the version parameter 
    if branch_result.returncode == 0:
        # print("Git command executed successfully.")
        # Split the command output into lines
        lines = branch_result.stdout.splitlines()
        if not lines:
            return "no such name " + version
        parts = lines[0].split()
        branch_sha = parts[0]

        # print the dictionary
        # print("branch sha:" + branch_sha, "verb name: " + verb_name)
    else:
        print("Git command failed.")
        print("Error:", branch_result.stderr)

    # print(tag_response_dict[branch_sha])
    return(tag_response_dict[branch_sha])



def get_license_info(repo_name):
    api_url = f"https://api.github.com/repos/{repo_name}/license"
    response = requests.get(api_url)
    if response.status_code == 200:
        license_info = response.json()
        return license_info.get("license", {}).get("spdx_id") # extracts the license name
    else:
        return "no license"
