# python 3.10-4

# Collect bug related big functions

from urllib import response
import requests
import json
import re
from bs4 import BeautifulSoup 

import time

mode = "Sample"
years = '1y'

save = True


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

    # Load commits data
    with open(f'{root_dir}/{mode}/commits_{project_name}_filter-{years}.json', 'r') as df:
        commits_data = json.load(df)

    go_bug_function_result = []
    py_bug_function_result = []
    
    for index, commit in enumerate(commits_data):
        
        commit_sha = commit['sha']
        bug_function_names = []

        site = f'https://github.com/{project_author}/{project_name}/commit/{commit_sha}'

        try:
            response = requests.get(site, headers=heads)
        except Exception as e:
            print(e)

        soup = BeautifulSoup(response.text, 'html.parser')

        if "Oops" in response.text:
            print(site)
            print("QWQ, this needs manual check")
        else:
            print(f"Index {index} / {len(commits_data)} OK")

        
        for bug_function_name in soup.find_all("td","blob-code blob-code-inner blob-code-hunk"):
            if bug_function_name.text.strip() != '':
                bug_function_names.append(bug_function_name.text.strip())

        for function in bug_function_names:
            
            if 'func' in function and 'function' not in function:
                # print(function)
                function_name = re.search("(.*)func(.*)", function)[2]
                go_bug_function_result.append(function_name)
            elif 'function' in function:
                function_name = re.search("(.*)function(.*)", function)[2]
                py_bug_function_result.append(function_name)

    if save:
        with open(f"{root_dir}/BugFunctions/{project_name}-{years}.data", 'w') as savef:
            savef.write()
