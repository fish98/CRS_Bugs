# python 3.10-4

# Figure out what sort of files are modifed in the highest frequency

import json

root_dir = "{ROOT_DIR}"

mode = "Sample"

if __name__ == '__main__':

    with open(f'{root_dir}/config.json', 'r') as jf:
        config_data = json.load(jf)

    project_name = config_data['project_name']
    query_type = config_data['query_type']

    # Read filtered json 
    with open(f"{root_dir}/{mode}/{query_type}_{project_name}_filter.json", 'r') as rf:
        data = json.load(rf)

    modified_files = {}

    for commit in data:
        for change_file in commit["changed_files"]:
            if change_file in modified_files:
                modified_files[change_file] += 1
            else:
                modified_files[change_file] = 1

    # Find the most hot files
    sorted_modified_files = sorted(modified_files.items(), key=lambda s:s[1], reverse=True)
