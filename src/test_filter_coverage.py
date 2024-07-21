# # python 3.10-4

import json
import time
import re
import subprocess

root_dir = "{ROOT_DIR}"

mode = "read" # analysis / read

if __name__ == '__main__':
    
    Version = "1.1.4"

    code_dir = f"{root_dir}/Source_Code/runc-{Version}"
    log_dir = f"{root_dir}/Test"
    log_file_path = f"{log_dir}/runc-{Version}-unittest.log"

    function_names = []

    with open(log_file_path, 'r') as lf:
        log_data = lf.readlines()

    for log in log_data:
        if "PASS:" in log:
            function_name = re.search('PASS: (.*) (.*)', log)[1]
            function_names.append(function_name)


        