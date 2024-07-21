# python 3.10-4

import json
import webbrowser
import pyperclip

# Set python path dir
root_dir = "{ROOT_DIR}"

mode = "Sample"

if __name__ == '__main__':

    with open(f'{root_dir}/config.json', 'r') as jf:
        config_data = json.load(jf)

    # print(config_data)
    project_name = config_data['project_name']
    project_author = config_data['project_author']
    query_type = config_data['query_type']

    filename = f"{query_type}_{project_name}_filter.json"
    print(f"Reading File {filename}\n")

    with open(f'{root_dir}/{mode}/{filename}', 'r') as p:
        data = json.loads(p.read())
    commits_index = 0
    sample_commits = []
    sample_number = len(data)      
    while(commits_index != sample_number):
        input_command = input("Command for viewing: \n")

        if input_command.isdigit():
            display_data = data[int(input_command)]
            commits_index = int(input_command)
            # for clipboard
            print("##################################################################")
            print(f"Send Current Commit Number {commits_index} to Clip Board\n")
            pyperclip.copy(display_data[list(display_data.keys())[0]])
            print(f"The SHA is {display_data[list(display_data.keys())[0]]}\n")
            print("******************************************************************\n")
            print(f"The Message for the Commit is: \n{display_data['title']}")
            print("##################################################################\n")
        elif input_command == 'p': #pull
            pull_num = input("Input Pull Request Index: \n")
            webbrowser.open(f"github.com/{project_author}/{project_name}/pull/{pull_num}")
        elif input_command == 'i': #pull
            issue_num = input("Input Issue Index: \n")
            webbrowser.open(f"github.com/{project_author}/{project_name}/issues/{issue_num}")
        elif input_command == 'c': #commit
            # commit_num = input("Input Commit Index: \n")
            webbrowser.open(f"github.com/{project_author}/{project_name}/commit/{display_data[list(display_data.keys())[0]]}")
        elif input_command == 'n': #next
            commits_index = commits_index + 1
            if(commits_index < len(data)):
                display_data = data[commits_index]
                print(f"Send Current Commit Number {commits_index} to Clip Board\n")
                pyperclip.copy(display_data[list(display_data.keys())[0]])
                print(f"The SHA is {display_data[list(display_data.keys())[0]]}\n")
                print("******************************************************************\n")
                print(f"The Message for the Commit is: \n{display_data['title']}")
                print("##################################################################\n")
            else:
                print("Exceed data length!")
        
