import re
import csv

import git_crawler_tools


with open('repos.txt', 'r') as repos, open('results.csv', 'w', newline="") as results:

    lines = repos.readlines()
    writer = csv.writer(results)
    count = 0 # to count amount of results written to csv file

    while lines:
        count += 1
        repo_name = re.sub(r":\n", "", lines[0]) # extract the repo name
        repo_url = lines[2].split()[1] # extract the repo url
        version = lines[3].split()[1] # extract the repo branch

        license = git_crawler_tools.get_license_info(repo_name)
        latest_tag = git_crawler_tools.get_latest_version_from_branch(repo_url, version)

        writer.writerow([repo_url, latest_tag, license]) # write to csv
        print("#"+str(count),repo_name, latest_tag, license, " -written.")

        if len(lines) > 4:
            lines = lines[4:]
        else:
            break

    print("\nALL DONE!!!")
    






