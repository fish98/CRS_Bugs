# python 3.10-4

# Read/Analyze the test functions covered in the unit test

import json
import time
import re
import subprocess
import asyncio
import pyperclip
import random

root_dir = "{ROOT_DIR}"

mode = "read" # analysis / read
sample = True

project = 'runc' # runc / containerds
Version = "1.1.4" # 1.1.4 / 1.6.15

async def search_function_file(code_dir, function_name):
    cmdline = f"find {code_dir} -type f -name '*.go'|xargs grep -n '{function_name}'"
    subprocess.Popen(cmdline, shell=True)
    # Dirty Code
    await asyncio.sleep(1)

if __name__ == '__main__':

    code_dir = f"{root_dir}/Source_Code/{project}-{Version}"
    log_dir = f"{root_dir}/Test"
    log_file_path = f"{log_dir}/{project}-{Version}-unittest.log"

    function_names = []

    with open(log_file_path, 'r') as lf:
        log_data = lf.readlines()

    for log in log_data:
        if "PASS:" in log:
            function_name = re.search('PASS: (.*) (.*)', log)[1]
            function_names.append(function_name)

    if mode == 'read':
        test_index = 0
        read_indexs = []
        while(test_index != len(function_names)+1):
            input_command = input("Command for reading: \n")
            if input_command.isdigit():
                # display_data = data[int(input_command)]
                test_index = int(input_command)
                function_name = function_names[test_index]
                # for clipboard
                print("##################################################################")
                print(f"Send Current Test Name {test_index} to Clip Board\n")
                print(f"Test Function Name: {function_name}\n")
                pyperclip.copy(function_name)
                function_name = function_name + '('
                search_task = search_function_file(code_dir, function_name)
                asyncio.run(search_task)
                print("##################################################################\n")
                # For sample option
                read_indexs.append(test_index)
            # elif input_command == 'p': #pull
            #     pull_num = input("Input Pull Request Index: \n")
            #     webbrowser.open(f"github.com/{project_author}/{project_name}/pull/{pull_num}")
            elif input_command == 'n': #next
                if sample:
                    test_index = random.randint(0, len(function_names))
                    while(test_index in read_indexs):
                        test_index = random.randint(0, len(function_names))
                else:
                    test_index = test_index + 1
                if(test_index < len(function_names)):
                    function_name = function_names[test_index]
                    # for clipboard
                    print("##################################################################")
                    print(f"Send Current Test Name {test_index} to Clip Board\n")
                    print(f"Test Function Name: {function_name}\n")
                    pyperclip.copy(function_name)
                    function_name = function_name + '('
                    search_task = search_function_file(code_dir, function_name)
                    asyncio.run(search_task)
                    print("##################################################################\n")
                else:
                    print("Exceed data length!")
    
    elif mode == 'analysis':
        f = open(f'{log_dir}/{project}-{Version}-unittest-functions.data','w')
        f.write(str(function_names))
        f.close()

