# python 3.10-4

import requests
import os
from bs4 import BeautifulSoup 
import json
import re

debug = False

root_dir = "{ROOT_DIR}"
save_path = f"{root_dir}/AST/tmp.log"

with open(f'{root_dir}/config.json', 'r') as jf:
    config_data = json.load(jf)

project_name = config_data['project_name']
project_author = config_data['project_author']

access_token = config_data['access_token']
heads = {"Authorization": "token " + access_token}

def collectGitLog():
    command = f"cd {root_dir}/Source_Code/{project_name} && git show {commit_sha} > {save_path}"
    os.system(command)

def collectBigFunctions(commit_sha):

    bug_function_names = []
    result_function_names = []
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
        print(f"Parse Page OK")

    
    for bug_function_name in soup.find_all("td","blob-code blob-code-inner blob-code-hunk"):
        if bug_function_name.text.strip() != '':
            bug_function_names.append(bug_function_name.text.strip())

    # Post process
    for function in bug_function_names:
        # print(function)
        function_name = ""
        if 'func' in function and 'function' not in function:
            # print(function)
            try:
                function_name = re.search("(.*)func (.*)\((.*)", function)[2]
            except Exception as e:
                print(e)
            # result_function_names.append(function_name)
        elif 'function' in function:
            function_name = re.search("(.*)function (.*)\((.*)", function)[2]
            # result_function_names.append(function_name)
        refined_function_name = re.sub('\(.*?\) ','',function_name)
        if 'func' in refined_function_name:
            print(f"** - Find func in BigFunction, replce from {refined_function_name}")
            refined_function_name = refined_function_name.replace("func", "")
        if refined_function_name != '' and refined_function_name not in result_function_names:
            result_function_names.append(refined_function_name)

    return result_function_names

def collectSmallFunctions():
    small_function_names = []
    with open(save_path, 'r') as glf:
        data = glf.readlines()
    for line in data:
        if line[0] == '-' and '(' in line:
            function_name = ''
            try:
                function_name = re.search("(.*) (.*)\((.*)", line)[2]
            except Exception as e:
                print(e)
                print(f"* Error parsing line {line}") 
            if function_name != '':
                if function_name not in small_function_names:
                    small_function_names.append(function_name)
    
    return small_function_names

def getTestFunctions(commit_sha):

    # Get parent sha
    commandp = f"cd {root_dir}/Source_Code/{project_name} && git log --pretty=format:'%P' {commit_sha} -1"
    with os.popen(commandp) as cm1:
        parent_commit_sha = cm1.readlines()[0]

    # Switch to parent commit
    command1 = f"cd {root_dir}/Source_Code/{project_name} && git reset --hard {parent_commit_sha}"
    os.system(command1)
    
    # Get test functions
    command2 = f"cd {root_dir}/AST && go run extract_ast.go > logs.out"
    os.system(command2)

    with open(f"{root_dir}/AST/logs.out") as tf:
        test_functions = tf.readlines()
    
    return test_functions

if __name__ == '__main__':
    
    # Read all commits
    with open(f"{root_dir}/Sample/commits_{project_name}_filter.json", 'r') as cmf:
        commits_data = json.load(cmf)
    all_commit_num = len(commits_data)
    no_test_commit_num = 0
    for index, commit in enumerate(commits_data):

    # commit_sha = "9c444070ec7bb83995dbc0185da68284da71c554"
        commit_sha = commit['sha']
        print(f"Parsing Commit {commit_sha}")
        tested = 0

        # Prepare Bugful Functions
        collectGitLog()
        big_functions = collectBigFunctions(commit_sha)
        small_functions = collectSmallFunctions()

        # Compare with Test Functions 
        test_functions = getTestFunctions(commit_sha)

        for function in big_functions:
            if function in str(test_functions):
                print(f"Found Function {function} in Tests")
                tested = 1

        for function in small_functions:
            if function in str(test_functions):
                print(f"Found Function {function} in Tests")
                tested = 1
        
        if not tested:
            no_test_commit_num += 1
            print("#"*40+f"\nCommit {index} does not contain in tests\n")
        else:
            print("#"*40+f"\nParse {index}/{all_commit_num} commit success\n")

        if debug:
            input_command = input("Command for viewing: \n")
            if input_command == 'n':
                continue

    print(f"Result: {no_test_commit_num}/{all_commit_num}")