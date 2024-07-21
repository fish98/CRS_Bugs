# python 3.8

# Github Commits

from urllib import response
import requests
import json
from bs4 import BeautifulSoup 

import time

root_dir = "{ROOT_DIR}"

if __name__ == '__main__':
    
    result_commits = []

    with open(f'{root_dir}/config.json', 'r') as jf:
        config_data = json.load(jf)

    project_name = config_data['project_name']
    project_author = config_data['project_author']
    query_type = config_data['query_type']

    page_num = config_data['page_num']
    per_page = config_data['per_page']
    
    access_token = config_data['access_token']
    heads = {"Authorization": "token " + access_token}

    while(1):

        site = f"https://api.github.com/repos/{project_author}/{project_name}/{query_type}?page={page_num}&per_page={per_page}"
        try:
            response = requests.get(site, headers=heads)
        except Exception as e:
            print(e)

        data = response.json()

        if(data == []):
            print("All commits parsed")
            break
        if query_type == "commits":
            for commit_data in data:
            # Check Messages contain key words
                request_sha = commit_data['sha']
                
                changed_files = []

                request_sha = f"https://github.com/{project_author}/{project_name}/commit/{commit_data['sha']}"
                
                try:
                    commit_response = requests.get(request_sha, headers=heads)
                except Exception as e:
                    print(e)

                soup = BeautifulSoup(commit_response.text, 'html.parser')
                for changed_file in soup.find_all("a","Link--primary"):
                    changed_files.append(changed_file.text.strip())
                    time.sleep(0.5)
                    print(f"Successful load changed file {changed_files}")
                result_commits.append({"sha": commit_data['sha'], "time": commit_data['commit']['author']['date'], "changed_files": changed_files, "title": commit_data['commit']['message']}) # result_commits.append({kw: commit_data['sha']}+'\n')
                        # break
            print("Parse page {} Down".format(page_num))

        page_num = page_num + 1
        
    print(f"Total Commits Number for Project {project_name}: {len(result_commits)}")

    json_result = json.dumps(result_commits)
    with open(f'{root_dir}/Collection/{query_type}_{project_name}_full_result.json', 'w') as p:
        p.write(json_result)



